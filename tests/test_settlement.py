"""Tests for the settlement calculator."""

from legal_judge.engine.settlement import (
    DamagesEstimate,
    SettlementCalculator,
    SettlementRange,
    SettlementReport,
)
from legal_judge.models.case import (
    Argument,
    Case,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)


def _make_tort_case() -> Case:
    return Case(
        case_id="SETTLE-001",
        title="Settler v. Defender",
        case_type=CaseType.TORT,
        parties=[
            Party(name="Settler", role=PartyRole.PLAINTIFF),
            Party(name="Defender", role=PartyRole.DEFENDANT),
        ],
        facts=[
            "Defender acted negligently.",
            "Settler suffered personal injury.",
            "Medical bills totaled $50000.",
            "Settler missed work for 3 months.",
        ],
        issues=["Whether Defender was negligent", "Damages amount"],
        arguments=[
            Argument(
                party_name="Settler",
                claim="Defender was negligent.",
                supporting_facts=["Ran red light", "Caused collision"],
                legal_basis=["Duty of care", "Negligence"],
            ),
            Argument(
                party_name="Defender",
                claim="Settler was contributorily negligent.",
                supporting_facts=["Settler was speeding"],
            ),
        ],
        evidence=[
            Evidence(
                title="Medical records",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Shows injuries and bills.",
                submitted_by="Settler",
                credibility_weight=0.9,
            ),
            Evidence(
                title="Police report",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Report of the accident.",
                submitted_by="Settler",
                credibility_weight=0.85,
            ),
        ],
    )


def test_settlement_report_structure():
    calc = SettlementCalculator()
    case = _make_tort_case()
    report = calc.analyze(case)

    assert isinstance(report, SettlementReport)
    assert report.case_id == "SETTLE-001"
    assert report.case_title == "Settler v. Defender"
    assert isinstance(report.damages_estimate, DamagesEstimate)
    assert isinstance(report.settlement_range, SettlementRange)
    assert report.settlement_recommendation != ""
    assert report.cost_of_litigation_estimate > 0


def test_damages_include_punitive_for_tort():
    calc = SettlementCalculator()
    case = _make_tort_case()
    report = calc.analyze(case)
    assert report.damages_estimate.punitive > 0


def test_damages_no_punitive_for_contract():
    calc = SettlementCalculator()
    case = Case(
        case_id="S-002",
        title="A v. B",
        case_type=CaseType.CONTRACT,
        parties=[
            Party(name="A", role=PartyRole.PLAINTIFF),
            Party(name="B", role=PartyRole.DEFENDANT),
        ],
        facts=["Contract breach."],
        issues=["Whether breach occurred"],
        arguments=[
            Argument(party_name="A", claim="B breached.", supporting_facts=["Late delivery"]),
        ],
    )
    report = calc.analyze(case)
    assert report.damages_estimate.punitive == 0


def test_claimed_damages_used():
    calc = SettlementCalculator()
    case = _make_tort_case()
    report = calc.analyze(case, claimed_damages=500_000)
    # Compensatory should be based on claimed * credibility.
    assert report.damages_estimate.compensatory > 0
    assert report.damages_estimate.total > 0


def test_settlement_range_order():
    calc = SettlementCalculator()
    case = _make_tort_case()
    report = calc.analyze(case)
    s = report.settlement_range
    assert s.low <= s.midpoint <= s.high
    assert s.low <= s.recommended <= s.high


def test_litigation_cost_scales_with_complexity():
    calc = SettlementCalculator()
    simple = Case(
        case_id="SIMPLE",
        title="Simple",
        case_type=CaseType.CIVIL,
        issues=["One issue"],
    )
    complex_case = _make_tort_case()
    simple_report = calc.analyze(simple)
    complex_report = calc.analyze(complex_case)
    assert complex_report.cost_of_litigation_estimate > simple_report.cost_of_litigation_estimate


def test_should_settle_flag():
    calc = SettlementCalculator()
    case = _make_tort_case()
    report = calc.analyze(case)
    assert isinstance(report.should_settle, bool)


def test_settlement_infers_damages_from_facts():
    calc = SettlementCalculator()
    case = _make_tort_case()
    # Case has "$50000" in facts.
    report = calc.analyze(case)
    assert report.damages_estimate.total > 0


def test_damages_basis_populated():
    calc = SettlementCalculator()
    case = _make_tort_case()
    report = calc.analyze(case)
    assert len(report.damages_estimate.basis) > 0
