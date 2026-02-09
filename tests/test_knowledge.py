"""Tests for the knowledge base."""

from legal_judge.knowledge.base import KnowledgeBase
from legal_judge.knowledge.domains import (
    get_all_precedents,
    get_all_principles,
    get_all_statutes,
    get_contract_law,
    get_criminal_law,
    get_tort_law,
)
from legal_judge.models.legal import LegalDomain, Precedent, Statute, LegalPrinciple


def test_contract_law_has_entries():
    statutes, precedents, principles = get_contract_law()
    assert len(statutes) >= 2
    assert len(precedents) >= 3
    assert len(principles) >= 3


def test_tort_law_has_entries():
    statutes, precedents, principles = get_tort_law()
    assert len(statutes) >= 1
    assert len(precedents) >= 3
    assert len(principles) >= 3


def test_criminal_law_has_entries():
    statutes, precedents, principles = get_criminal_law()
    assert len(statutes) >= 2
    assert len(precedents) >= 2
    assert len(principles) >= 3


def test_all_statutes_aggregation():
    all_statutes = get_all_statutes()
    assert len(all_statutes) >= 18  # 10 domains with statutes


def test_all_precedents_aggregation():
    all_precedents = get_all_precedents()
    assert len(all_precedents) >= 20  # Expanded precedent library


def test_all_principles_aggregation():
    all_principles = get_all_principles()
    assert len(all_principles) >= 22  # Expanded principles


def test_knowledge_base_defaults():
    kb = KnowledgeBase.with_defaults()
    assert len(kb.statutes) > 0
    assert len(kb.precedents) > 0
    assert len(kb.principles) > 0


def test_knowledge_base_create_judge():
    kb = KnowledgeBase.with_defaults()
    engine = kb.create_judge()
    assert engine is not None


def test_knowledge_base_add():
    kb = KnowledgeBase()
    assert len(kb.statutes) == 0
    kb.add_statute(Statute(
        name="Test Act",
        code="TST",
        domain=LegalDomain.CONTRACT_LAW,
    ))
    assert len(kb.statutes) == 1


def test_knowledge_base_filter_by_domain():
    kb = KnowledgeBase.with_defaults()
    contract_statutes = kb.statutes_for_domain(LegalDomain.CONTRACT_LAW)
    assert len(contract_statutes) >= 1
    for s in contract_statutes:
        assert s.domain == LegalDomain.CONTRACT_LAW


def test_knowledge_base_repr():
    kb = KnowledgeBase.with_defaults()
    r = repr(kb)
    assert "KnowledgeBase" in r
    assert "statutes=" in r
