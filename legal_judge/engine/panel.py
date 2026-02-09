"""Multi-judge panel with distinct judicial philosophies.

Simulates a panel of judges who independently analyze a case through
different interpretive lenses and then produce a majority opinion,
concurrences, and dissents — just like a real appellate court.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel, Field

from legal_judge.engine.analyzer import IRACAnalysis, LegalAnalyzer
from legal_judge.engine.precedent import PrecedentMatcher
from legal_judge.models.case import Case, CaseType
from legal_judge.models.judgment import Disposition, Judgment, RemedyType
from legal_judge.models.legal import LegalPrinciple, Precedent, Statute


class JudicialPhilosophy(str, Enum):
    TEXTUALIST = "textualist"
    PRAGMATIST = "pragmatist"
    ORIGINALIST = "originalist"


# Weights each philosophy applies to the scoring factors.
# (evidence_weight, precedent_weight, policy_weight, textual_weight)
_PHILOSOPHY_WEIGHTS: dict[JudicialPhilosophy, tuple[float, float, float, float]] = {
    JudicialPhilosophy.TEXTUALIST:  (0.25, 0.20, 0.05, 0.50),
    JudicialPhilosophy.PRAGMATIST:  (0.30, 0.25, 0.30, 0.15),
    JudicialPhilosophy.ORIGINALIST: (0.20, 0.40, 0.05, 0.35),
}

_PHILOSOPHY_LABELS: dict[JudicialPhilosophy, str] = {
    JudicialPhilosophy.TEXTUALIST:  "Hon. Justice Clarke (Textualist)",
    JudicialPhilosophy.PRAGMATIST:  "Hon. Justice Okafor (Pragmatist)",
    JudicialPhilosophy.ORIGINALIST: "Hon. Justice Whitfield (Originalist)",
}

_PHILOSOPHY_DESCRIPTIONS: dict[JudicialPhilosophy, str] = {
    JudicialPhilosophy.TEXTUALIST: (
        "Focuses strictly on the plain text of statutes and contractual language. "
        "Gives less weight to policy arguments and more to what the words actually say."
    ),
    JudicialPhilosophy.PRAGMATIST: (
        "Considers practical consequences and real-world impact alongside legal text. "
        "Weighs policy considerations and the interests of justice more heavily."
    ),
    JudicialPhilosophy.ORIGINALIST: (
        "Emphasizes the original meaning of legal texts and strong adherence to precedent. "
        "Gives great deference to established case law and historical interpretation."
    ),
}


@dataclass
class JudgeOpinion:
    """One judge's independent opinion on a case."""

    judge_name: str
    philosophy: JudicialPhilosophy
    philosophy_description: str
    disposition: Disposition
    confidence: float
    reasoning_summary: str
    key_factors: list[str] = field(default_factory=list)
    cited_precedents: list[str] = field(default_factory=list)
    agrees_with_majority: bool = True


class PanelDecision(BaseModel):
    """The collective decision of a multi-judge panel."""

    case_id: str
    case_title: str
    panel_size: int = 3
    majority_disposition: Disposition
    majority_vote: str = ""
    is_unanimous: bool = False
    majority_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    majority_opinion: str = ""
    opinions: list[dict] = Field(default_factory=list)
    # Full judgment from the majority reasoning.
    judgment: Judgment | None = None


