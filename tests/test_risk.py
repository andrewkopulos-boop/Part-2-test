"""Tests for the risk assessment engine."""

from legal_judge.engine.risk import PartyRisk, RiskAssessor, RiskReport
from legal_judge.models.case import (
    Argument,
    Case,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)


def _make_case_with_evidence() -> Case:
    return Case(
        case_id="RISK-001",
        title="Risk v. Test",
        case_type=CaseType.CONTRACT,
        parties=[
            Party(name="Plaintiff", role=PartyRole.PLAINTIFF),
            Party(name="Defendant", role=PartyRole.DEFENDANT),
        ],
        facts=[
            "Contract was signed.",
            "Defendant breached terms.",
            "Plaintiff suffered loss.",
        ],
        issues=["Whether breach occurred"],
        arguments=[
            Argument(
                party_name="Plaintiff",
                claim="Defendant breached the contract.",
                supporting_facts=["Late delivery", "No notice"],
                legal_basis=["Breach of contract", "UCC"],
                cited_precedents=["Hadley v. Baxendale"],
            ),
            Argument(
                party_name="Defendant",
                claim="Performance was excused.",
                supporting_facts=["Supply issues"],
            ),
        ],
        evidence=[
            Evidence(
                title="Contract",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Signed contract.",
                submitted_by="Plaintiff",
                credibility_weight=0.9,
            ),
            Evidence(
                title="Delivery log",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Shows no delivery.",
                submitted_by="Plaintiff",
                credibility_weight=0.85,
            ),
            Evidence(
                title="Excuse letter",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Claims force majeure.",
                submitted_by="Defendant",
                credibility_weight=0.4,
            ),
        ],
    )


def test_risk_report_structure():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    assert isinstance(report, RiskReport)
    assert report.case_id == "RISK-001"
    assert report.case_title == "Risk v. Test"
    assert len(report.party_assessments) == 2
    assert report.litigation_risk_level in ("low", "moderate", "high", "very_low", "unknown")
    assert report.recommendation != ""


def test_win_probabilities_sum_to_one():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    total = sum(pa.win_probability for pa in report.party_assessments)
    assert abs(total - 1.0) < 0.01


def test_party_risk_has_grade():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    for pa in report.party_assessments:
        assert pa.overall_grade in ("A", "B", "C", "D", "F")


def test_stronger_party_has_higher_probability():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    plaintiff = next(pa for pa in report.party_assessments if pa.party_name == "Plaintiff")
    defendant = next(pa for pa in report.party_assessments if pa.party_name == "Defendant")
    # Plaintiff has stronger evidence and arguments.
    assert plaintiff.win_probability > defendant.win_probability


def test_strengths_identified():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    plaintiff = next(pa for pa in report.party_assessments if pa.party_name == "Plaintiff")
    assert len(plaintiff.strengths) > 0


def test_weaknesses_identified():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    defendant = next(pa for pa in report.party_assessments if pa.party_name == "Defendant")
    assert len(defendant.weaknesses) > 0


def test_evidence_score_range():
    assessor = RiskAssessor()
    case = _make_case_with_evidence()
    report = assessor.assess(case)

    for pa in report.party_assessments:
        assert 0.0 <= pa.evidence_score <= 1.0
        assert 0.0 <= pa.argument_score <= 1.0


def test_risk_empty_case():
    assessor = RiskAssessor()
    case = Case(
        case_id="EMPTY",
        title="Empty v. Nothing",
        case_type=CaseType.CIVIL,
    )
    report = assessor.assess(case)
    assert report.case_id == "EMPTY"
    assert len(report.party_assessments) == 0
