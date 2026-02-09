"""Tests for the IRAC legal analyzer."""

from legal_judge.engine.analyzer import LegalAnalyzer
from legal_judge.engine.precedent import PrecedentMatcher
from legal_judge.knowledge.domains import get_contract_law, get_tort_law
from legal_judge.models.case import (
    Argument,
    Case,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)


def _make_analyzer() -> LegalAnalyzer:
    contract_s, contract_p, contract_pr = get_contract_law()
    tort_s, tort_p, tort_pr = get_tort_law()
    matcher = PrecedentMatcher(contract_p + tort_p)
    return LegalAnalyzer(
        statutes=contract_s + tort_s,
        principles=contract_pr + tort_pr,
        precedent_matcher=matcher,
    )


def _make_contract_case() -> Case:
    return Case(
        case_id="A-001",
        title="Seller v. Buyer",
        case_type=CaseType.CONTRACT,
        parties=[
            Party(name="Seller", role=PartyRole.PLAINTIFF),
            Party(name="Buyer", role=PartyRole.DEFENDANT),
        ],
        facts=[
            "Parties entered a contract for sale of goods.",
            "Buyer failed to pay upon delivery.",
            "Seller suffered losses.",
        ],
        issues=[
            "Whether Buyer breached the contract by failing to pay",
        ],
        arguments=[
            Argument(
                party_name="Seller",
                claim="Buyer breached the contract by failing to pay.",
                supporting_facts=["Non-payment after delivery"],
                legal_basis=["UCC Article 2", "Breach of contract"],
                cited_precedents=["Hadley v. Baxendale"],
            ),
            Argument(
                party_name="Buyer",
                claim="Goods were defective, excusing payment.",
                supporting_facts=["Quality issues noted"],
            ),
        ],
        evidence=[
            Evidence(
                title="Invoice",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Invoice for delivered goods.",
                submitted_by="Seller",
                credibility_weight=0.9,
            ),
        ],
        applicable_statutes=["UCC Article 2"],
    )


def test_analyzer_produces_irac():
    analyzer = _make_analyzer()
    case = _make_contract_case()
    results = analyzer.analyze_case(case)
    assert len(results) == 1
    analysis = results[0]
    assert analysis.issue != ""
    assert len(analysis.rules) > 0
    assert analysis.application != ""
    assert analysis.conclusion != ""
    assert 0.0 <= analysis.confidence <= 1.0


def test_analyzer_infers_issues():
    analyzer = _make_analyzer()
    case = Case(
        case_id="A-002",
        title="X v. Y",
        case_type=CaseType.CONTRACT,
        arguments=[
            Argument(party_name="X", claim="Y breached contract."),
        ],
    )
    results = analyzer.analyze_case(case)
    assert len(results) >= 1
    assert "breached" in results[0].issue.lower()


def test_analyzer_handles_no_evidence():
    analyzer = _make_analyzer()
    case = Case(
        case_id="A-003",
        title="P v. Q",
        case_type=CaseType.CONTRACT,
        facts=["Contract existed."],
        issues=["Whether contract was valid"],
    )
    results = analyzer.analyze_case(case)
    assert len(results) == 1
    assert results[0].conclusion != ""


def test_analyzer_includes_precedents():
    analyzer = _make_analyzer()
    case = _make_contract_case()
    results = analyzer.analyze_case(case)
    analysis = results[0]
    if analysis.reasoning_chain:
        has_analogical = any(
            step.reasoning_type.value == "analogical"
            for step in analysis.reasoning_chain.steps
        )
        # Should find analogical steps when precedents are available.
        assert has_analogical


def test_analysis_as_text():
    analyzer = _make_analyzer()
    case = _make_contract_case()
    results = analyzer.analyze_case(case)
    text = results[0].as_text()
    assert "ISSUE:" in text
    assert "RULE" in text
    assert "APPLICATION:" in text
    assert "CONCLUSION:" in text
