"""Tests for the judge engine and its components."""

from legal_judge.engine.judge import JudgeEngine
from legal_judge.engine.precedent import PrecedentMatcher
from legal_judge.engine.reasoning import ReasoningChain, ReasoningType
from legal_judge.knowledge.base import KnowledgeBase
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
from legal_judge.models.judgment import Disposition, RemedyType
from legal_judge.models.legal import LegalDomain, Precedent


# ------------------------------------------------------------------
# ReasoningChain
# ------------------------------------------------------------------

def test_reasoning_chain_empty():
    chain = ReasoningChain(issue="test")
    assert chain.overall_confidence == 0.5  # default
    chain._recalculate_confidence()
    assert chain.overall_confidence == 0.0


def test_reasoning_chain_add_steps():
    chain = ReasoningChain(issue="Does X apply?")
    chain.add_step(
        reasoning_type=ReasoningType.DEDUCTIVE,
        premise="P1",
        inference="I1",
        conclusion="C1",
        confidence=0.8,
    )
    assert len(chain.steps) == 1
    assert chain.overall_confidence == 0.8

    chain.add_step(
        reasoning_type=ReasoningType.ANALOGICAL,
        premise="P2",
        inference="I2",
        conclusion="C2",
        confidence=0.6,
    )
    assert len(chain.steps) == 2
    # Geometric mean of 0.8 and 0.6
    assert 0.6 < chain.overall_confidence < 0.8


def test_reasoning_chain_finalize():
    chain = ReasoningChain(issue="Issue")
    chain.add_step(
        reasoning_type=ReasoningType.DEDUCTIVE,
        premise="P",
        inference="I",
        conclusion="C",
        confidence=0.9,
    )
    chain.finalize("Final answer")
    assert chain.final_conclusion == "Final answer"


def test_reasoning_chain_str():
    chain = ReasoningChain(issue="Test issue")
    chain.add_step(
        reasoning_type=ReasoningType.BALANCING,
        premise="P",
        inference="I",
        conclusion="C",
        confidence=0.7,
    )
    chain.finalize("Done")
    output = str(chain)
    assert "Test issue" in output
    assert "Done" in output


# ------------------------------------------------------------------
# PrecedentMatcher
# ------------------------------------------------------------------

def _sample_precedents() -> list[Precedent]:
    return [
        Precedent(
            case_name="Hadley v. Baxendale",
            citation="9 Exch. 341",
            year=1854,
            domain=LegalDomain.CONTRACT_LAW,
            holding="Damages limited to foreseeable losses.",
            ratio_decidendi="Foreseeability test for damages.",
            relevance_keywords=["damages", "breach", "contract", "foreseeability"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Donoghue v. Stevenson",
            citation="[1932] AC 562",
            year=1932,
            domain=LegalDomain.TORT_LAW,
            holding="Duty of care to ultimate consumer.",
            ratio_decidendi="Neighbour principle.",
            relevance_keywords=["duty", "care", "negligence", "consumer"],
            authority_weight=0.95,
        ),
    ]


def test_precedent_matcher_finds_contract():
    matcher = PrecedentMatcher(_sample_precedents())
    case = Case(
        case_id="T1",
        title="A v B",
        case_type=CaseType.CONTRACT,
        facts=["Breach of contract with damages claim."],
        issues=["Whether damages are recoverable."],
    )
    results = matcher.find_relevant(case)
    assert len(results) >= 1
    assert results[0].precedent.case_name == "Hadley v. Baxendale"


def test_precedent_matcher_finds_tort():
    matcher = PrecedentMatcher(_sample_precedents())
    case = Case(
        case_id="T2",
        title="C v D",
        case_type=CaseType.TORT,
        facts=["Negligence caused injury."],
        issues=["Whether duty of care was owed."],
    )
    results = matcher.find_relevant(case)
    assert len(results) >= 1
    names = [r.precedent.case_name for r in results]
    assert "Donoghue v. Stevenson" in names


def test_precedent_matcher_empty_library():
    matcher = PrecedentMatcher()
    case = Case(case_id="T3", title="E v F", case_type=CaseType.CIVIL)
    results = matcher.find_relevant(case)
    assert results == []


def test_precedent_matcher_add_precedent():
    matcher = PrecedentMatcher()
    assert len(matcher.library) == 0
    matcher.add_precedent(_sample_precedents()[0])
    assert len(matcher.library) == 1


# ------------------------------------------------------------------
# JudgeEngine - full adjudication
# ------------------------------------------------------------------

def _make_contract_case() -> Case:
    return Case(
        case_id="J-001",
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
                supporting_facts=["Late delivery", "No excuse given"],
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
            Evidence(
                title="Delivery log",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Shows no delivery.",
                submitted_by="Alpha",
                credibility_weight=0.85,
            ),
        ],
        applicable_statutes=["UCC Article 2"],
    )


