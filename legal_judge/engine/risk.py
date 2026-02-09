"""Risk assessment engine for pre-litigation analysis.

Evaluates each party's litigation position and assigns win probabilities,
identifies strengths and weaknesses, and flags critical risk factors.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from legal_judge.engine.precedent import PrecedentMatcher
from legal_judge.models.case import Argument, Case, Evidence, Party


@dataclass
class PartyRisk:
    """Risk assessment for a single party."""

    party_name: str
    role: str
    win_probability: float = 0.0
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    risk_factors: list[str] = field(default_factory=list)
    evidence_score: float = 0.0
    argument_score: float = 0.0
    overall_grade: str = ""  # A, B, C, D, F


@dataclass
class RiskReport:
    """Complete risk assessment report for all parties."""

    case_id: str
    case_title: str
    party_assessments: list[PartyRisk] = field(default_factory=list)
    litigation_risk_level: str = ""  # low, moderate, high, extreme
    recommendation: str = ""


class RiskAssessor:
    """Evaluates litigation risk for each party in a case."""

    def assess(self, case: Case) -> RiskReport:
        """Generate a risk report for all parties."""
        assessments: list[PartyRisk] = []

        for party in case.parties:
            assessment = self._assess_party(party, case)
            assessments.append(assessment)

        # Normalize win probabilities to sum to ~1.
        total = sum(a.win_probability for a in assessments)
        if total > 0:
            for a in assessments:
                a.win_probability = round(a.win_probability / total, 4)

        # Assign grades.
        for a in assessments:
            a.overall_grade = self._compute_grade(a.win_probability)

        risk_level = self._overall_risk_level(assessments)
        recommendation = self._generate_recommendation(assessments, case)

        return RiskReport(
            case_id=case.case_id,
            case_title=case.title,
            party_assessments=assessments,
            litigation_risk_level=risk_level,
            recommendation=recommendation,
        )

    # ------------------------------------------------------------------
    # Per-party assessment
    # ------------------------------------------------------------------

    def _assess_party(self, party: Party, case: Case) -> PartyRisk:
        party_args = case.get_arguments_by_party(party.name)
        party_evidence = [
            e for e in case.get_admissible_evidence()
            if e.submitted_by == party.name
        ]

        evidence_score = self._score_evidence(party_evidence)
        argument_score = self._score_arguments(party_args)
        strengths = self._identify_strengths(party, party_args, party_evidence, case)
        weaknesses = self._identify_weaknesses(party, party_args, party_evidence, case)
        risk_factors = self._identify_risks(party, party_args, party_evidence, case)

        # Raw win probability before normalization.
        raw_prob = 0.5 * evidence_score + 0.35 * argument_score + 0.15 * (len(strengths) / max(len(strengths) + len(weaknesses), 1))

        return PartyRisk(
            party_name=party.name,
            role=party.role.value,
            win_probability=max(0.05, min(raw_prob, 0.95)),
            strengths=strengths,
            weaknesses=weaknesses,
            risk_factors=risk_factors,
            evidence_score=round(evidence_score, 4),
            argument_score=round(argument_score, 4),
        )

    @staticmethod
    def _score_evidence(evidence: list[Evidence]) -> float:
        if not evidence:
            return 0.1
        total_weight = sum(e.credibility_weight for e in evidence)
        avg = total_weight / len(evidence)
        # Bonus for volume.
        volume_bonus = min(len(evidence) * 0.05, 0.2)
        return min(avg + volume_bonus, 1.0)

    @staticmethod
    def _score_arguments(arguments: list[Argument]) -> float:
        if not arguments:
            return 0.1
        total = 0.0
        for arg in arguments:
            score = 0.0
            score += min(len(arg.supporting_facts), 3) * 0.1
            score += min(len(arg.legal_basis), 3) * 0.15
            score += min(len(arg.cited_precedents), 2) * 0.1
            total += min(score, 1.0)
        return min(total / len(arguments), 1.0)

    @staticmethod
    def _identify_strengths(
        party: Party, args: list[Argument], evidence: list[Evidence], case: Case
    ) -> list[str]:
        strengths: list[str] = []
        strong_evidence = [e for e in evidence if e.credibility_weight >= 0.8]
        if strong_evidence:
            strengths.append(
                f"{len(strong_evidence)} highly credible evidence item(s) "
                f"(avg credibility: {sum(e.credibility_weight for e in strong_evidence) / len(strong_evidence):.0%})"
            )
        for arg in args:
            if len(arg.legal_basis) >= 2:
                strengths.append(f"Well-grounded argument: '{arg.claim[:60]}...' with {len(arg.legal_basis)} legal bases")
            if arg.cited_precedents:
                strengths.append(f"Cites precedent: {', '.join(arg.cited_precedents[:2])}")
        if len(evidence) >= 3:
            strengths.append(f"Strong evidence portfolio ({len(evidence)} items)")
        return strengths[:6]

    @staticmethod
    def _identify_weaknesses(
        party: Party, args: list[Argument], evidence: list[Evidence], case: Case
    ) -> list[str]:
        weaknesses: list[str] = []
        if not evidence:
            weaknesses.append("No evidence submitted")
        weak_evidence = [e for e in evidence if e.credibility_weight < 0.4]
        if weak_evidence:
            weaknesses.append(f"{len(weak_evidence)} low-credibility evidence item(s)")
        if not args:
            weaknesses.append("No arguments presented")
        for arg in args:
            if not arg.legal_basis and not arg.cited_precedents:
                weaknesses.append(f"Unsupported argument: '{arg.claim[:60]}...'")
            if not arg.supporting_facts:
                weaknesses.append(f"Argument lacks factual support: '{arg.claim[:50]}...'")
        # Check for opposing strong arguments.
        other_args = [a for a in case.arguments if a.party_name != party.name]
        strong_opposition = [a for a in other_args if len(a.legal_basis) >= 2 and len(a.supporting_facts) >= 2]
        if strong_opposition:
            weaknesses.append(f"Faces {len(strong_opposition)} well-supported opposing argument(s)")
        return weaknesses[:6]

    @staticmethod
    def _identify_risks(
        party: Party, args: list[Argument], evidence: list[Evidence], case: Case
    ) -> list[str]:
        risks: list[str] = []
        inadmissible = [e for e in case.evidence if e.submitted_by == party.name and not e.admissible]
        if inadmissible:
            risks.append(f"{len(inadmissible)} evidence item(s) ruled inadmissible")
        if len(case.issues) > 3:
            risks.append("Multiple issues increase complexity and unpredictability")
        other_evidence = [e for e in case.get_admissible_evidence() if e.submitted_by != party.name]
        if other_evidence:
            avg_other = sum(e.credibility_weight for e in other_evidence) / len(other_evidence)
            if avg_other >= 0.8:
                risks.append("Opposing party has highly credible evidence")
        return risks[:4]

    @staticmethod
    def _compute_grade(win_prob: float) -> str:
        if win_prob >= 0.75:
            return "A"
        if win_prob >= 0.60:
            return "B"
        if win_prob >= 0.45:
            return "C"
        if win_prob >= 0.30:
            return "D"
        return "F"

    @staticmethod
    def _overall_risk_level(assessments: list[PartyRisk]) -> str:
        if not assessments:
            return "unknown"
        probs = [a.win_probability for a in assessments]
        spread = max(probs) - min(probs)
        if spread < 0.15:
            return "high"  # Very close — unpredictable.
        if spread < 0.30:
            return "moderate"
        if spread < 0.50:
            return "low"
        return "very_low"

    def _generate_recommendation(
        self, assessments: list[PartyRisk], case: Case
    ) -> str:
        if not assessments:
            return "Insufficient information for recommendation."

        sorted_a = sorted(assessments, key=lambda a: a.win_probability, reverse=True)
        leader = sorted_a[0]
        trailer = sorted_a[-1]

        parts: list[str] = []
        parts.append(
            f"Based on pre-trial risk analysis, {leader.party_name} holds "
            f"the stronger position ({leader.win_probability:.0%} estimated win probability, "
            f"grade: {leader.overall_grade})."
        )

        if leader.win_probability - trailer.win_probability < 0.20:
            parts.append(
                "The margin is narrow. Both parties face significant litigation risk. "
                "Settlement negotiations are strongly recommended."
            )
        elif leader.win_probability >= 0.70:
            parts.append(
                f"{trailer.party_name} faces substantial risk of an adverse ruling. "
                f"Early settlement should be seriously considered."
            )
        else:
            parts.append(
                "The outcome is moderately uncertain. Parties should weigh "
                "the cost of litigation against potential settlement."
            )

        return " ".join(parts)
