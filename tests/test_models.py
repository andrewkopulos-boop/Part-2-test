"""Tests for the data models."""

from datetime import date

from legal_judge.models.case import (
    Argument,
    Case,
    CaseStatus,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)
from legal_judge.models.judgment import (
    Disposition,
    Judgment,
    JudgmentSection,
    RemedyType,
)
from legal_judge.models.legal import (
    JurisdictionType,
    LegalDomain,
    LegalPrinciple,
    Precedent,
    Statute,
)


# ------------------------------------------------------------------
# Party
# ------------------------------------------------------------------

def test_party_creation():
    p = Party(name="Alice", role=PartyRole.PLAINTIFF, description="Claimant")
    assert p.name == "Alice"
    assert p.role == PartyRole.PLAINTIFF
    assert "Alice" in str(p)
    assert "plaintiff" in str(p)


# ------------------------------------------------------------------
# Evidence
# ------------------------------------------------------------------

def test_evidence_defaults():
    e = Evidence(
        title="Contract",
        evidence_type=EvidenceType.DOCUMENTARY,
        description="The signed contract.",
        submitted_by="Alice",
    )
    assert e.credibility_weight == 0.5
    assert e.admissible is True


def test_evidence_str():
    e = Evidence(
        title="Photo",
        evidence_type=EvidenceType.PHYSICAL,
        description="Scene photo.",
        submitted_by="Bob",
        admissible=False,
    )
    assert "inadmissible" in str(e)


# ------------------------------------------------------------------
# Argument
# ------------------------------------------------------------------

def test_argument_str():
    a = Argument(party_name="Alice", claim="Breach of contract occurred.")
    assert "Alice" in str(a)


# ------------------------------------------------------------------
# Case
# ------------------------------------------------------------------

def _make_case() -> Case:
    return Case(
        case_id="TEST-001",
        title="Test v. Case",
        case_type=CaseType.CONTRACT,
        parties=[
            Party(name="Alice", role=PartyRole.PLAINTIFF),
            Party(name="Bob", role=PartyRole.DEFENDANT),
        ],
        facts=["Fact 1", "Fact 2"],
        issues=["Issue 1"],
        arguments=[
            Argument(party_name="Alice", claim="Breach"),
            Argument(party_name="Bob", claim="No breach"),
        ],
        evidence=[
            Evidence(
                title="Doc1",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="d",
                submitted_by="Alice",
                credibility_weight=0.9,
            ),
            Evidence(
                title="Doc2",
                evidence_type=EvidenceType.TESTIMONIAL,
                description="d",
                submitted_by="Bob",
                admissible=False,
            ),
        ],
    )


def test_case_get_parties_by_role():
    case = _make_case()
    plaintiffs = case.get_parties_by_role(PartyRole.PLAINTIFF)
    assert len(plaintiffs) == 1
    assert plaintiffs[0].name == "Alice"


def test_case_get_admissible_evidence():
    case = _make_case()
    admissible = case.get_admissible_evidence()
    assert len(admissible) == 1
    assert admissible[0].title == "Doc1"


def test_case_get_arguments_by_party():
    case = _make_case()
    alice_args = case.get_arguments_by_party("Alice")
    assert len(alice_args) == 1
    assert alice_args[0].claim == "Breach"


def test_case_str():
    case = _make_case()
    s = str(case)
    assert "Alice" in s
    assert "Bob" in s


def test_case_status_default():
    case = _make_case()
    assert case.status == CaseStatus.FILED


# ------------------------------------------------------------------
# Judgment
# ------------------------------------------------------------------

def test_judgment_creation():
    j = Judgment(
        case_id="TEST-001",
        case_title="Test v. Case",
        disposition=Disposition.GRANTED,
        remedy=RemedyType.DAMAGES,
        confidence=0.75,
        prevailing_party="Alice",
    )
    assert j.disposition == Disposition.GRANTED
    assert j.confidence == 0.75
    assert "GRANTED" in str(j).upper()


def test_judgment_section():
    s = JudgmentSection(heading="I. Intro", content="Some content")
    assert s.heading == "I. Intro"
    assert s.subsections == []


# ------------------------------------------------------------------
# Legal models
# ------------------------------------------------------------------

def test_statute_str():
    s = Statute(
        name="UCC Art 2",
        code="UCC",
        section="Art. 2",
        domain=LegalDomain.CONTRACT_LAW,
    )
    assert "UCC" in str(s)


def test_precedent_str():
    p = Precedent(
        case_name="Hadley v. Baxendale",
        citation="9 Exch. 341",
        year=1854,
        domain=LegalDomain.CONTRACT_LAW,
    )
    assert "1854" in str(p)
    assert "Hadley" in str(p)


def test_principle_str_with_latin():
    p = LegalPrinciple(
        name="Good Faith",
        latin_name="Bona Fide",
        domain=LegalDomain.CONTRACT_LAW,
        description="Act in good faith.",
    )
    assert "Bona Fide" in str(p)


def test_principle_str_without_latin():
    p = LegalPrinciple(
        name="Mitigation",
        domain=LegalDomain.CONTRACT_LAW,
        description="Mitigate damages.",
    )
    assert str(p) == "Mitigation"