class JudicialPanel:
    """A panel of judges with different philosophies who independently decide."""

    def __init__(
        self,
        statutes: list[Statute] | None = None,
        principles: list[LegalPrinciple] | None = None,
        precedents: list[Precedent] | None = None,
        philosophies: list[JudicialPhilosophy] | None = None,
    ) -> None:
        self._statutes = statutes or []
        self._principles = principles or []
        self._precedents = precedents or []
        self._philosophies = philosophies or [
            JudicialPhilosophy.TEXTUALIST,
            JudicialPhilosophy.PRAGMATIST,
            JudicialPhilosophy.ORIGINALIST,
        ]

    def decide(self, case: Case) -> PanelDecision:
        """Each judge independently analyzes; then votes are tallied."""
        opinions: list[JudgeOpinion] = []

        for philosophy in self._philosophies:
            opinion = self._judge_with_philosophy(case, philosophy)
            opinions.append(opinion)

        # Tally votes.
        disposition_votes: dict[Disposition, list[JudgeOpinion]] = {}
        for op in opinions:
            disposition_votes.setdefault(op.disposition, []).append(op)

        majority_disp = max(disposition_votes, key=lambda d: len(disposition_votes[d]))
        majority_opinions = disposition_votes[majority_disp]
        minority_opinions = [op for op in opinions if op.disposition != majority_disp]

        for op in opinions:
            op.agrees_with_majority = (op.disposition == majority_disp)

        is_unanimous = len(majority_opinions) == len(opinions)
        majority_conf = sum(o.confidence for o in majority_opinions) / len(majority_opinions)

        # Build the full judgment using the majority's average confidence.
        from legal_judge.engine.judge import JudgeEngine
        engine = JudgeEngine(
            statutes=self._statutes,
            principles=self._principles,
            precedents=self._precedents,
        )
        judgment = engine.adjudicate(case)

        # Build the vote string.
        vote_str = f"{len(majority_opinions)}-{len(minority_opinions)}"

        # Majority opinion text.
        majority_text = self._write_majority_opinion(
            case, majority_disp, majority_opinions, minority_opinions
        )

        return PanelDecision(
            case_id=case.case_id,
            case_title=case.title,
            panel_size=len(opinions),
            majority_disposition=majority_disp,
            majority_vote=vote_str,
            is_unanimous=is_unanimous,
            majority_confidence=round(majority_conf, 4),
            majority_opinion=majority_text,
            opinions=[self._opinion_to_dict(op) for op in opinions],
            judgment=judgment,
        )

    # ------------------------------------------------------------------
    # Internal: per-judge analysis
    # ------------------------------------------------------------------

    def _judge_with_philosophy(
        self, case: Case, philosophy: JudicialPhilosophy
    ) -> JudgeOpinion:
        matcher = PrecedentMatcher(self._precedents)
        analyzer = LegalAnalyzer(
            statutes=self._statutes,
            principles=self._principles,
            precedent_matcher=matcher,
        )
        analyses = analyzer.analyze_case(case)

        if not analyses:
            return JudgeOpinion(
                judge_name=_PHILOSOPHY_LABELS[philosophy],
                philosophy=philosophy,
                philosophy_description=_PHILOSOPHY_DESCRIPTIONS[philosophy],
                disposition=Disposition.DISMISSED,
                confidence=0.0,
                reasoning_summary="No issues to analyze; case dismissed.",
            )

        # Apply philosophy-specific weighting.
        ev_w, prec_w, pol_w, text_w = _PHILOSOPHY_WEIGHTS[philosophy]

        # Compute weighted confidence per analysis.
        adjusted_confidences: list[float] = []
        for analysis in analyses:
            base = analysis.confidence

            # Evidence factor.
            admissible = case.get_admissible_evidence()
            ev_score = (
                sum(e.credibility_weight for e in admissible) / len(admissible)
                if admissible else 0.3
            )

            # Precedent factor.
            prec_score = (
                max((p.relevance_score for p in analysis.supporting_precedents), default=0.3)
            )

            # Policy factor: pragmatists boost when strong arguments exist.
            arg_count = len(case.arguments)
            fact_count = len(case.facts)
            pol_score = min((arg_count * 0.15 + fact_count * 0.1), 1.0)

            # Textual factor: textualists boost when statutes are cited.
            statute_count = len(case.applicable_statutes) + len(analysis.rules)
            text_score = min(statute_count * 0.15, 1.0)

            weighted = (
                ev_w * ev_score
                + prec_w * prec_score
                + pol_w * pol_score
                + text_w * text_score
            )
            # Blend with base confidence.
            adjusted = 0.5 * base + 0.5 * weighted
            adjusted_confidences.append(max(0.0, min(adjusted, 1.0)))

        avg_conf = sum(adjusted_confidences) / len(adjusted_confidences)

        # Determine disposition for this judge.
        disposition = self._disposition_for_confidence(avg_conf, case)

        # Collect key factors and precedents.
        key_factors = self._extract_key_factors(analyses, philosophy)
        cited = []
        for a in analyses:
            for pm in a.supporting_precedents:
                cited.append(f"{pm.precedent.case_name} ({pm.precedent.citation})")

        reasoning = self._write_individual_reasoning(
            philosophy, analyses, avg_conf, case
        )

        return JudgeOpinion(
            judge_name=_PHILOSOPHY_LABELS[philosophy],
            philosophy=philosophy,
            philosophy_description=_PHILOSOPHY_DESCRIPTIONS[philosophy],
            disposition=disposition,
            confidence=round(avg_conf, 4),
            reasoning_summary=reasoning,
            key_factors=key_factors,
            cited_precedents=list(dict.fromkeys(cited))[:5],
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _disposition_for_confidence(conf: float, case: Case) -> Disposition:
        if case.case_type == CaseType.CRIMINAL:
            return Disposition.GUILTY if conf >= 0.80 else Disposition.NOT_GUILTY
        if conf >= 0.68:
            return Disposition.GRANTED
        if conf >= 0.48:
            return Disposition.GRANTED_IN_PART
        if conf >= 0.28:
            return Disposition.DENIED
        return Disposition.DISMISSED

    @staticmethod
    def _extract_key_factors(
        analyses: list[IRACAnalysis], philosophy: JudicialPhilosophy
    ) -> list[str]:
        factors: list[str] = []
        if philosophy == JudicialPhilosophy.TEXTUALIST:
            for a in analyses:
                for r in a.rules:
                    if "statute" in r.lower() or "referenced" in r.lower():
                        factors.append(f"Statutory basis: {r}")
        elif philosophy == JudicialPhilosophy.ORIGINALIST:
            for a in analyses:
                for pm in a.supporting_precedents:
                    factors.append(
                        f"Precedent: {pm.precedent.case_name} "
                        f"(authority: {pm.precedent.authority_weight:.0%})"
                    )
        else:  # pragmatist
            for a in analyses:
                factors.append(f"Issue outcome: {a.conclusion[:100]}")
        return factors[:5]

    @staticmethod
    def _write_individual_reasoning(
        philosophy: JudicialPhilosophy,
        analyses: list[IRACAnalysis],
        confidence: float,
        case: Case,
    ) -> str:
        label = _PHILOSOPHY_LABELS[philosophy]
        parts: list[str] = [f"{label} writes:"]

        if philosophy == JudicialPhilosophy.TEXTUALIST:
            parts.append(
                "Applying a strict textual analysis to the applicable statutes "
                "and contractual language, the plain meaning of the operative "
                "provisions yields a clear result."
            )
        elif philosophy == JudicialPhilosophy.ORIGINALIST:
            parts.append(
                "Guided by established precedent and the original understanding "
                "of the applicable legal principles, the court finds the weight "
                "of authority supports the following disposition."
            )
        else:
            parts.append(
                "Considering the practical consequences, the interests of "
                "justice, and the real-world impact on the parties, the court "
                "finds that the equities favor the following result."
            )

        for a in analyses:
            parts.append(
                f"On the issue of '{a.issue}': confidence {a.confidence:.0%}."
            )

        parts.append(f"Overall judicial confidence: {confidence:.0%}.")
        return "\n".join(parts)

    @staticmethod
    def _write_majority_opinion(
        case: Case,
        disposition: Disposition,
        majority: list[JudgeOpinion],
        minority: list[JudgeOpinion],
    ) -> str:
        parts: list[str] = []
        majority_names = ", ".join(o.judge_name for o in majority)
        parts.append(
            f"MAJORITY OPINION ({len(majority)}-{len(minority)}) "
            f"delivered by the panel:\n"
        )
        parts.append(f"Joined by: {majority_names}\n")
        parts.append(
            f"In the matter of {case.title}, the majority of this panel "
            f"finds that the appropriate disposition is: {disposition.value}.\n"
        )

        for op in majority:
            parts.append(f"--- {op.judge_name} ---")
            parts.append(op.reasoning_summary)
            parts.append("")

        if minority:
            parts.append("DISSENTING OPINION(S):\n")
            for op in minority:
                parts.append(f"--- {op.judge_name} (dissenting) ---")
                parts.append(
                    f"The undersigned respectfully dissents. This case warrants "
                    f"a disposition of {op.disposition.value} "
                    f"(confidence: {op.confidence:.0%})."
                )
                parts.append(op.reasoning_summary)
                parts.append("")

        return "\n".join(parts)

    @staticmethod
    def _opinion_to_dict(op: JudgeOpinion) -> dict:
        return {
            "judge_name": op.judge_name,
            "philosophy": op.philosophy.value,
            "philosophy_description": op.philosophy_description,
            "disposition": op.disposition.value,
            "confidence": op.confidence,
            "reasoning_summary": op.reasoning_summary,
            "key_factors": op.key_factors,
            "cited_precedents": op.cited_precedents,
            "agrees_with_majority": op.agrees_with_majority,
        }
