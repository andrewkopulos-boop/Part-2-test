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

    @property
    def analyzer(self) -> LegalAnalyzer:
        return self._analyzer

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
        judgment = self._build_judgment(
            case, analyses, disposition, remedy, prevailing
        )
        case.status = CaseStatus.DECIDED
        return judgment

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
        sections = self._build_sections(case, analyses, disposition, remedy, prevailing_party)

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

        return sections