def test_judge_engine_adjudicates():
    kb = KnowledgeBase.with_defaults()
    engine = kb.create_judge()
    case = _make_contract_case()
    judgment = engine.adjudicate(case)

    assert judgment.case_id == "J-001"
    assert judgment.disposition in list(Disposition)
    assert judgment.prevailing_party != ""
    assert 0.0 <= judgment.confidence <= 1.0
    assert case.status == CaseStatus.DECIDED
    assert len(judgment.sections) > 0


def test_judge_engine_criminal_case():
    kb = KnowledgeBase.with_defaults()
    engine = kb.create_judge()
    case = Case(
        case_id="CRIM-001",
        title="State v. Doe",
        case_type=CaseType.CRIMINAL,
        parties=[
            Party(name="State", role=PartyRole.PROSECUTOR),
            Party(name="John Doe", role=PartyRole.DEFENDANT),
        ],
        facts=["Defendant was found at the scene.", "Witness testimony is conflicting."],
        issues=["Whether defendant committed the offense"],
        arguments=[
            Argument(
                party_name="State",
                claim="Defendant committed the offense.",
                supporting_facts=["Found at scene"],
            ),
            Argument(
                party_name="John Doe",
                claim="Defendant was not involved.",
                supporting_facts=["Alibi evidence"],
            ),
        ],
        evidence=[
            Evidence(
                title="Witness Statement",
                evidence_type=EvidenceType.TESTIMONIAL,
                description="Conflicting testimony.",
                submitted_by="State",
                credibility_weight=0.4,
            ),
        ],
    )
    judgment = engine.adjudicate(case)
    # Criminal cases require high confidence for guilty verdict.
    assert judgment.disposition in (Disposition.GUILTY, Disposition.NOT_GUILTY)


def test_judge_engine_empty_case():
    engine = JudgeEngine()
    case = Case(
        case_id="EMPTY-001",
        title="Nobody v. Nothing",
        case_type=CaseType.CIVIL,
    )
    judgment = engine.adjudicate(case)
    assert judgment.disposition == Disposition.DISMISSED


def test_judge_remedy_for_tort():
    kb = KnowledgeBase.with_defaults()
    engine = kb.create_judge()
    case = Case(
        case_id="TORT-001",
        title="X v. Y",
        case_type=CaseType.TORT,
        parties=[
            Party(name="X", role=PartyRole.PLAINTIFF),
            Party(name="Y", role=PartyRole.DEFENDANT),
        ],
        facts=["Y caused injury to X through negligence."],
        issues=["Whether Y was negligent"],
        arguments=[
            Argument(
                party_name="X",
                claim="Y was negligent.",
                supporting_facts=["Ran red light", "Caused injury"],
                legal_basis=["Duty of care", "Negligence"],
            ),
        ],
        evidence=[
            Evidence(
                title="Medical record",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Shows injuries.",
                submitted_by="X",
                credibility_weight=0.9,
            ),
        ],
    )
    judgment = engine.adjudicate(case)
    # If granted, tort remedy should be damages.
    if judgment.disposition in (Disposition.GRANTED, Disposition.GRANTED_IN_PART):
        assert judgment.remedy == RemedyType.DAMAGES
