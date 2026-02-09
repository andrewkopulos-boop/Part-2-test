"""Tests for the multi-judge panel."""

from legal_judge.engine.panel import JudicialPanel, JudicialPhilosophy, PanelDecision
from legal_judge.knowledge.base import KnowledgeBase
from legal_judge.models.case import (
    Argument,
    Case,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)
from legal_judge.models.judgment import Disposition


def _make_contract_case() -> Case:
    return Case(
        case_id="PANEL-001",
        title="Alpha v. Beta",
        case_type=CaseType.CONTRACT,
        parties=[
            Party(name="Alpha", role=PartyRole.PLAINTIFF),
            Party(name="Beta", role=PartyRole.DEFENDANT),
        ],
        facts=[
            "Alpha and Beta entered into a contract.",
            "Beta failed to deliver goods on time.",
            "Alpha suffered financial loss.",
        ],
        issues=[
            "Whether Beta breached the contract",
            "Whether Alpha is entitled to damages",
        ],
        arguments=[
            Argument(
                party_name="Alpha",
                claim="Beta breached the contract.",
                supporting_facts=["Late delivery", "No excuse"],
                legal_basis=["Breach of contract"],
                cited_precedents=["Hadley v. Baxendale"],
            ),
            Argument(
                party_name="Beta",
                claim="Performance was excused.",
                supporting_facts=["Supply issues"],
            ),
        ],
        evidence=[
            Evidence(
                title="Contract",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Signed contract.",
                submitted_by="Alpha",
                credibility_weight=0.9,
            ),
        ],
        applicable_statutes=["UCC Article 2"],
    )


def test_panel_returns_decision():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = _make_contract_case()
    decision = panel.decide(case)

    assert isinstance(decision, PanelDecision)
    assert decision.case_id == "PANEL-001"
    assert decision.panel_size == 3
    assert decision.majority_disposition in list(Disposition)
    assert decision.majority_vote != ""
    assert 0.0 <= decision.majority_confidence <= 1.0
    assert decision.majority_opinion != ""


def test_panel_has_three_opinions():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = _make_contract_case()
    decision = panel.decide(case)

    assert len(decision.opinions) == 3
    philosophies = {op["philosophy"] for op in decision.opinions}
    assert philosophies == {"textualist", "pragmatist", "originalist"}


def test_panel_opinion_fields():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = _make_contract_case()
    decision = panel.decide(case)

    for op in decision.opinions:
        assert "judge_name" in op
        assert "philosophy" in op
        assert "disposition" in op
        assert "confidence" in op
        assert "reasoning_summary" in op
        assert "agrees_with_majority" in op
        assert 0.0 <= op["confidence"] <= 1.0


def test_panel_vote_format():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = _make_contract_case()
    decision = panel.decide(case)

    # Vote should be in format "X-Y" where X+Y == panel_size
    parts = decision.majority_vote.split("-")
    assert len(parts) == 2
    assert int(parts[0]) + int(parts[1]) == decision.panel_size


def test_panel_includes_judgment():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = _make_contract_case()
    decision = panel.decide(case)
    assert decision.judgment is not None


def test_panel_minimal_case():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = Case(case_id="MIN", title="Minimal v. Case", case_type=CaseType.CIVIL)
    decision = panel.decide(case)
    # Minimal case still produces a valid decision.
    assert decision.majority_disposition in list(Disposition)
    assert decision.panel_size == 3


def test_panel_unanimous_flag():
    kb = KnowledgeBase.with_defaults()
    panel = JudicialPanel(
        statutes=kb.statutes,
        principles=kb.principles,
        precedents=kb.precedents,
    )
    case = _make_contract_case()
    decision = panel.decide(case)
    # If unanimous, all opinions should agree.
    if decision.is_unanimous:
        assert all(op["agrees_with_majority"] for op in decision.opinions)
    else:
        assert any(not op["agrees_with_majority"] for op in decision.opinions)
