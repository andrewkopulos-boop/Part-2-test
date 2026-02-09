"""Settlement recommendation and damages calculator.

Uses risk assessment data to compute optimal settlement ranges
and estimate expected damages.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from legal_judge.engine.risk import PartyRisk, RiskAssessor, RiskReport
from legal_judge.models.case import Case, CaseType


@dataclass
class DamagesEstimate:
    """Estimated damages breakdown."""

    compensatory: float = 0.0
    consequential: float = 0.0
    punitive: float = 0.0
    total: float = 0.0
    confidence: float = 0.0
    basis: list[str] = field(default_factory=list)


@dataclass
class SettlementRange:
    """Recommended settlement range."""

    low: float = 0.0
    midpoint: float = 0.0
    high: float = 0.0
    recommended: float = 0.0
    rationale: str = ""


@dataclass
class SettlementReport:
    """Complete settlement analysis."""

    case_id: str
    case_title: str
    risk_report: RiskReport
    damages_estimate: DamagesEstimate
    settlement_range: SettlementRange
    should_settle: bool = False
    settlement_recommendation: str = ""
    cost_of_litigation_estimate: float = 0.0


class SettlementCalculator:
    """Computes settlement recommendations based on risk and damages."""

    def __init__(self) -> None:
        self._risk_assessor = RiskAssessor()

    def analyze(self, case: Case, claimed_damages: float = 0.0) -> SettlementReport:
        """Generate a full settlement analysis for a case."""
        risk_report = self._risk_assessor.assess(case)
        damages = self._estimate_damages(case, claimed_damages, risk_report)
        litigation_cost = self._estimate_litigation_cost(case)
        settlement = self._compute_settlement_range(damages, risk_report, litigation_cost)
        should_settle = self._should_settle(risk_report, damages, litigation_cost)
        recommendation = self._generate_recommendation(
            risk_report, damages, settlement, litigation_cost, should_settle
        )

        return SettlementReport(
            case_id=case.case_id,
            case_title=case.title,
            risk_report=risk_report,
            damages_estimate=damages,
            settlement_range=settlement,
            should_settle=should_settle,
            settlement_recommendation=recommendation,
            cost_of_litigation_estimate=litigation_cost,
        )

    # ------------------------------------------------------------------
    # Damages estimation
    # ------------------------------------------------------------------

    def _estimate_damages(
        self, case: Case, claimed: float, risk: RiskReport
    ) -> DamagesEstimate:
        """Estimate damages from case facts and claimed amount."""
        basis: list[str] = []

        if claimed <= 0:
            claimed = self._infer_damages_from_facts(case)
            if claimed > 0:
                basis.append(f"Inferred from case facts: ${claimed:,.0f}")

        # Evidence credibility discount.
        admissible = case.get_admissible_evidence()
        if admissible:
            avg_cred = sum(e.credibility_weight for e in admissible) / len(admissible)
        else:
            avg_cred = 0.3
        basis.append(f"Evidence credibility factor: {avg_cred:.0%}")

        compensatory = claimed * avg_cred
        basis.append(f"Compensatory (claimed x credibility): ${compensatory:,.0f}")

        # Consequential damages: fraction based on case complexity.
        consequential = 0.0
        if len(case.facts) >= 4 and len(case.arguments) >= 2:
            consequential = compensatory * 0.25
            basis.append(f"Consequential damages (25% of compensatory): ${consequential:,.0f}")

        # Punitive damages: only for torts and intentional wrongs.
        punitive = 0.0
        if case.case_type in (CaseType.TORT, CaseType.CRIMINAL):
            punitive = compensatory * 0.5
            basis.append(f"Punitive damages (50% of compensatory): ${punitive:,.0f}")

        total = compensatory + consequential + punitive
        # Win probability adjustment.
        plaintiff_risk = None
        for pa in risk.party_assessments:
            if pa.role in ("plaintiff", "petitioner", "prosecutor"):
                plaintiff_risk = pa
                break
        if plaintiff_risk:
            expected_value = total * plaintiff_risk.win_probability
            basis.append(
                f"Expected value (total x {plaintiff_risk.win_probability:.0%} win prob): "
                f"${expected_value:,.0f}"
            )
        else:
            expected_value = total * 0.5

        return DamagesEstimate(
            compensatory=round(compensatory, 2),
            consequential=round(consequential, 2),
            punitive=round(punitive, 2),
            total=round(total, 2),
            confidence=round(avg_cred, 4),
            basis=basis,
        )

    @staticmethod
    def _infer_damages_from_facts(case: Case) -> float:
        """Try to extract dollar amounts from case facts."""
        import re
        for fact in case.facts:
            match = re.search(r'\$[\d,]+(?:\.\d{2})?', fact.replace(',', ''))
            if match:
                try:
                    return float(match.group().replace('$', '').replace(',', ''))
                except ValueError:
                    continue
        # Default heuristic based on case type.
        defaults: dict[CaseType, float] = {
            CaseType.CONTRACT: 100_000,
            CaseType.TORT: 250_000,
            CaseType.EMPLOYMENT: 150_000,
            CaseType.INTELLECTUAL_PROPERTY: 500_000,
            CaseType.PROPERTY: 200_000,
            CaseType.CORPORATE: 1_000_000,
        }
        return defaults.get(case.case_type, 100_000)

    @staticmethod
    def _estimate_litigation_cost(case: Case) -> float:
        """Rough estimate of litigation costs based on complexity."""
        base = 25_000
        base += len(case.issues) * 10_000
        base += len(case.arguments) * 5_000
        base += len(case.evidence) * 2_000
        base += len(case.parties) * 5_000
        return float(base)

    # ------------------------------------------------------------------
    # Settlement computation
    # ------------------------------------------------------------------

    def _compute_settlement_range(
        self,
        damages: DamagesEstimate,
        risk: RiskReport,
        litigation_cost: float,
    ) -> SettlementRange:
        """Compute a settlement range based on expected value and risk."""
        plaintiff_prob = 0.5
        defendant_prob = 0.5
        for pa in risk.party_assessments:
            if pa.role in ("plaintiff", "petitioner", "prosecutor"):
                plaintiff_prob = pa.win_probability
            elif pa.role in ("defendant", "respondent", "appellee"):
                defendant_prob = pa.win_probability

        # Low: what defendant would pay (their risk * damages - their litigation savings).
        low = damages.total * plaintiff_prob - litigation_cost * 0.5
        low = max(low, 0)

        # High: what plaintiff would accept (damages * their win prob + saved litigation costs).
        high = damages.total * plaintiff_prob + litigation_cost * 0.3

        midpoint = (low + high) / 2
        recommended = midpoint

        rationale = (
            f"Settlement range computed based on ${damages.total:,.0f} estimated total damages, "
            f"{plaintiff_prob:.0%} plaintiff win probability, and "
            f"${litigation_cost:,.0f} estimated litigation costs. "
            f"The midpoint of ${midpoint:,.0f} represents the zone of mutual benefit."
        )

        return SettlementRange(
            low=round(low, 2),
            midpoint=round(midpoint, 2),
            high=round(high, 2),
            recommended=round(recommended, 2),
            rationale=rationale,
        )

    @staticmethod
    def _should_settle(
        risk: RiskReport, damages: DamagesEstimate, litigation_cost: float
    ) -> bool:
        """Determine whether settlement is advisable."""
        if risk.litigation_risk_level in ("high", "moderate"):
            return True
        if litigation_cost > damages.total * 0.3:
            return True
        return False

    @staticmethod
    def _generate_recommendation(
        risk: RiskReport,
        damages: DamagesEstimate,
        settlement: SettlementRange,
        litigation_cost: float,
        should_settle: bool,
    ) -> str:
        parts: list[str] = []
        if should_settle:
            parts.append(
                "RECOMMENDATION: Settlement is strongly advisable. "
            )
            parts.append(
                f"Estimated litigation costs (${litigation_cost:,.0f}) represent "
                f"a significant expenditure relative to the dispute value. "
            )
            parts.append(
                f"A settlement in the range of ${settlement.low:,.0f} to "
                f"${settlement.high:,.0f} (recommended: ${settlement.recommended:,.0f}) "
                f"would serve both parties' interests."
            )
        else:
            parts.append(
                "RECOMMENDATION: Proceeding to trial may be warranted given "
                "the strength of the prevailing party's position. "
            )
            parts.append(
                f"However, a settlement offer of ${settlement.recommended:,.0f} "
                f"may still be worth exploring to avoid litigation risk."
            )
        return " ".join(parts)
