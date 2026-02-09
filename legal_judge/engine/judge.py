"""Main judge engine that orchestrates analysis and renders judgments."""

from __future__ import annotations

from legal_judge.engine.analyzer import IRACAnalysis, LegalAnalyzer
from legal_judge.engine.precedent import PrecedentMatcher
from legal_judge.models.case import Case, CaseStatus, CaseType, PartyRole
from legal_judge.models.judgment import (
    Disposition,
    Judgment,
    JudgmentSection,
    RemedyType,
)
from legal_judge.models.legal import LegalPrinciple, Precedent, Statute


class JudgeEngine:
    """Top-level engine: takes a Case in, produces a Judgment out."""

    def __init__(
        self,
        statutes: list[Statute] | None = None,
        principles: list[LegalPrinciple] | None = None,
        precedents: list[Precedent] | None = None,
    ) -> None:
        matcher = PrecedentMatcher(precedents)
        self._analyzer = LegalAnalyzer(
            statutes=statutes,
            principles=principles,
            precedent_matcher=matcher,
        )
        self._decided_cases: list[tuple[Case, Judgment]] = []

    @property
    def analyzer(self) -> LegalAnalyzer:
        return self._analyzer

    @property
    def case_history(self) -> list[tuple[Case, Judgment]]:
        return list(self._decided_cases)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def adjudicate(self, case: Case) -> Judgment:
        """Analyze a case and render a judgment."""
        case.status = CaseStatus.DELIBERATION
        analyses = self._analyzer.analyze_case(case)
        disposition = self._determine_disposition(analyses, case)
        remedy = self._determine_remedy(disposition, case)
        prevailing = self._determine_prevailing_party(analyses, case)
        dissent = self._generate_dissent(analyses, case, disposition, prevailing)
        judgment = self._build_judgment(
            case, analyses, disposition, remedy, prevailing, dissent
        )
        case.status = CaseStatus.DECIDED
        self._decided_cases.append((case, judgment))
        return judgment

    def appeal(self, original_case: Case, original_judgment: Judgment, new_arguments: list | None = None, new_evidence: list | None = None) -> Judgment:
        """Appeal a prior judgment with optional new arguments and evidence."""
        appeal_case = original_case.model_copy(deep=True)
        appeal_case.case_id = f"{original_case.case_id}-APPEAL"
        appeal_case.status = CaseStatus.APPEALED

        # Upgrade party roles for appeal context.
        for party in appeal_case.parties:
            if party.role == PartyRole.PLAINTIFF:
                party.role = PartyRole.APPELLANT
            elif party.role == PartyRole.DEFENDANT:
                party.role = PartyRole.APPELLEE

        if new_arguments:
            appeal_case.arguments.extend(new_arguments)
        if new_evidence:
            appeal_case.evidence.extend(new_evidence)

        # Add the original judgment's findings to facts.
        appeal_case.facts.append(
            f"PRIOR JUDGMENT: The lower court ruled {original_judgment.disposition.value} "
            f"with confidence {original_judgment.confidence:.0%}, "
            f"finding for {original_judgment.prevailing_party}."
        )

        return self.adjudicate(appeal_case)

    def compare_cases(self, case_a: Case, case_b: Case) -> dict:
        """Compare two cases and return a similarity analysis."""
        kw_a = PrecedentMatcher._extract_case_keywords(case_a)
        kw_b = PrecedentMatcher._extract_case_keywords(case_b)

        overlap = kw_a & kw_b
        union = kw_a | kw_b
        keyword_similarity = len(overlap) / len(union) if union else 0.0

        type_match = case_a.case_type == case_b.case_type
        jurisdiction_match = case_a.jurisdiction == case_b.jurisdiction

        # Issue overlap.
        issues_a = {i.lower() for i in case_a.issues}
        issues_b = {i.lower() for i in case_b.issues}
        issue_overlap = issues_a & issues_b

        overall = (
            0.4 * keyword_similarity
            + 0.3 * (1.0 if type_match else 0.0)
            + 0.1 * (1.0 if jurisdiction_match else 0.0)
            + 0.2 * (len(issue_overlap) / max(len(issues_a | issues_b), 1))
        )

        return {
            "overall_similarity": round(overall, 3),
            "keyword_similarity": round(keyword_similarity, 3),
            "common_keywords": sorted(overlap)[:20],
            "case_type_match": type_match,
            "jurisdiction_match": jurisdiction_match,
            "common_issues": sorted(issue_overlap),
        }

    def find_similar_in_history(self, case: Case, top_k: int = 5) -> list[dict]:
        """Search decided cases for similar prior matters (DeepJudge-style)."""
        results: list[dict] = []
        for past_case, past_judgment in self._decided_cases:
            if past_case.case_id == case.case_id:
                continue
            sim = self.compare_cases(case, past_case)
            results.append({
                "case_id": past_case.case_id,
                "title": past_case.title,
                "disposition": past_judgment.disposition.value,
                "prevailing_party": past_judgment.prevailing_party,
                **sim,
            })
        results.sort(key=lambda r: r["overall_similarity"], reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # Dissenting opinion generation
    # ------------------------------------------------------------------

    def _generate_dissent(
        self,
        analyses: list[IRACAnalysis],
        case: Case,
        disposition: Disposition,
        prevailing_party: str,
    ) -> str:
        """Generate a dissenting opinion by arguing the other side."""
        if not analyses or not case.parties:
            return ""

        losing_parties = [
            p.name for p in case.parties if p.name != prevailing_party
        ]
        losing_name = losing_parties[0] if losing_parties else "the non-prevailing party"

        # Find the losing party's strongest arguments.
        losing_args = [a for a in case.arguments if a.party_name == losing_name]
        losing_evidence = [e for e in case.get_admissible_evidence() if e.submitted_by == losing_name]

        parts: list[str] = []
        parts.append(
            f"DISSENTING OPINION: The undersigned respectfully dissents from the "
            f"majority's {disposition.value} disposition."
        )

        if losing_args:
            parts.append(
                f"\nThe majority fails to give sufficient weight to {losing_name}'s arguments:"
            )
            for arg in losing_args:
                parts.append(f"  - {arg.claim}")
                if arg.legal_basis:
                    parts.append(f"    Legal basis: {', '.join(arg.legal_basis)}")

        if losing_evidence:
            parts.append(f"\nThe following evidence warrants greater consideration:")
            for ev in losing_evidence:
                parts.append(f"  - {ev.title}: {ev.description}")

        # Challenge the weakest analysis point.
        if analyses:
            weakest = min(analyses, key=lambda a: a.confidence)
            if weakest.confidence < 0.75:
                parts.append(
                    f"\nThe analysis on '{weakest.issue}' achieves only "
                    f"{weakest.confidence:.0%} confidence, which is insufficient to "
                    f"justify the majority's conclusion."
                )

        parts.append(
            f"\nFor these reasons, the dissent would find in favor of {losing_name}."
        )
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Disposition logic
    # ------------------------------------------------------------------

    def _determine_disposition(
        self, analyses: list[IRACAnalysis], case: Case
    ) -> Disposition:
        if not analyses:
            return Disposition.DISMISSED

        # Dismiss cases with no substantive content.
        if not case.facts and not case.arguments and not case.evidence:
            return Disposition.DISMISSED

        avg_confidence = sum(a.confidence for a in analyses) / len(analyses)

        if case.case_type == CaseType.CRIMINAL:
            # Higher bar for criminal cases.
            if avg_confidence >= 0.80:
                return Disposition.GUILTY
            return Disposition.NOT_GUILTY

        if avg_confidence >= 0.70:
            return Disposition.GRANTED
        if avg_confidence >= 0.50:
            return Disposition.GRANTED_IN_PART
        if avg_confidence >= 0.30:
            return Disposition.DENIED
        return Disposition.DISMISSED

    @staticmethod
    def _determine_remedy(disposition: Disposition, case: Case) -> RemedyType:
        if disposition in (Disposition.DISMISSED, Disposition.NOT_GUILTY, Disposition.DENIED):
            return RemedyType.NONE

        remedy_map: dict[CaseType, RemedyType] = {
            CaseType.CONTRACT: RemedyType.DAMAGES,
            CaseType.TORT: RemedyType.DAMAGES,
            CaseType.PROPERTY: RemedyType.INJUNCTION,
            CaseType.EMPLOYMENT: RemedyType.DAMAGES,
            CaseType.INTELLECTUAL_PROPERTY: RemedyType.INJUNCTION,
            CaseType.ENVIRONMENTAL: RemedyType.INJUNCTION,
            CaseType.CONSTITUTIONAL: RemedyType.DECLARATORY,
            CaseType.CORPORATE: RemedyType.SPECIFIC_PERFORMANCE,
        }
        return remedy_map.get(case.case_type, RemedyType.DECLARATORY)

    @staticmethod
    def _determine_prevailing_party(
        analyses: list[IRACAnalysis], case: Case
    ) -> str:
        """Determine which party prevails based on evidence balance."""
        party_scores: dict[str, float] = {}
        for evidence in case.get_admissible_evidence():
            party_scores.setdefault(evidence.submitted_by, 0.0)
            party_scores[evidence.submitted_by] += evidence.credibility_weight

        for arg in case.arguments:
            score_bump = 0.0
            score_bump += 0.1 * min(len(arg.supporting_facts), 3)
            score_bump += 0.1 * min(len(arg.legal_basis), 3)
            party_scores.setdefault(arg.party_name, 0.0)
            party_scores[arg.party_name] += score_bump

        if not party_scores:
            # Fall back to first plaintiff/petitioner.
            for p in case.parties:
                if p.role in (PartyRole.PLAINTIFF, PartyRole.PETITIONER, PartyRole.PROSECUTOR):
                    return p.name
            return case.parties[0].name if case.parties else "Unknown"

        return max(party_scores, key=party_scores.get)  # type: ignore[arg-type]

    # ------------------------------------------------------------------
    # Judgment assembly
    # ------------------------------------------------------------------

    def _build_judgment(
        self,
        case: Case,
        analyses: list[IRACAnalysis],
        disposition: Disposition,
        remedy: RemedyType,
        prevailing_party: str,
        dissent: str = "",
    ) -> Judgment:
        avg_confidence = (
            sum(a.confidence for a in analyses) / len(analyses)
            if analyses
            else 0.0
        )
        admissible = case.get_admissible_evidence()
        evidence_strength = (
            sum(e.credibility_weight for e in admissible) / len(admissible)
            if admissible
            else 0.0
        )

        # Build structured sections.
        sections = self._build_sections(case, analyses, disposition, remedy, prevailing_party, dissent)

        # Build summary.
        summary = (
            f"In the matter of {case.title}, this court finds in favor of "
            f"{prevailing_party}. The claim is {disposition.value}."
        )
        if remedy != RemedyType.NONE:
            summary += f" Remedy: {remedy.value}."

        # Assemble analysis text.
        analysis_text = "\n\n".join(a.as_text() for a in analyses)

        # Holding.
        holding = (
            f"This court holds that the {disposition.value} disposition is "
            f"warranted based on the analysis of {len(analyses)} issue(s). "
            f"The prevailing party is {prevailing_party}."
        )

        # Reasoning summary.
        reasoning_parts: list[str] = []
        for a in analyses:
            if a.reasoning_chain:
                reasoning_parts.append(str(a.reasoning_chain))
        reasoning_text = "\n\n".join(reasoning_parts)

        # Remedy details.
        remedy_details = ""
        if remedy != RemedyType.NONE:
            remedy_details = (
                f"The court awards {remedy.value} to {prevailing_party}. "
                f"Specific terms to be determined by further proceedings if necessary."
            )

        return Judgment(
            case_id=case.case_id,
            case_title=case.title,
            disposition=disposition,
            remedy=remedy,
            summary=summary,
            facts_found=case.facts[:],
            issues_addressed=[a.issue for a in analyses],
            rules_applied=self._collect_rules(analyses),
            analysis=analysis_text,
            holding=holding,
            reasoning=reasoning_text,
            remedy_details=remedy_details,
            dissent=dissent,
            confidence=avg_confidence,
            strength_of_evidence=evidence_strength,
            prevailing_party=prevailing_party,
            costs_awarded_to=prevailing_party if disposition == Disposition.GRANTED else "",
            sections=sections,
        )

    @staticmethod
    def _collect_rules(analyses: list[IRACAnalysis]) -> list[str]:
        rules: list[str] = []
        for a in analyses:
            for r in a.rules:
                if r not in rules:
                    rules.append(r)
        return rules

    @staticmethod
    def _build_sections(
        case: Case,
        analyses: list[IRACAnalysis],
        disposition: Disposition,
        remedy: RemedyType,
        prevailing_party: str,
        dissent: str = "",
    ) -> list[JudgmentSection]:
        sections: list[JudgmentSection] = []

        # I. Introduction
        parties_str = ", ".join(str(p) for p in case.parties)
        sections.append(JudgmentSection(
            heading="I. Introduction",
            content=(
                f"This matter comes before the court regarding {case.title}. "
                f"The parties are: {parties_str}. "
                f"Case type: {case.case_type.value}. "
                f"Jurisdiction: {case.jurisdiction}."
            ),
        ))

        # II. Statement of Facts
        if case.facts:
            facts_text = "\n".join(f"  {i+1}. {f}" for i, f in enumerate(case.facts))
            sections.append(JudgmentSection(
                heading="II. Statement of Facts",
                content=f"The court finds the following facts:\n{facts_text}",
            ))

        # III. Issues Presented
        if analyses:
            issues_text = "\n".join(
                f"  {i+1}. {a.issue}" for i, a in enumerate(analyses)
            )
            sections.append(JudgmentSection(
                heading="III. Issues Presented",
                content=f"The following issues are before the court:\n{issues_text}",
            ))

        # IV. Analysis
        for i, analysis in enumerate(analyses, 1):
            sections.append(JudgmentSection(
                heading=f"IV.{i}. Analysis: {analysis.issue}",
                content=analysis.as_text(),
            ))

        # V. Holding
        sections.append(JudgmentSection(
            heading="V. Holding",
            content=(
                f"The court finds in favor of {prevailing_party}. "
                f"Disposition: {disposition.value}."
            ),
        ))

        # VI. Remedy
        if remedy != RemedyType.NONE:
            sections.append(JudgmentSection(
                heading="VI. Remedy",
                content=(
                    f"The court awards {remedy.value} to {prevailing_party}. "
                    f"Specific terms to be determined by further proceedings if necessary."
                ),
            ))

        # VII. Dissent
        if dissent:
            sections.append(JudgmentSection(
                heading="VII. Dissenting Opinion",
                content=dissent,
            ))

        return sections
