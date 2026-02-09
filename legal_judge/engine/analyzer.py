"""IRAC-based legal analysis engine.

IRAC stands for Issue, Rule, Application, Conclusion - the standard
framework taught in law schools for structuring legal analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from legal_judge.engine.precedent import PrecedentMatch, PrecedentMatcher
from legal_judge.engine.reasoning import ReasoningChain, ReasoningType
from legal_judge.models.case import Argument, Case, Evidence
from legal_judge.models.legal import LegalPrinciple, Statute


@dataclass
class IRACAnalysis:
    """A complete IRAC analysis for a single legal issue."""

    issue: str
    rules: list[str] = field(default_factory=list)
    application: str = ""
    conclusion: str = ""
    reasoning_chain: ReasoningChain | None = None
    confidence: float = 0.5
    supporting_precedents: list[PrecedentMatch] = field(default_factory=list)

    def as_text(self) -> str:
        lines = [
            f"ISSUE: {self.issue}",
            "",
            "RULE(S):",
        ]
        for r in self.rules:
            lines.append(f"  - {r}")
        lines += [
            "",
            f"APPLICATION:\n  {self.application}",
            "",
            f"CONCLUSION:\n  {self.conclusion}",
        ]
        if self.supporting_precedents:
            lines.append("\nSUPPORTING PRECEDENTS:")
            for pm in self.supporting_precedents:
                lines.append(f"  - {pm.precedent} (relevance: {pm.relevance_score:.0%})")
        lines.append(f"\nConfidence: {self.confidence:.0%}")
        return "\n".join(lines)


class LegalAnalyzer:
    """Performs structured legal analysis using the IRAC framework."""

    def __init__(
        self,
        statutes: list[Statute] | None = None,
        principles: list[LegalPrinciple] | None = None,
        precedent_matcher: PrecedentMatcher | None = None,
    ) -> None:
        self._statutes = statutes or []
        self._principles = principles or []
        self._precedent_matcher = precedent_matcher or PrecedentMatcher()

    @property
    def precedent_matcher(self) -> PrecedentMatcher:
        return self._precedent_matcher

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_case(self, case: Case) -> list[IRACAnalysis]:
        """Run IRAC analysis on every identified issue in the case."""
        issues = case.issues or self._infer_issues(case)
        relevant_precedents = self._precedent_matcher.find_relevant(case, top_k=10)
        analyses: list[IRACAnalysis] = []
        for issue in issues:
            analysis = self._analyze_issue(
                issue, case, relevant_precedents
            )
            analyses.append(analysis)
        return analyses

    # ------------------------------------------------------------------
    # IRAC steps
    # ------------------------------------------------------------------

    def _analyze_issue(
        self,
        issue: str,
        case: Case,
        precedents: list[PrecedentMatch],
    ) -> IRACAnalysis:
        rules = self._find_rules(issue, case)
        application = self._apply_rules(issue, rules, case)
        chain = self._build_reasoning_chain(issue, rules, case, precedents)
        conclusion = self._draw_conclusion(chain, case)
        issue_precedents = self._filter_precedents_for_issue(issue, precedents)

        return IRACAnalysis(
            issue=issue,
            rules=rules,
            application=application,
            conclusion=conclusion,
            reasoning_chain=chain,
            confidence=chain.overall_confidence,
            supporting_precedents=issue_precedents,
        )

    def _find_rules(self, issue: str, case: Case) -> list[str]:
        """Identify applicable legal rules for an issue."""
        rules: list[str] = []
        issue_lower = issue.lower()

        # Match statutes.
        for statute in self._statutes:
            if self._text_overlaps(issue_lower, statute.summary or statute.name):
                rules.append(f"Statute: {statute}")

        # Match principles.
        for principle in self._principles:
            if self._text_overlaps(issue_lower, principle.description):
                rule_text = f"Principle: {principle.name}"
                if principle.elements:
                    rule_text += f" (elements: {', '.join(principle.elements)})"
                rules.append(rule_text)

        # Also pull from the case's own applicable_statutes field.
        for ref in case.applicable_statutes:
            if ref not in rules:
                rules.append(f"Referenced: {ref}")

        if not rules:
            rules.append("General principles of equity and fairness apply.")

        return rules

    def _apply_rules(
        self, issue: str, rules: list[str], case: Case
    ) -> str:
        """Apply the identified rules to the facts of the case."""
        parts: list[str] = []

        # Evidence assessment.
        admissible = case.get_admissible_evidence()
        if admissible:
            evidence_summary = self._assess_evidence(admissible, issue)
            parts.append(evidence_summary)

        # Argument evaluation.
        for arg in case.arguments:
            strength = self._evaluate_argument(arg, rules)
            parts.append(
                f"Argument by {arg.party_name}: {arg.claim} "
                f"[Strength: {strength}]"
            )

        if not parts:
            parts.append(
                "The available facts and evidence have been considered "
                "in light of the applicable rules."
            )

        return " ".join(parts)

    def _draw_conclusion(self, chain: ReasoningChain, case: Case) -> str:
        """Draw a conclusion from the reasoning chain."""
        if chain.final_conclusion:
            return chain.final_conclusion
        if chain.steps:
            return chain.steps[-1].conclusion
        return "Insufficient basis for a definitive conclusion on this issue."

    # ------------------------------------------------------------------
    # Reasoning chain construction
    # ------------------------------------------------------------------

    def _build_reasoning_chain(
        self,
        issue: str,
        rules: list[str],
        case: Case,
        precedents: list[PrecedentMatch],
    ) -> ReasoningChain:
        chain = ReasoningChain(issue=issue)

        # Step 1: Factual basis (deductive).
        if case.facts:
            chain.add_step(
                reasoning_type=ReasoningType.DEDUCTIVE,
                premise="The following facts are established: " + "; ".join(case.facts[:5]),
                inference="These facts frame the legal question at hand.",
                conclusion=f"The factual basis for '{issue}' is established.",
                confidence=0.85,
            )

        # Step 2: Rule application (deductive).
        if rules:
            chain.add_step(
                reasoning_type=ReasoningType.DEDUCTIVE,
                premise="Applicable rules: " + "; ".join(rules[:3]),
                inference="Applying these rules to the established facts.",
                conclusion="The legal framework for analysis is identified.",
                confidence=0.80,
            )

        # Step 3: Precedent analogy (analogical).
        applicable_prec = [
            p for p in precedents if p.relevance_score >= 0.3
        ]
        if applicable_prec:
            best = applicable_prec[0]
            chain.add_step(
                reasoning_type=ReasoningType.ANALOGICAL,
                premise=f"In {best.precedent.case_name}, the court held: {best.precedent.holding}",
                inference=(
                    f"The current facts are analogous (relevance: {best.relevance_score:.0%}). "
                    f"{best.applicability_note}"
                ),
                conclusion=f"Precedent supports a similar outcome to {best.precedent.case_name}.",
                confidence=0.55 + 0.35 * best.relevance_score,
                supporting_authority=[str(best.precedent)],
            )

        # Step 4: Evidence weighing (balancing).
        admissible = case.get_admissible_evidence()
        if admissible:
            avg_credibility = sum(e.credibility_weight for e in admissible) / len(admissible)
            side_summary = self._summarize_evidence_balance(admissible, case)
            chain.add_step(
                reasoning_type=ReasoningType.BALANCING,
                premise=f"{len(admissible)} admissible items of evidence considered.",
                inference=side_summary,
                conclusion=f"Evidence assessment complete (avg credibility: {avg_credibility:.0%}).",
                confidence=0.5 + 0.4 * avg_credibility,
            )

        # Step 5: Argument balancing.
        if case.arguments:
            arg_summary = self._summarize_arguments(case)
            chain.add_step(
                reasoning_type=ReasoningType.BALANCING,
                premise="Competing arguments from all parties evaluated.",
                inference=arg_summary,
                conclusion="Arguments have been weighed on their merits.",
                confidence=0.70,
            )

        # Finalize.
        conclusion = self._synthesize_conclusion(issue, chain, case)
        chain.finalize(conclusion)
        return chain

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    @staticmethod
    def _text_overlaps(query: str, target: str) -> bool:
        query_words = {w.strip(".,;:!?") for w in query.lower().split() if len(w) > 3}
        target_words = {w.strip(".,;:!?") for w in target.lower().split() if len(w) > 3}
        return bool(query_words & target_words)

    @staticmethod
    def _assess_evidence(evidence: list[Evidence], issue: str) -> str:
        strong = [e for e in evidence if e.credibility_weight >= 0.7]
        moderate = [e for e in evidence if 0.4 <= e.credibility_weight < 0.7]
        weak = [e for e in evidence if e.credibility_weight < 0.4]
        parts: list[str] = []
        if strong:
            parts.append(f"{len(strong)} strong item(s) of evidence")
        if moderate:
            parts.append(f"{len(moderate)} moderate item(s)")
        if weak:
            parts.append(f"{len(weak)} weak item(s)")
        return f"Evidence assessment for '{issue}': {', '.join(parts)}."

    @staticmethod
    def _evaluate_argument(arg: Argument, rules: list[str]) -> str:
        score = 0
        if arg.supporting_facts:
            score += min(len(arg.supporting_facts), 3)
        if arg.legal_basis:
            score += min(len(arg.legal_basis), 3)
        if arg.cited_precedents:
            score += min(len(arg.cited_precedents), 2)
        if score >= 6:
            return "Strong"
        if score >= 3:
            return "Moderate"
        return "Weak"

    @staticmethod
    def _summarize_evidence_balance(
        evidence: list[Evidence], case: Case
    ) -> str:
        party_scores: dict[str, float] = {}
        for e in evidence:
            party_scores.setdefault(e.submitted_by, 0.0)
            party_scores[e.submitted_by] += e.credibility_weight
        if not party_scores:
            return "No evidence to weigh."
        ranked = sorted(party_scores.items(), key=lambda x: x[1], reverse=True)
        parts = [f"{name}: {score:.2f}" for name, score in ranked]
        return "Evidence balance - " + ", ".join(parts) + "."

    @staticmethod
    def _summarize_arguments(case: Case) -> str:
        party_counts: dict[str, int] = {}
        for a in case.arguments:
            party_counts[a.party_name] = party_counts.get(a.party_name, 0) + 1
        parts = [f"{name} ({count} argument(s))" for name, count in party_counts.items()]
        return "Arguments presented by: " + ", ".join(parts) + "."

    def _synthesize_conclusion(
        self, issue: str, chain: ReasoningChain, case: Case
    ) -> str:
        """Synthesize a final conclusion from all reasoning steps."""
        if chain.overall_confidence >= 0.7:
            strength = "On balance, the weight of evidence and law strongly suggests"
        elif chain.overall_confidence >= 0.5:
            strength = "The evidence and applicable law indicate"
        else:
            strength = "While not conclusive, the available evidence suggests"

        return f"{strength} a resolution of the issue: '{issue}'."

    @staticmethod
    def _filter_precedents_for_issue(
        issue: str, precedents: list[PrecedentMatch]
    ) -> list[PrecedentMatch]:
        issue_words = {w.lower().strip(".,;:!?") for w in issue.split() if len(w) > 3}
        filtered: list[PrecedentMatch] = []
        for pm in precedents:
            kw_set = {k.lower() for k in pm.precedent.relevance_keywords}
            if kw_set & issue_words or pm.relevance_score >= 0.4:
                filtered.append(pm)
        return filtered[:3]

    def _infer_issues(self, case: Case) -> list[str]:
        """If no explicit issues are stated, infer them from the arguments."""
        issues: list[str] = []
        for arg in case.arguments:
            issues.append(arg.claim)
        if not issues:
            issues.append(f"General adjudication of {case.case_type.value} matter: {case.title}")
        return issues
