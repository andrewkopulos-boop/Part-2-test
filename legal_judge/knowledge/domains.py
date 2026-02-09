"""Built-in legal knowledge across multiple domains.

This module provides a curated set of statutes, precedents, and principles
drawn from well-known areas of Anglo-American common law. These serve as
the judge bot's baseline legal knowledge.
"""

from __future__ import annotations

from legal_judge.models.legal import (
    JurisdictionType,
    LegalDomain,
    LegalPrinciple,
    Precedent,
    Statute,
)

# ======================================================================
# CONTRACT LAW
# ======================================================================


def get_contract_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Uniform Commercial Code Article 2",
            code="UCC",
            section="Art. 2",
            domain=LegalDomain.CONTRACT_LAW,
            summary="Governs the sale of goods, including formation, performance, and remedies for breach.",
        ),
        Statute(
            name="Statute of Frauds",
            code="Common Law",
            section="Various",
            domain=LegalDomain.CONTRACT_LAW,
            summary="Requires certain contracts to be in writing to be enforceable, including contracts for sale of land and contracts not performable within one year.",
        ),
        Statute(
            name="Restatement (Second) of Contracts",
            code="Restatement",
            section="Various",
            domain=LegalDomain.CONTRACT_LAW,
            summary="Authoritative treatise on contract law principles including formation, consideration, and breach.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Hadley v. Baxendale",
            citation="9 Exch. 341",
            year=1854,
            domain=LegalDomain.CONTRACT_LAW,
            holding="Damages for breach of contract are limited to those arising naturally from the breach or those reasonably contemplated by both parties at the time of contracting.",
            ratio_decidendi="Foreseeability is the test for consequential damages in contract.",
            relevance_keywords=["damages", "breach", "contract", "foreseeability", "consequential"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Carlill v. Carbolic Smoke Ball Co.",
            citation="[1893] 1 QB 256",
            year=1893,
            domain=LegalDomain.CONTRACT_LAW,
            holding="An advertisement can constitute a binding unilateral offer if it shows clear intent to be bound and consideration is provided by performance.",
            ratio_decidendi="A unilateral contract is formed when an offer is accepted by performance.",
            relevance_keywords=["offer", "acceptance", "unilateral", "contract", "advertisement", "performance"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Williams v. Roffey Bros.",
            citation="[1991] 1 QB 1",
            year=1991,
            domain=LegalDomain.CONTRACT_LAW,
            holding="A practical benefit conferred on the promisor can constitute sufficient consideration for a promise of additional payment.",
            ratio_decidendi="Practical benefit can satisfy the consideration requirement.",
            relevance_keywords=["consideration", "practical", "benefit", "payment", "contract", "modification"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Lucy v. Zehmer",
            citation="196 Va. 493",
            year=1954,
            domain=LegalDomain.CONTRACT_LAW,
            holding="An agreement is enforceable if a reasonable person would believe a valid offer was made, regardless of the offeror's subjective intent.",
            ratio_decidendi="Objective theory of contracts: outward expressions, not secret intentions, determine contract formation.",
            relevance_keywords=["intent", "objective", "offer", "agreement", "formation", "reasonable"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Freedom of Contract",
            latin_name="Libertas Contractus",
            domain=LegalDomain.CONTRACT_LAW,
            description="Parties are free to enter into contracts and determine their terms, subject to public policy limits.",
            elements=["mutual assent", "capacity", "lawful purpose"],
            exceptions=["unconscionability", "duress", "undue influence", "illegality"],
        ),
        LegalPrinciple(
            name="Consideration",
            domain=LegalDomain.CONTRACT_LAW,
            description="A contract requires consideration - a bargained-for exchange of value between the parties.",
            elements=["bargained-for exchange", "legal value", "adequacy not required"],
            exceptions=["promissory estoppel", "contracts under seal"],
        ),
        LegalPrinciple(
            name="Good Faith and Fair Dealing",
            latin_name="Bona Fide",
            domain=LegalDomain.CONTRACT_LAW,
            description="Every contract imposes an obligation of good faith and fair dealing in its performance and enforcement.",
            elements=["honesty in fact", "reasonable commercial standards"],
        ),
        LegalPrinciple(
            name="Mitigation of Damages",
            domain=LegalDomain.CONTRACT_LAW,
            description="The injured party has a duty to take reasonable steps to minimize damages after a breach.",
            elements=["reasonable effort", "good faith attempt to reduce loss"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# TORT LAW
# ======================================================================


def get_tort_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Restatement (Third) of Torts",
            code="Restatement",
            section="Various",
            domain=LegalDomain.TORT_LAW,
            summary="Comprehensive treatise on tort liability including negligence, strict liability, and intentional torts.",
        ),
        Statute(
            name="Comparative Negligence Statute",
            code="Model Act",
            section="Various",
            domain=LegalDomain.TORT_LAW,
            summary="Allows recovery based on proportional fault, reducing damages by the plaintiff's percentage of negligence.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Donoghue v. Stevenson",
            citation="[1932] AC 562",
            year=1932,
            domain=LegalDomain.TORT_LAW,
            holding="Manufacturers owe a duty of care to the ultimate consumer of their products.",
            ratio_decidendi="The 'neighbour principle': you owe a duty of care to persons closely and directly affected by your actions.",
            relevance_keywords=["duty", "care", "negligence", "manufacturer", "consumer", "product", "liability"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Palsgraf v. Long Island Railroad Co.",
            citation="248 N.Y. 339",
            year=1928,
            domain=LegalDomain.TORT_LAW,
            holding="A defendant owes a duty of care only to foreseeable plaintiffs within the zone of danger.",
            ratio_decidendi="Duty in negligence is limited to risks reasonably foreseeable to the particular plaintiff.",
            relevance_keywords=["duty", "foreseeability", "negligence", "proximate", "cause", "zone", "danger"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Liebeck v. McDonald's Restaurants",
            citation="No. D-202 CV-93-02419",
            year=1994,
            domain=LegalDomain.TORT_LAW,
            holding="A manufacturer can be liable for injuries caused by a product that is unreasonably dangerous when the risk is foreseeable.",
            ratio_decidendi="Product liability extends to foreseeable misuse and unreasonable danger.",
            relevance_keywords=["product", "liability", "negligence", "injury", "damages", "unreasonable", "danger"],
            authority_weight=0.70,
        ),
        Precedent(
            case_name="Rylands v. Fletcher",
            citation="(1868) LR 3 HL 330",
            year=1868,
            domain=LegalDomain.TORT_LAW,
            holding="A person who brings something on their land which is likely to do mischief if it escapes is strictly liable for damage caused by its escape.",
            ratio_decidendi="Strict liability applies to non-natural use of land causing foreseeable harm.",
            relevance_keywords=["strict", "liability", "land", "escape", "damage", "non-natural", "nuisance"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Duty of Care",
            domain=LegalDomain.TORT_LAW,
            description="A person owes a duty to act with reasonable care toward others who could foreseeably be harmed.",
            elements=["foreseeability", "proximity", "fairness"],
            exceptions=["no duty to rescue (general rule)", "assumption of risk"],
        ),
        LegalPrinciple(
            name="Proximate Cause",
            latin_name="Causa Proxima",
            domain=LegalDomain.TORT_LAW,
            description="The defendant's action must be a proximate (legally sufficient) cause of the plaintiff's harm.",
            elements=["but-for causation", "foreseeability of harm", "no superseding cause"],
        ),
        LegalPrinciple(
            name="Res Ipsa Loquitur",
            latin_name="Res Ipsa Loquitur",
            domain=LegalDomain.TORT_LAW,
            description="The thing speaks for itself - negligence may be inferred from the very nature of an accident when it ordinarily would not occur without negligence.",
            elements=[
                "accident does not normally occur without negligence",
                "instrumentality was in defendant's exclusive control",
                "plaintiff did not contribute to the injury",
            ],
        ),
        LegalPrinciple(
            name="Vicarious Liability",
            latin_name="Respondeat Superior",
            domain=LegalDomain.TORT_LAW,
            description="An employer is liable for the torts of employees committed within the scope of employment.",
            elements=["employer-employee relationship", "scope of employment", "tortious act"],
            exceptions=["independent contractors (generally)", "frolic and detour"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# CRIMINAL LAW
# ======================================================================


def get_criminal_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Model Penal Code",
            code="MPC",
            section="Various",
            domain=LegalDomain.CRIMINAL_LAW,
            summary="Model criminal code covering offenses, defenses, and sentencing guidelines.",
        ),
        Statute(
            name="Fourth Amendment",
            code="U.S. Const.",
            section="Amend. IV",
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Protects against unreasonable searches and seizures and requires warrants based on probable cause.",
        ),
        Statute(
            name="Fifth Amendment",
            code="U.S. Const.",
            section="Amend. V",
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Protects against self-incrimination, double jeopardy, and guarantees due process of law.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Miranda v. Arizona",
            citation="384 U.S. 436",
            year=1966,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Statements made during custodial interrogation are inadmissible unless the suspect was informed of their rights.",
            ratio_decidendi="The Fifth Amendment requires warning suspects of their right to silence and counsel before custodial interrogation.",
            relevance_keywords=["rights", "interrogation", "confession", "custodial", "silence", "counsel", "admissible"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Mapp v. Ohio",
            citation="367 U.S. 643",
            year=1961,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Evidence obtained through unconstitutional search and seizure is inadmissible in state courts.",
            ratio_decidendi="The exclusionary rule applies to the states through the Fourteenth Amendment.",
            relevance_keywords=["search", "seizure", "evidence", "exclusionary", "fourth", "amendment", "inadmissible"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="R v. Woollin",
            citation="[1999] 1 AC 82",
            year=1999,
            domain=LegalDomain.CRIMINAL_LAW,
            holding="Intent can be inferred where the defendant foresaw death or serious harm as a virtual certainty.",
            ratio_decidendi="Virtual certainty of consequence allows inference of intent for murder.",
            relevance_keywords=["intent", "murder", "foresight", "certainty", "mens", "rea", "death"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Presumption of Innocence",
            latin_name="Praesumptio Innocentiae",
            domain=LegalDomain.CRIMINAL_LAW,
            description="Every person accused of a crime is presumed innocent until proven guilty beyond a reasonable doubt.",
            elements=["burden on prosecution", "proof beyond reasonable doubt"],
        ),
        LegalPrinciple(
            name="Mens Rea",
            latin_name="Mens Rea",
            domain=LegalDomain.CRIMINAL_LAW,
            description="A guilty mind is generally required for criminal liability - the defendant must have intended the criminal act or been reckless.",
            elements=["purpose", "knowledge", "recklessness", "negligence"],
            exceptions=["strict liability offenses"],
        ),
        LegalPrinciple(
            name="Actus Reus",
            latin_name="Actus Reus",
            domain=LegalDomain.CRIMINAL_LAW,
            description="Criminal liability requires a voluntary guilty act or omission where there is a duty to act.",
            elements=["voluntary act", "omission where duty exists", "state of affairs"],
        ),
        LegalPrinciple(
            name="Double Jeopardy",
            latin_name="Autrefois Acquit",
            domain=LegalDomain.CRIMINAL_LAW,
            description="A person cannot be tried twice for the same offense after acquittal or conviction.",
            elements=["same offense", "prior acquittal or conviction", "same sovereign"],
            exceptions=["separate sovereigns doctrine", "mistrial"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# CONSTITUTIONAL LAW
# ======================================================================


def _get_constitutional_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Fourteenth Amendment - Equal Protection",
            code="U.S. Const.",
            section="Amend. XIV",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="No state shall deny to any person within its jurisdiction the equal protection of the laws.",
        ),
        Statute(
            name="First Amendment",
            code="U.S. Const.",
            section="Amend. I",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Protects freedom of speech, religion, press, assembly, and petition.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Marbury v. Madison",
            citation="5 U.S. 137",
            year=1803,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Supreme Court has the power to review acts of Congress and declare them unconstitutional.",
            ratio_decidendi="Judicial review is inherent in the constitutional structure.",
            relevance_keywords=["judicial", "review", "constitutional", "power", "unconstitutional", "congress"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Brown v. Board of Education",
            citation="347 U.S. 483",
            year=1954,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Separate educational facilities are inherently unequal and violate the Equal Protection Clause.",
            ratio_decidendi="Racial segregation in public schools is unconstitutional.",
            relevance_keywords=["equal", "protection", "segregation", "discrimination", "education", "rights"],
            authority_weight=0.95,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Due Process",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            description="No person shall be deprived of life, liberty, or property without due process of law.",
            elements=["notice", "opportunity to be heard", "impartial tribunal"],
            related_principles=["procedural due process", "substantive due process"],
        ),
        LegalPrinciple(
            name="Equal Protection",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            description="The law must treat similarly situated individuals in the same manner.",
            elements=["classification", "level of scrutiny", "governmental interest"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# PROPERTY LAW
# ======================================================================


def _get_property_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Recording Acts",
            code="Model Act",
            section="Various",
            domain=LegalDomain.PROPERTY_LAW,
            summary="Governs the recording of property interests and priorities among competing claims.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Pierson v. Post",
            citation="3 Cai. R. 175",
            year=1805,
            domain=LegalDomain.PROPERTY_LAW,
            holding="Mere pursuit of a wild animal does not vest property rights; actual capture or mortal wounding is required.",
            ratio_decidendi="Property in wild animals requires physical possession or certain control.",
            relevance_keywords=["property", "possession", "capture", "ownership", "rights", "wild"],
            authority_weight=0.75,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Adverse Possession",
            domain=LegalDomain.PROPERTY_LAW,
            description="Title to land may be acquired by continuous, open, notorious, adverse, and exclusive possession for a statutory period.",
            elements=["continuous", "open and notorious", "adverse/hostile", "exclusive", "statutory period"],
        ),
        LegalPrinciple(
            name="Bundle of Rights",
            domain=LegalDomain.PROPERTY_LAW,
            description="Property ownership consists of a bundle of rights including possession, use, exclusion, and disposition.",
            elements=["right to possess", "right to use", "right to exclude", "right to transfer"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# EMPLOYMENT LAW
# ======================================================================


def _get_employment_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Title VII of the Civil Rights Act",
            code="42 U.S.C.",
            section="\u00a72000e",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Prohibits employment discrimination based on race, color, religion, sex, or national origin.",
        ),
        Statute(
            name="Fair Labor Standards Act",
            code="29 U.S.C.",
            section="\u00a7201",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Establishes minimum wage, overtime pay, and child labor standards.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="McDonnell Douglas Corp. v. Green",
            citation="411 U.S. 792",
            year=1973,
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Established the burden-shifting framework for employment discrimination cases.",
            ratio_decidendi="Plaintiff must establish a prima facie case, then burden shifts to employer for legitimate reason.",
            relevance_keywords=["discrimination", "employment", "burden", "prima", "facie", "hiring", "termination"],
            authority_weight=0.90,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="At-Will Employment",
            domain=LegalDomain.EMPLOYMENT_LAW,
            description="Either party may terminate the employment relationship at any time for any lawful reason.",
            elements=["no fixed term", "mutual right to terminate"],
            exceptions=["discriminatory termination", "retaliation", "public policy violations", "implied contract"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# Aggregation helpers
# ======================================================================


def _all_domains() -> list[tuple[list[Statute], list[Precedent], list[LegalPrinciple]]]:
    return [
        get_contract_law(),
        get_tort_law(),
        get_criminal_law(),
        _get_constitutional_law(),
        _get_property_law(),
        _get_employment_law(),
    ]


def get_all_statutes() -> list[Statute]:
    return [s for domain in _all_domains() for s in domain[0]]


def get_all_precedents() -> list[Precedent]:
    return [p for domain in _all_domains() for p in domain[1]]


def get_all_principles() -> list[LegalPrinciple]:
    return [p for domain in _all_domains() for p in domain[2]]
