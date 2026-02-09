"""Tests for the opinion writer and formatter."""

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
from legal_judge.output.formatter import Formatter
from legal_judge.output.opinion import OpinionWriter


def _make_case() -> Case:
    return Case(
        case_id="OUT-001",
        title="Plaintiff v. Defendant",
        case_type=CaseType.CONTRACT,
        parties=[
            Party(name="Plaintiff", role=PartyRole.PLAINTIFF),
            Party(name="Defendant", role=PartyRole.DEFENDANT),
        ],
        facts=["Contract was signed.", "Defendant failed to perform."],
        issues=["Whether defendant breached the contract"],
        arguments=[
            Argument(
                party_name="Plaintiff",
                claim="Defendant breached the contract.",
                supporting_facts=["Non-performance"],
                legal_basis=["Breach of contract"],
            ),
        ],
        evidence=[
            Evidence(
                title="Contract Copy",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Signed contract.",
                submitted_by="Plaintiff",
                credibility_weight=0.9,
            ),
        ],
    )


def test_opinion_writer_decide():
    writer = OpinionWriter()
    case = _make_case()
    judgment = writer.decide(case)
    assert judgment.case_id == "OUT-001"
    assert judgment.prevailing_party != ""


def test_opinion_writer_render_text():
    writer = OpinionWriter()
    case = _make_case()
    text = writer.render_text(case)
    assert "JUDICIAL OPINION" in text
    assert "Plaintiff v. Defendant" in text
    assert "HOLDING" in text


def test_opinion_writer_render_markdown():
    writer = OpinionWriter()
    case = _make_case()
    md = writer.render_markdown(case)
    assert "# Judicial Opinion" in md
    assert "| **Case ID**" in md


def test_formatter_text_has_sections():
    writer = OpinionWriter()
    case = _make_case()
    judgment = writer.decide(case)
    text = Formatter.to_text(judgment)
    assert "I. Introduction" in text
    assert "END OF OPINION" in text


def test_formatter_markdown_has_structure():
    writer = OpinionWriter()
    case = _make_case()
    judgment = writer.decide(case)
    md = Formatter.to_markdown(judgment)
    assert "## Holding" in md
    assert "## Rules Applied" in md


def test_static_format_methods():
    writer = OpinionWriter()
    case = _make_case()
    judgment = writer.decide(case)
    text = OpinionWriter.format_judgment_text(judgment)
    md = OpinionWriter.format_judgment_markdown(judgment)
    assert "JUDICIAL OPINION" in text
    assert "# Judicial Opinion" in md
