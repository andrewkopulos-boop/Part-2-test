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
        Statute(
            name="Uniform Commercial Code Article 2A",
            code="UCC",
            section="Art. 2A",
            domain=LegalDomain.CONTRACT_LAW,
            summary="Governs leases of goods, providing rules for formation, effect, and enforcement of lease contracts.",
        ),
        Statute(
            name="Electronic Signatures in Global and National Commerce Act",
            code="15 U.S.C.",
            section="§7001",
            domain=LegalDomain.CONTRACT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Validates electronic signatures and records in interstate and foreign commerce, ensuring digital contracts are enforceable.",
        ),
        Statute(
            name="Uniform Electronic Transactions Act",
            code="UETA",
            section="Various",
            domain=LegalDomain.CONTRACT_LAW,
            summary="State-level model act giving legal effect to electronic records and signatures in transactions.",
        ),
        Statute(
            name="Convention on Contracts for the International Sale of Goods",
            code="CISG",
            section="Various",
            domain=LegalDomain.CONTRACT_LAW,
            jurisdiction=JurisdictionType.INTERNATIONAL,
            summary="International treaty governing contracts for the sale of goods between parties in different contracting states.",
        ),
        Statute(
            name="Magnuson-Moss Warranty Act",
            code="15 U.S.C.",
            section="§2301",
            domain=LegalDomain.CONTRACT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Federal law governing consumer product warranties, requiring clear disclosure of warranty terms and limiting disclaimer of implied warranties.",
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
        Precedent(
            case_name="Hamer v. Sidway",
            citation="124 N.Y. 538",
            year=1891,
            domain=LegalDomain.CONTRACT_LAW,
            holding="Forbearance from a legal right at the request of another constitutes sufficient consideration for a promise.",
            ratio_decidendi="Consideration may consist of a detriment to the promisee, not merely a benefit to the promisor.",
            relevance_keywords=["consideration", "forbearance", "promise", "detriment", "benefit", "contract"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Jacob & Youngs v. Kent",
            citation="230 N.Y. 239",
            year=1921,
            domain=LegalDomain.CONTRACT_LAW,
            holding="Trivial or innocent departures from contract specifications do not justify forfeiture where substantial performance has occurred.",
            ratio_decidendi="The doctrine of substantial performance prevents forfeiture for minor, unintentional deviations.",
            relevance_keywords=["substantial", "performance", "breach", "minor", "forfeiture", "construction", "specification"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Peevyhouse v. Garland Coal & Mining Co.",
            citation="382 P.2d 109",
            year=1962,
            domain=LegalDomain.CONTRACT_LAW,
            holding="Where the cost of performance greatly exceeds the diminution in value caused by the breach, damages are limited to the diminution in value.",
            ratio_decidendi="Economic waste doctrine limits damages to the lesser of cost of performance or diminution in value.",
            relevance_keywords=["damages", "breach", "cost", "performance", "diminution", "value", "economic", "waste"],
            authority_weight=0.75,
        ),
        Precedent(
            case_name="ProCD Inc. v. Zeidenberg",
            citation="86 F.3d 1447",
            year=1996,
            domain=LegalDomain.CONTRACT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Shrinkwrap licenses are enforceable contracts when the buyer has an opportunity to review terms and the option to return the product.",
            ratio_decidendi="Terms inside a box are binding if the buyer uses the product after having opportunity to review and reject.",
            relevance_keywords=["shrinkwrap", "license", "terms", "acceptance", "software", "contract", "clickwrap"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Wood v. Lucy, Lady Duff-Gordon",
            citation="222 N.Y. 88",
            year=1917,
            domain=LegalDomain.CONTRACT_LAW,
            holding="An implied promise to use reasonable efforts can supply the consideration needed for an exclusive dealing arrangement.",
            ratio_decidendi="Courts will imply an obligation of reasonable efforts to uphold commercial agreements.",
            relevance_keywords=["implied", "promise", "consideration", "exclusive", "dealing", "efforts", "reasonable"],
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
        LegalPrinciple(
            name="Promissory Estoppel",
            domain=LegalDomain.CONTRACT_LAW,
            description="A promise that the promisor should reasonably expect to induce reliance is binding if injustice can be avoided only by enforcement.",
            elements=["clear and definite promise", "reasonable reliance", "detrimental reliance", "injustice without enforcement"],
            exceptions=["availability of other remedies", "unreasonable reliance"],
            related_principles=["consideration", "equitable estoppel"],
        ),
        LegalPrinciple(
            name="Unconscionability",
            domain=LegalDomain.CONTRACT_LAW,
            description="Courts may refuse to enforce contracts or clauses that are so one-sided as to be oppressive, considering both procedural and substantive unfairness.",
            elements=["procedural unconscionability (unfair bargaining process)", "substantive unconscionability (unfair terms)", "absence of meaningful choice"],
            exceptions=["commercially sophisticated parties", "arm's-length negotiation"],
        ),
        LegalPrinciple(
            name="Parol Evidence Rule",
            domain=LegalDomain.CONTRACT_LAW,
            description="When parties reduce their agreement to a final written document, prior or contemporaneous oral or written agreements that contradict the writing are inadmissible.",
            elements=["integrated written agreement", "prior or contemporaneous terms", "contradiction of written terms"],
            exceptions=["fraud", "duress", "mistake", "ambiguity", "conditions precedent", "subsequent modifications"],
        ),
        LegalPrinciple(
            name="Anticipatory Repudiation",
            domain=LegalDomain.CONTRACT_LAW,
            description="When a party clearly and unequivocally indicates it will not perform its contractual obligations before performance is due, the other party may treat the contract as breached immediately.",
            elements=["clear and unequivocal refusal", "communication before performance due", "material obligation"],
            related_principles=["mitigation of damages", "adequate assurance of performance"],
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
        Statute(
            name="Federal Tort Claims Act",
            code="28 U.S.C.",
            section="§1346(b)",
            domain=LegalDomain.TORT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Waives sovereign immunity and allows tort claims against the United States for negligent acts of federal employees acting within the scope of employment.",
        ),
        Statute(
            name="Restatement (Second) of Torts - Products Liability",
            code="Restatement",
            section="§402A",
            domain=LegalDomain.TORT_LAW,
            summary="Imposes strict liability on sellers of defective products that are unreasonably dangerous to the user or consumer.",
        ),
        Statute(
            name="Wrongful Death Statute",
            code="Model Act",
            section="Various",
            domain=LegalDomain.TORT_LAW,
            summary="Allows surviving family members or estate representatives to bring a cause of action for a death caused by the wrongful act or negligence of another.",
        ),
        Statute(
            name="Good Samaritan Laws",
            code="Model Act",
            section="Various",
            domain=LegalDomain.TORT_LAW,
            summary="Provides immunity from civil liability for persons who render emergency assistance in good faith without expectation of compensation.",
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
        Precedent(
            case_name="BMW of North America v. Gore",
            citation="517 U.S. 559",
            year=1996,
            domain=LegalDomain.TORT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Grossly excessive punitive damages violate the Due Process Clause of the Fourteenth Amendment.",
            ratio_decidendi="Punitive damages must bear a reasonable relationship to compensatory damages using guideposts of reprehensibility, ratio, and comparable sanctions.",
            relevance_keywords=["punitive", "damages", "excessive", "due", "process", "constitutional", "ratio"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Tarasoff v. Regents of the University of California",
            citation="17 Cal.3d 425",
            year=1976,
            domain=LegalDomain.TORT_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="When a therapist determines a patient poses a serious danger to another, the therapist has a duty to protect the intended victim.",
            ratio_decidendi="Special relationships create affirmative duties to protect identifiable third parties from foreseeable harm.",
            relevance_keywords=["duty", "warn", "protect", "therapist", "danger", "special", "relationship", "third", "party"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Escola v. Coca-Cola Bottling Co.",
            citation="24 Cal.2d 453",
            year=1944,
            domain=LegalDomain.TORT_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="A manufacturer is strictly liable in tort when placing a defective product on the market knowing it will be used without inspection.",
            ratio_decidendi="Public policy supports strict liability for defective products to ensure manufacturers bear the cost of injuries.",
            relevance_keywords=["strict", "liability", "product", "defective", "manufacturer", "injury", "consumer"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Summers v. Tice",
            citation="33 Cal.2d 80",
            year=1948,
            domain=LegalDomain.TORT_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="When two defendants acted tortiously and it is impossible to determine which one caused the injury, the burden of proof shifts to each defendant to prove they were not the cause.",
            ratio_decidendi="Alternative liability shifts the burden of causation to defendants when each acted negligently and either could have caused the harm.",
            relevance_keywords=["causation", "burden", "proof", "alternative", "liability", "negligence", "multiple", "defendants"],
            authority_weight=0.80,
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
        LegalPrinciple(
            name="Strict Product Liability",
            domain=LegalDomain.TORT_LAW,
            description="Manufacturers and sellers are liable for injuries caused by defective products regardless of fault or negligence.",
            elements=["defective product (manufacturing, design, or warning defect)", "product reached consumer without substantial alteration", "defect caused injury"],
            exceptions=["product misuse", "assumption of risk", "state of the art defense"],
        ),
        LegalPrinciple(
            name="Contributory and Comparative Negligence",
            domain=LegalDomain.TORT_LAW,
            description="A plaintiff's own negligence may reduce or bar recovery depending on the jurisdiction's approach to shared fault.",
            elements=["plaintiff's fault", "causal connection to harm", "comparison of fault percentages"],
            related_principles=["pure comparative negligence", "modified comparative negligence", "contributory negligence bar"],
        ),
        LegalPrinciple(
            name="Assumption of Risk",
            latin_name="Volenti Non Fit Injuria",
            domain=LegalDomain.TORT_LAW,
            description="A plaintiff who voluntarily assumes a known risk cannot recover for injuries resulting from that risk.",
            elements=["knowledge of the risk", "voluntary assumption", "risk was the cause of injury"],
            exceptions=["implied primary assumption of risk", "firefighter's rule"],
        ),
        LegalPrinciple(
            name="Negligence Per Se",
            domain=LegalDomain.TORT_LAW,
            description="Violation of a statute designed to protect a class of persons creates a presumption of negligence if the plaintiff is within the protected class and suffered the type of harm the statute was designed to prevent.",
            elements=["violation of statute", "plaintiff in protected class", "harm of the type statute intended to prevent"],
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
        Statute(
            name="Sixth Amendment",
            code="U.S. Const.",
            section="Amend. VI",
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Guarantees the right to a speedy and public trial, impartial jury, confrontation of witnesses, and assistance of counsel.",
        ),
        Statute(
            name="Eighth Amendment",
            code="U.S. Const.",
            section="Amend. VIII",
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Prohibits excessive bail, excessive fines, and cruel and unusual punishment.",
        ),
        Statute(
            name="Racketeer Influenced and Corrupt Organizations Act",
            code="18 U.S.C.",
            section="§1961",
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Provides for extended criminal penalties and civil cause of action for acts performed as part of an ongoing criminal organization.",
        ),
        Statute(
            name="Federal Sentencing Guidelines",
            code="U.S.S.G.",
            section="Various",
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Advisory guidelines establishing sentencing ranges based on offense level and criminal history category.",
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
        Precedent(
            case_name="Gideon v. Wainwright",
            citation="372 U.S. 335",
            year=1963,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Sixth Amendment right to counsel is a fundamental right applicable to state criminal prosecutions through the Fourteenth Amendment.",
            ratio_decidendi="Indigent defendants in felony cases must be provided counsel at state expense.",
            relevance_keywords=["counsel", "right", "attorney", "indigent", "sixth", "amendment", "defense", "felony"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Terry v. Ohio",
            citation="392 U.S. 1",
            year=1968,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Police may briefly detain and pat down a person based on reasonable suspicion of criminal activity without a warrant.",
            ratio_decidendi="A stop and frisk based on reasonable articulable suspicion does not violate the Fourth Amendment.",
            relevance_keywords=["stop", "frisk", "reasonable", "suspicion", "search", "fourth", "amendment", "pat", "down"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Brady v. Maryland",
            citation="373 U.S. 83",
            year=1963,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The prosecution must disclose material evidence favorable to the defendant upon request.",
            ratio_decidendi="Suppression of exculpatory evidence violates due process regardless of prosecution's good or bad faith.",
            relevance_keywords=["disclosure", "exculpatory", "evidence", "prosecution", "due", "process", "material", "favorable"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Batson v. Kentucky",
            citation="476 U.S. 79",
            year=1986,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The use of peremptory challenges to exclude jurors based on race violates the Equal Protection Clause.",
            ratio_decidendi="Racially discriminatory use of peremptory strikes in jury selection is unconstitutional.",
            relevance_keywords=["jury", "selection", "peremptory", "race", "discrimination", "equal", "protection", "challenge"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Katz v. United States",
            citation="389 U.S. 347",
            year=1967,
            domain=LegalDomain.CRIMINAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Fourth Amendment protects people, not places; a search occurs when the government violates a reasonable expectation of privacy.",
            ratio_decidendi="The reasonable expectation of privacy test determines whether a Fourth Amendment search has occurred.",
            relevance_keywords=["privacy", "search", "expectation", "fourth", "amendment", "surveillance", "wiretap", "electronic"],
            authority_weight=0.90,
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
        LegalPrinciple(
            name="Legality",
            latin_name="Nullum Crimen Sine Lege",
            domain=LegalDomain.CRIMINAL_LAW,
            description="No conduct may be treated as criminal unless it has been defined as such by statute before the conduct occurred.",
            elements=["prior statutory definition", "fair notice", "no retroactive application"],
            related_principles=["void for vagueness", "rule of lenity"],
        ),
        LegalPrinciple(
            name="Self-Defense",
            domain=LegalDomain.CRIMINAL_LAW,
            description="A person may use reasonable force to defend themselves against an imminent threat of unlawful bodily harm.",
            elements=["imminent threat", "reasonable belief of danger", "proportional force", "no duty to retreat (in stand-your-ground jurisdictions)"],
            exceptions=["initial aggressor", "excessive force", "duty to retreat (in retreat jurisdictions)"],
        ),
        LegalPrinciple(
            name="Entrapment",
            domain=LegalDomain.CRIMINAL_LAW,
            description="A defendant may assert entrapment when law enforcement induces a person to commit a crime they were not predisposed to commit.",
            elements=["government inducement", "lack of predisposition (subjective test)", "conduct that would induce a law-abiding person (objective test)"],
        ),
        LegalPrinciple(
            name="Accomplice Liability",
            domain=LegalDomain.CRIMINAL_LAW,
            description="A person who aids, abets, counsels, or procures the commission of a crime is liable as a principal.",
            elements=["intent to assist", "act of assistance", "underlying criminal offense committed"],
            exceptions=["withdrawal before crime", "protected class member"],
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
        Statute(
            name="Second Amendment",
            code="U.S. Const.",
            section="Amend. II",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Protects the right of the people to keep and bear arms.",
        ),
        Statute(
            name="Thirteenth Amendment",
            code="U.S. Const.",
            section="Amend. XIII",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Abolishes slavery and involuntary servitude except as punishment for crime.",
        ),
        Statute(
            name="Commerce Clause",
            code="U.S. Const.",
            section="Art. I, §8, cl. 3",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Grants Congress the power to regulate commerce among the states, with foreign nations, and with Indian tribes.",
        ),
        Statute(
            name="Supremacy Clause",
            code="U.S. Const.",
            section="Art. VI, cl. 2",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Establishes that federal law is the supreme law of the land and preempts conflicting state laws.",
        ),
        Statute(
            name="Tenth Amendment",
            code="U.S. Const.",
            section="Amend. X",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Powers not delegated to the federal government nor prohibited to the states are reserved to the states or the people.",
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
        Precedent(
            case_name="New York Times Co. v. Sullivan",
            citation="376 U.S. 254",
            year=1964,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Public officials suing for defamation must prove actual malice - knowledge of falsity or reckless disregard for the truth.",
            ratio_decidendi="The First Amendment requires the actual malice standard for defamation claims by public officials.",
            relevance_keywords=["speech", "press", "defamation", "first", "amendment", "actual", "malice", "public", "official"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Griswold v. Connecticut",
            citation="381 U.S. 479",
            year=1965,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Constitution protects a right to privacy found in the penumbras of the Bill of Rights.",
            ratio_decidendi="The right to privacy is a fundamental right implicit in several constitutional amendments.",
            relevance_keywords=["privacy", "right", "fundamental", "penumbra", "contraception", "liberty", "personal"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="McCulloch v. Maryland",
            citation="17 U.S. 316",
            year=1819,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Congress has implied powers under the Necessary and Proper Clause, and states cannot tax the federal government.",
            ratio_decidendi="Federal supremacy and implied powers doctrine: the power to create implies the power to preserve.",
            relevance_keywords=["implied", "powers", "necessary", "proper", "federal", "supremacy", "state", "tax"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Tinker v. Des Moines Independent Community School District",
            citation="393 U.S. 503",
            year=1969,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Students do not shed their constitutional rights at the schoolhouse gate; student speech is protected unless it materially disrupts school operations.",
            ratio_decidendi="Student expression that does not cause substantial disruption is protected under the First Amendment.",
            relevance_keywords=["speech", "student", "school", "first", "amendment", "expression", "symbolic", "protest"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Citizens United v. Federal Election Commission",
            citation="558 U.S. 310",
            year=2010,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Political speech by corporations and unions is protected by the First Amendment; the government cannot restrict independent political expenditures.",
            ratio_decidendi="The First Amendment does not allow restricting political speech based on the speaker's corporate identity.",
            relevance_keywords=["speech", "corporate", "political", "expenditure", "first", "amendment", "election", "campaign"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Obergefell v. Hodges",
            citation="576 U.S. 644",
            year=2015,
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Fourteenth Amendment requires all states to grant and recognize same-sex marriages.",
            ratio_decidendi="The right to marry is a fundamental liberty protected by the Due Process and Equal Protection Clauses.",
            relevance_keywords=["marriage", "fundamental", "right", "equal", "protection", "due", "process", "liberty", "same-sex"],
            authority_weight=0.85,
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
        LegalPrinciple(
            name="Separation of Powers",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            description="Government power is divided among legislative, executive, and judicial branches, with each branch serving as a check on the others.",
            elements=["legislative power (Article I)", "executive power (Article II)", "judicial power (Article III)", "checks and balances"],
        ),
        LegalPrinciple(
            name="Federalism",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            description="The division of power between the federal government and state governments, with each sovereign in its own sphere.",
            elements=["enumerated federal powers", "reserved state powers", "concurrent powers", "preemption doctrine"],
            related_principles=["Tenth Amendment", "Supremacy Clause", "Commerce Clause"],
        ),
        LegalPrinciple(
            name="Strict Scrutiny",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            description="The most rigorous standard of judicial review: the government must show a compelling interest and the law must be narrowly tailored and use the least restrictive means.",
            elements=["compelling governmental interest", "narrowly tailored", "least restrictive means"],
            related_principles=["intermediate scrutiny", "rational basis review"],
        ),
        LegalPrinciple(
            name="State Action Doctrine",
            domain=LegalDomain.CONSTITUTIONAL_LAW,
            description="Constitutional protections generally apply only against government action, not private conduct.",
            elements=["government actor", "state involvement or direction", "public function"],
            exceptions=["public function exception", "entanglement exception", "compulsion test"],
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
        Statute(
            name="Uniform Residential Landlord and Tenant Act",
            code="URLTA",
            section="Various",
            domain=LegalDomain.PROPERTY_LAW,
            summary="Model act governing residential leases, landlord obligations, tenant rights, security deposits, and eviction procedures.",
        ),
        Statute(
            name="Fair Housing Act",
            code="42 U.S.C.",
            section="§3601",
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Prohibits discrimination in the sale, rental, and financing of housing based on race, color, religion, sex, national origin, familial status, or disability.",
        ),
        Statute(
            name="Eminent Domain (Fifth Amendment Takings Clause)",
            code="U.S. Const.",
            section="Amend. V",
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Private property shall not be taken for public use without just compensation.",
        ),
        Statute(
            name="Uniform Probate Code",
            code="UPC",
            section="Various",
            domain=LegalDomain.PROPERTY_LAW,
            summary="Model act governing wills, trusts, intestate succession, and the administration of decedents' estates.",
        ),
        Statute(
            name="Interstate Land Sales Full Disclosure Act",
            code="15 U.S.C.",
            section="§1701",
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires disclosure of information to purchasers of subdivision land and prohibits fraud in interstate land sales.",
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
        Precedent(
            case_name="Kelo v. City of New London",
            citation="545 U.S. 469",
            year=2005,
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Economic development qualifies as a public use under the Takings Clause, allowing government to exercise eminent domain to transfer property to private developers.",
            ratio_decidendi="Public use in the Takings Clause broadly encompasses public purposes including economic development.",
            relevance_keywords=["eminent", "domain", "taking", "public", "use", "compensation", "property", "government"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Penn Central Transportation Co. v. New York City",
            citation="438 U.S. 104",
            year=1978,
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Government regulation of property may constitute a taking requiring compensation, evaluated through a multi-factor balancing test.",
            ratio_decidendi="Regulatory takings analysis considers economic impact, investment-backed expectations, and character of government action.",
            relevance_keywords=["taking", "regulatory", "zoning", "property", "compensation", "regulation", "investment"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Shelley v. Kraemer",
            citation="334 U.S. 1",
            year=1948,
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Judicial enforcement of racially restrictive covenants constitutes state action violating the Equal Protection Clause.",
            ratio_decidendi="Courts may not enforce private agreements that discriminate on the basis of race.",
            relevance_keywords=["covenant", "restrictive", "race", "discrimination", "property", "equal", "protection", "deed"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Village of Euclid v. Ambler Realty Co.",
            citation="272 U.S. 365",
            year=1926,
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Zoning ordinances that divide a municipality into use districts are a valid exercise of police power.",
            ratio_decidendi="Comprehensive zoning is constitutional as a reasonable exercise of police power to promote public welfare.",
            relevance_keywords=["zoning", "land", "use", "police", "power", "regulation", "property", "municipal"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Javins v. First National Realty Corp.",
            citation="428 F.2d 1071",
            year=1970,
            domain=LegalDomain.PROPERTY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="There is an implied warranty of habitability in residential leases; a landlord must maintain the premises in compliance with housing codes.",
            ratio_decidendi="Modern landlord-tenant law imposes an implied warranty of habitability derived from housing code requirements.",
            relevance_keywords=["lease", "landlord", "tenant", "habitability", "warranty", "housing", "rent", "residential"],
            authority_weight=0.85,
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
        LegalPrinciple(
            name="Quiet Enjoyment",
            domain=LegalDomain.PROPERTY_LAW,
            description="A tenant has the right to use and enjoy leased premises without substantial interference from the landlord.",
            elements=["actual or constructive eviction", "substantial interference", "landlord action or failure to act"],
            related_principles=["implied warranty of habitability", "constructive eviction"],
        ),
        LegalPrinciple(
            name="Rule Against Perpetuities",
            domain=LegalDomain.PROPERTY_LAW,
            description="No interest in property is valid unless it must vest, if at all, not later than twenty-one years after some life in being at the creation of the interest.",
            elements=["future interest", "vesting requirement", "measuring life", "twenty-one year period"],
            exceptions=["charitable trusts", "statutory reforms (wait-and-see)", "Uniform Statutory Rule Against Perpetuities"],
        ),
        LegalPrinciple(
            name="Easements and Servitudes",
            domain=LegalDomain.PROPERTY_LAW,
            description="A non-possessory right to use another's land for a specific purpose, which may be created by express grant, implication, necessity, or prescription.",
            elements=["dominant and servient estates", "express grant or reservation", "implication", "necessity", "prescription"],
            exceptions=["abandonment", "merger", "release", "estoppel"],
        ),
        LegalPrinciple(
            name="Implied Warranty of Habitability",
            domain=LegalDomain.PROPERTY_LAW,
            description="In residential leases, landlords impliedly warrant that the premises are fit for human habitation and comply with applicable building and housing codes.",
            elements=["residential lease", "substantial defect affecting habitability", "notice to landlord", "reasonable time to repair"],
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
        Statute(
            name="Americans with Disabilities Act",
            code="42 U.S.C.",
            section="\u00a712101",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Prohibits discrimination against individuals with disabilities in employment, requiring reasonable accommodations.",
        ),
        Statute(
            name="Age Discrimination in Employment Act",
            code="29 U.S.C.",
            section="\u00a7621",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Prohibits employment discrimination against persons 40 years of age or older.",
        ),
        Statute(
            name="Family and Medical Leave Act",
            code="29 U.S.C.",
            section="\u00a72601",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Entitles eligible employees to take unpaid, job-protected leave for specified family and medical reasons.",
        ),
        Statute(
            name="National Labor Relations Act",
            code="29 U.S.C.",
            section="\u00a7151",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Protects the rights of employees to organize, bargain collectively, and engage in concerted activities.",
        ),
        Statute(
            name="Occupational Safety and Health Act",
            code="29 U.S.C.",
            section="\u00a7651",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires employers to provide safe and healthful working conditions and establishes OSHA to set and enforce standards.",
        ),
        Statute(
            name="Worker Adjustment and Retraining Notification Act",
            code="29 U.S.C.",
            section="\u00a72101",
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires employers with 100+ employees to give 60 days advance notice of plant closings and mass layoffs.",
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
        Precedent(
            case_name="Griggs v. Duke Power Co.",
            citation="401 U.S. 424",
            year=1971,
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Employment practices that are facially neutral but discriminatory in operation violate Title VII unless justified by business necessity.",
            ratio_decidendi="Disparate impact theory: neutral practices with discriminatory effects are unlawful absent business necessity.",
            relevance_keywords=["disparate", "impact", "discrimination", "employment", "testing", "business", "necessity", "neutral"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Meritor Savings Bank v. Vinson",
            citation="477 U.S. 57",
            year=1986,
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Sexual harassment that creates a hostile work environment constitutes sex discrimination under Title VII.",
            ratio_decidendi="Title VII is violated when the workplace is permeated with discriminatory intimidation that alters conditions of employment.",
            relevance_keywords=["sexual", "harassment", "hostile", "work", "environment", "discrimination", "Title", "VII"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Burlington Industries v. Ellerth",
            citation="524 U.S. 742",
            year=1998,
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="An employer is vicariously liable for harassment by a supervisor, but may assert an affirmative defense based on reasonable preventive measures.",
            ratio_decidendi="Employer liability for supervisor harassment can be avoided by showing reasonable prevention and the employee's failure to use corrective opportunities.",
            relevance_keywords=["harassment", "supervisor", "employer", "liability", "affirmative", "defense", "prevention"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="NLRB v. Jones & Laughlin Steel Corp.",
            citation="301 U.S. 1",
            year=1937,
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The National Labor Relations Act is a valid exercise of Congress's Commerce Clause power; employees have the right to organize and bargain collectively.",
            ratio_decidendi="The right of employees to self-organization and collective bargaining is a fundamental right protected by federal law.",
            relevance_keywords=["union", "collective", "bargaining", "organize", "labor", "NLRA", "right", "employee"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Oncale v. Sundowner Offshore Services",
            citation="523 U.S. 75",
            year=1998,
            domain=LegalDomain.EMPLOYMENT_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Same-sex sexual harassment is actionable under Title VII.",
            ratio_decidendi="Title VII protects against discrimination because of sex regardless of whether the harasser and victim are the same sex.",
            relevance_keywords=["harassment", "same-sex", "discrimination", "Title", "VII", "workplace", "sex"],
            authority_weight=0.80,
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
        LegalPrinciple(
            name="Disparate Treatment",
            domain=LegalDomain.EMPLOYMENT_LAW,
            description="Intentional discrimination in employment on the basis of a protected characteristic, proven through direct evidence or the McDonnell Douglas burden-shifting framework.",
            elements=["protected class membership", "adverse employment action", "similarly situated comparators", "discriminatory intent"],
        ),
        LegalPrinciple(
            name="Disparate Impact",
            domain=LegalDomain.EMPLOYMENT_LAW,
            description="Facially neutral employment practices that disproportionately affect a protected group are unlawful unless justified by business necessity.",
            elements=["neutral policy or practice", "disproportionate adverse effect on protected group", "lack of business necessity"],
            exceptions=["bona fide occupational qualification", "validated job-related testing"],
        ),
        LegalPrinciple(
            name="Reasonable Accommodation",
            domain=LegalDomain.EMPLOYMENT_LAW,
            description="Employers must make reasonable accommodations for qualified individuals with disabilities or sincerely held religious beliefs, unless it would cause undue hardship.",
            elements=["qualified individual", "disability or religious belief", "interactive process", "reasonable modification"],
            exceptions=["undue hardship", "direct threat to safety"],
        ),
        LegalPrinciple(
            name="Whistleblower Protection",
            domain=LegalDomain.EMPLOYMENT_LAW,
            description="Employees who report illegal activity or refuse to participate in unlawful conduct are protected from retaliation by their employer.",
            elements=["protected activity (reporting or refusal)", "adverse employment action", "causal connection"],
            related_principles=["public policy exception to at-will employment"],
        ),
        LegalPrinciple(
            name="Respondeat Superior in Employment",
            latin_name="Respondeat Superior",
            domain=LegalDomain.EMPLOYMENT_LAW,
            description="An employer is liable for the wrongful acts of an employee committed within the scope of employment.",
            elements=["employer-employee relationship", "scope of employment", "wrongful act"],
            exceptions=["independent contractors", "frolic and detour", "intentional torts outside scope"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# CORPORATE LAW
# ======================================================================


def _get_corporate_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Delaware General Corporation Law",
            code="DGCL",
            section="Title 8",
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.STATE,
            summary="Primary statute governing corporate formation, governance, and fiduciary duties in Delaware.",
        ),
        Statute(
            name="Securities Exchange Act of 1934",
            code="15 U.S.C.",
            section="\u00a778a",
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Regulates secondary trading of securities, including insider trading and corporate disclosure.",
        ),
        Statute(
            name="Securities Act of 1933",
            code="15 U.S.C.",
            section="\u00a777a",
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires registration of securities offerings and mandates disclosure of material information to investors.",
        ),
        Statute(
            name="Sarbanes-Oxley Act",
            code="15 U.S.C.",
            section="\u00a77201",
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Enacted after corporate scandals to mandate reforms in financial disclosure, corporate governance, and auditor independence for public companies.",
        ),
        Statute(
            name="Model Business Corporation Act",
            code="MBCA",
            section="Various",
            domain=LegalDomain.CORPORATE_LAW,
            summary="Model statute adopted by many states providing a framework for corporate governance, shareholder rights, and director duties.",
        ),
        Statute(
            name="Dodd-Frank Wall Street Reform Act",
            code="12 U.S.C.",
            section="\u00a75301",
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Comprehensive financial regulatory reform addressing systemic risk, executive compensation, shareholder say-on-pay, and enhanced corporate governance.",
        ),
        Statute(
            name="Uniform Limited Liability Company Act",
            code="ULLCA",
            section="Various",
            domain=LegalDomain.CORPORATE_LAW,
            summary="Model act governing the formation, operation, and dissolution of limited liability companies.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Dodge v. Ford Motor Co.",
            citation="204 Mich. 459",
            year=1919,
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="A corporation is organized primarily for the profit of stockholders; directors cannot use corporate funds for purely charitable purposes against shareholder interests.",
            ratio_decidendi="Directors owe a fiduciary duty to maximize shareholder value.",
            relevance_keywords=["shareholder", "fiduciary", "duty", "profit", "directors", "corporate", "dividend"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Smith v. Van Gorkom",
            citation="488 A.2d 858",
            year=1985,
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="Directors who approve a merger without adequate deliberation breach their duty of care.",
            ratio_decidendi="The business judgment rule does not protect uninformed decisions.",
            relevance_keywords=["duty", "care", "merger", "business", "judgment", "directors", "informed"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Revlon Inc. v. MacAndrews & Forbes",
            citation="506 A.2d 173",
            year=1986,
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="Once a sale of the company becomes inevitable, directors must act as auctioneers to obtain the best price for shareholders.",
            ratio_decidendi="Revlon duties: board must maximize shareholder value in a change of control.",
            relevance_keywords=["sale", "auction", "shareholder", "price", "merger", "acquisition", "control"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="SEC v. Texas Gulf Sulphur Co.",
            citation="401 F.2d 833",
            year=1968,
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Corporate insiders must disclose material non-public information before trading or abstain from trading.",
            ratio_decidendi="The disclose-or-abstain rule prohibits trading on material non-public information.",
            relevance_keywords=["insider", "trading", "disclosure", "material", "nonpublic", "information", "securities"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Weinberger v. UOP Inc.",
            citation="457 A.2d 701",
            year=1983,
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="In a parent-subsidiary merger, the entire fairness standard applies, requiring fair dealing and fair price.",
            ratio_decidendi="Controlling shareholders in freeze-out mergers must demonstrate entire fairness: fair process and fair price.",
            relevance_keywords=["merger", "fairness", "controlling", "shareholder", "freeze-out", "price", "fiduciary", "minority"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="In re Caremark International Inc. Derivative Litigation",
            citation="698 A.2d 959",
            year=1996,
            domain=LegalDomain.CORPORATE_LAW,
            jurisdiction=JurisdictionType.STATE,
            holding="Directors have a duty to implement and monitor compliance systems; failure to do so in good faith can breach the duty of loyalty.",
            ratio_decidendi="The duty of oversight requires directors to assure adequate information and reporting systems exist.",
            relevance_keywords=["oversight", "compliance", "monitoring", "duty", "loyalty", "good", "faith", "directors", "board"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Business Judgment Rule",
            domain=LegalDomain.CORPORATE_LAW,
            description="Courts defer to the business decisions of directors made in good faith, on an informed basis, and in the honest belief that the action was in the company's best interest.",
            elements=["good faith", "informed decision", "no self-dealing", "rational business purpose"],
            exceptions=["waste of corporate assets", "fraud", "self-dealing", "uninformed decisions"],
        ),
        LegalPrinciple(
            name="Fiduciary Duty of Loyalty",
            domain=LegalDomain.CORPORATE_LAW,
            description="Directors and officers must act in the best interests of the corporation and its shareholders, not in their own self-interest.",
            elements=["duty to corporation", "no self-dealing", "corporate opportunity doctrine"],
        ),
        LegalPrinciple(
            name="Piercing the Corporate Veil",
            domain=LegalDomain.CORPORATE_LAW,
            description="Courts may disregard the corporate entity and hold shareholders personally liable when the corporate form is used to perpetrate fraud or injustice.",
            elements=["alter ego", "undercapitalization", "commingling of assets", "fraud or injustice"],
        ),
        LegalPrinciple(
            name="Entire Fairness Standard",
            domain=LegalDomain.CORPORATE_LAW,
            description="In conflicted transactions involving controlling shareholders or interested directors, the transaction must be entirely fair in both process and price.",
            elements=["fair dealing (process)", "fair price (economics)", "burden on fiduciary to prove fairness"],
            related_principles=["business judgment rule", "fiduciary duty of loyalty"],
        ),
        LegalPrinciple(
            name="Corporate Opportunity Doctrine",
            domain=LegalDomain.CORPORATE_LAW,
            description="Officers and directors may not usurp business opportunities that belong to the corporation without first offering them to the company.",
            elements=["opportunity in corporation's line of business", "financial ability to take advantage", "interest or expectancy of the corporation", "conflict of duty and self-interest"],
        ),
        LegalPrinciple(
            name="Shareholder Derivative Action",
            domain=LegalDomain.CORPORATE_LAW,
            description="A shareholder may bring suit on behalf of the corporation to enforce a corporate right when the board refuses to act, subject to demand requirements.",
            elements=["demand on board or demand futility", "contemporaneous ownership", "adequate representation", "corporate right being enforced"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# INTELLECTUAL PROPERTY LAW
# ======================================================================


def _get_ip_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Patent Act",
            code="35 U.S.C.",
            section="Various",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs patent applications, examination, and enforcement of patent rights.",
        ),
        Statute(
            name="Copyright Act of 1976",
            code="17 U.S.C.",
            section="Various",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Provides protection for original works of authorship including fair use doctrine.",
        ),
        Statute(
            name="Lanham Act (Trademark Act)",
            code="15 U.S.C.",
            section="\u00a71051",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Federal statute governing trademarks, service marks, and unfair competition.",
        ),
        Statute(
            name="Defend Trade Secrets Act",
            code="18 U.S.C.",
            section="\u00a71836",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Creates a federal civil cause of action for trade secret misappropriation.",
        ),
        Statute(
            name="Digital Millennium Copyright Act",
            code="17 U.S.C.",
            section="\u00a71201",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Criminalizes circumvention of digital rights management and provides safe harbors for online service providers regarding user-posted infringing content.",
        ),
        Statute(
            name="America Invents Act",
            code="35 U.S.C.",
            section="\u00a7100 (amended)",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Converted the U.S. patent system from first-to-invent to first-inventor-to-file and created inter partes review proceedings.",
        ),
        Statute(
            name="Uniform Trade Secrets Act",
            code="UTSA",
            section="Various",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            summary="Model state law providing a legal framework for trade secret protection, defining misappropriation and available remedies.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Alice Corp. v. CLS Bank International",
            citation="573 U.S. 208",
            year=2014,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Claims directed to abstract ideas implemented on generic computers are not patent-eligible under 35 U.S.C. 101.",
            ratio_decidendi="A two-step framework determines patent eligibility: (1) is the claim directed to an abstract idea? (2) does it contain an inventive concept?",
            relevance_keywords=["patent", "abstract", "idea", "eligible", "software", "computer", "inventive"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Campbell v. Acuff-Rose Music",
            citation="510 U.S. 569",
            year=1994,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="A commercial parody can qualify as fair use under the Copyright Act.",
            ratio_decidendi="Fair use analysis requires consideration of all four statutory factors; transformative use weighs in favor of fair use.",
            relevance_keywords=["copyright", "fair", "use", "parody", "transformative", "infringement"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="eBay Inc. v. MercExchange",
            citation="547 U.S. 388",
            year=2006,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The traditional four-factor test for injunctive relief applies in patent cases; injunctions are not automatic upon finding infringement.",
            ratio_decidendi="Patent holders are not entitled to automatic injunctions; courts must apply the standard equitable test.",
            relevance_keywords=["patent", "injunction", "infringement", "equitable", "remedy", "irreparable", "harm"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="KSR International Co. v. Teleflex Inc.",
            citation="550 U.S. 398",
            year=2007,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The obviousness analysis under 35 U.S.C. 103 should use a flexible, expansive approach, not the rigid teaching-suggestion-motivation test.",
            ratio_decidendi="A combination of prior art elements may be obvious if a person of ordinary skill would have reason to combine them.",
            relevance_keywords=["patent", "obviousness", "prior", "art", "combination", "inventive", "skill", "103"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Qualitex Co. v. Jacobson Products Co.",
            citation="514 U.S. 159",
            year=1995,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Color alone can serve as a legally protectable trademark when it has acquired secondary meaning.",
            ratio_decidendi="The Lanham Act permits the registration of any symbol that identifies and distinguishes goods, including color.",
            relevance_keywords=["trademark", "color", "secondary", "meaning", "distinctive", "trade", "dress", "registration"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Google LLC v. Oracle America Inc.",
            citation="593 U.S. 1",
            year=2021,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Google's copying of the Java SE API declaring code was a fair use as a matter of law.",
            ratio_decidendi="Copying of software interfaces for reimplementation purposes can constitute transformative fair use, especially when it enables new creative expression on a different platform.",
            relevance_keywords=["copyright", "software", "API", "fair", "use", "transformative", "code", "interface"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Feist Publications v. Rural Telephone Service",
            citation="499 U.S. 340",
            year=1991,
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Facts are not copyrightable; a minimum degree of creativity is required for copyright protection.",
            ratio_decidendi="The Constitution requires originality for copyright; the sweat of the brow doctrine is rejected.",
            relevance_keywords=["copyright", "originality", "facts", "compilation", "creativity", "database", "threshold"],
            authority_weight=0.90,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Fair Use Doctrine",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            description="Permits limited use of copyrighted material without permission for purposes such as criticism, commentary, news reporting, teaching, and research.",
            elements=[
                "purpose and character of use (commercial vs. educational)",
                "nature of the copyrighted work",
                "amount and substantiality of portion used",
                "effect on the market for the original work",
            ],
        ),
        LegalPrinciple(
            name="Trade Secret Protection",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            description="Information that derives economic value from not being generally known and is subject to reasonable secrecy efforts is protectable as a trade secret.",
            elements=["economic value from secrecy", "not generally known", "reasonable efforts to maintain secrecy"],
            exceptions=["reverse engineering", "independent development", "public disclosure"],
        ),
        LegalPrinciple(
            name="First Sale Doctrine",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            description="Once a copyrighted work or patented item is lawfully sold, the rights holder cannot control subsequent resales.",
            elements=["authorized first sale", "lawful acquisition", "physical or digital copy"],
        ),
        LegalPrinciple(
            name="Patent Claim Construction",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            description="The scope of a patent is defined by its claims, which are construed by courts to determine what the patent covers and whether infringement has occurred.",
            elements=["claim language", "specification and prosecution history", "ordinary meaning to person of skill in the art"],
            related_principles=["doctrine of equivalents", "prosecution history estoppel"],
        ),
        LegalPrinciple(
            name="Trademark Likelihood of Confusion",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            description="Trademark infringement occurs when a mark is used in commerce in a way that is likely to cause confusion as to the source, sponsorship, or affiliation of goods or services.",
            elements=["similarity of marks", "similarity of goods/services", "strength of the mark", "evidence of actual confusion", "intent of the alleged infringer", "marketing channels"],
        ),
        LegalPrinciple(
            name="Doctrine of Equivalents",
            domain=LegalDomain.INTELLECTUAL_PROPERTY,
            description="A product may infringe a patent even if it does not literally satisfy every claim limitation, if it performs substantially the same function in substantially the same way to achieve substantially the same result.",
            elements=["same function", "same way", "same result", "insubstantial differences"],
            exceptions=["prosecution history estoppel", "prior art limitation", "disclosure-dedication rule"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# FAMILY LAW
# ======================================================================


def _get_family_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Uniform Child Custody Jurisdiction and Enforcement Act",
            code="UCCJEA",
            section="Various",
            domain=LegalDomain.FAMILY_LAW,
            summary="Determines which state has jurisdiction over child custody disputes.",
        ),
        Statute(
            name="Uniform Marriage and Divorce Act",
            code="UMDA",
            section="Various",
            domain=LegalDomain.FAMILY_LAW,
            summary="Model act governing marriage formation, divorce grounds, property division, and spousal support.",
        ),
        Statute(
            name="Child Support Enforcement Act",
            code="42 U.S.C.",
            section="\u00a7651",
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Establishes a federal-state program for locating absent parents, establishing paternity, and enforcing child support obligations.",
        ),
        Statute(
            name="Indian Child Welfare Act",
            code="25 U.S.C.",
            section="\u00a71901",
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Establishes federal standards for the removal and placement of Native American children in foster or adoptive homes, prioritizing placement with extended family or tribal members.",
        ),
        Statute(
            name="Uniform Premarital Agreement Act",
            code="UPAA",
            section="Various",
            domain=LegalDomain.FAMILY_LAW,
            summary="Provides a uniform framework for the enforceability of premarital agreements, including requirements for voluntariness and disclosure.",
        ),
        Statute(
            name="Parental Kidnapping Prevention Act",
            code="28 U.S.C.",
            section="\u00a71738A",
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires states to enforce and not modify custody determinations made by the child's home state.",
        ),
        Statute(
            name="Adoption and Safe Families Act",
            code="42 U.S.C.",
            section="\u00a7671",
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Promotes the adoption of children in foster care by establishing timelines for permanency hearings and termination of parental rights.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Troxel v. Granville",
            citation="530 U.S. 57",
            year=2000,
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Parents have a fundamental right to make decisions concerning the care, custody, and control of their children.",
            ratio_decidendi="Due process protects the fundamental right of parents to direct the upbringing of their children.",
            relevance_keywords=["parental", "rights", "custody", "children", "visitation", "fundamental", "care"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Palmore v. Sidoti",
            citation="466 U.S. 429",
            year=1984,
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="A court cannot consider the race of the parties or community prejudice when determining child custody.",
            ratio_decidendi="The Equal Protection Clause prohibits giving effect to private racial biases in custody determinations.",
            relevance_keywords=["custody", "race", "discrimination", "equal", "protection", "child", "best", "interest"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Boddie v. Connecticut",
            citation="401 U.S. 371",
            year=1971,
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Filing fees that effectively deny indigent persons access to divorce proceedings violate the Due Process Clause.",
            ratio_decidendi="Due process requires that the state not deny access to its courts for the dissolution of marriage based on inability to pay fees.",
            relevance_keywords=["divorce", "access", "court", "due", "process", "indigent", "filing", "fees"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Santosky v. Kramer",
            citation="455 U.S. 745",
            year=1982,
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The state must support its allegations of parental unfitness by at least clear and convincing evidence before terminating parental rights.",
            ratio_decidendi="The Due Process Clause requires the clear and convincing evidence standard in proceedings to terminate parental rights.",
            relevance_keywords=["parental", "rights", "termination", "due", "process", "evidence", "clear", "convincing"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Turner v. Rogers",
            citation="564 U.S. 431",
            year=2011,
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Due process does not automatically require appointment of counsel in civil contempt proceedings for child support enforcement, but does require alternative procedural safeguards.",
            ratio_decidendi="When an unrepresented person faces incarceration for civil contempt in support cases, the court must provide procedural safeguards to determine ability to pay.",
            relevance_keywords=["child", "support", "contempt", "counsel", "due", "process", "incarceration", "ability", "pay"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Zablocki v. Redhail",
            citation="434 U.S. 374",
            year=1978,
            domain=LegalDomain.FAMILY_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The right to marry is a fundamental right; statutes that significantly interfere with it are subject to strict scrutiny.",
            ratio_decidendi="Marriage is a fundamental liberty protected by the Equal Protection Clause; restrictions must be narrowly tailored to compelling interests.",
            relevance_keywords=["marriage", "fundamental", "right", "equal", "protection", "liberty", "restriction"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Best Interest of the Child",
            domain=LegalDomain.FAMILY_LAW,
            description="In custody and child welfare proceedings, the primary consideration is the best interest and welfare of the child.",
            elements=[
                "child's wishes (if of sufficient age)",
                "emotional ties with each parent",
                "stability of home environment",
                "mental and physical health of parties",
            ],
        ),
        LegalPrinciple(
            name="Equitable Distribution",
            domain=LegalDomain.FAMILY_LAW,
            description="Marital property is divided equitably (though not necessarily equally) upon divorce based on various factors.",
            elements=["length of marriage", "contributions of each spouse", "economic circumstances", "future earning capacity"],
        ),
        LegalPrinciple(
            name="Parens Patriae",
            latin_name="Parens Patriae",
            domain=LegalDomain.FAMILY_LAW,
            description="The state has the authority and responsibility to protect persons who cannot protect themselves, particularly children.",
            elements=["state protective authority", "incapacity of protected person", "best interest standard"],
            related_principles=["best interest of the child", "police power"],
        ),
        LegalPrinciple(
            name="Marital Privilege",
            domain=LegalDomain.FAMILY_LAW,
            description="Spouses have the privilege to refuse to testify against each other and to prevent disclosure of confidential marital communications.",
            elements=["valid marriage", "confidential communication", "during marriage"],
            exceptions=["crimes against spouse or children", "joint participation in crime"],
            related_principles=["spousal immunity", "marital communications privilege"],
        ),
        LegalPrinciple(
            name="Spousal Support (Alimony)",
            domain=LegalDomain.FAMILY_LAW,
            description="A court may order one spouse to provide financial support to the other after divorce based on need, ability to pay, and the standard of living during the marriage.",
            elements=["need of recipient spouse", "ability of paying spouse", "duration of marriage", "standard of living", "contributions to marriage"],
        ),
        LegalPrinciple(
            name="Presumption of Paternity",
            domain=LegalDomain.FAMILY_LAW,
            description="A man is presumed to be the father of a child born during marriage or within a statutory period after divorce.",
            elements=["marriage at time of birth", "acknowledgment of paternity", "genetic testing"],
            exceptions=["rebuttal by genetic evidence", "estoppel", "best interest of child override"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# EVIDENCE LAW
# ======================================================================


def _get_evidence_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Federal Rules of Evidence",
            code="FRE",
            section="Various",
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs the admissibility and presentation of evidence in federal court proceedings.",
        ),
        Statute(
            name="FRE Rule 702 - Expert Testimony",
            code="FRE",
            section="Rule 702",
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="A witness qualified as an expert may testify in the form of an opinion if the testimony is based on sufficient facts, reliable principles, and reliable application.",
        ),
        Statute(
            name="FRE Rule 403 - Exclusion of Relevant Evidence",
            code="FRE",
            section="Rule 403",
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Relevant evidence may be excluded if its probative value is substantially outweighed by danger of unfair prejudice, confusing issues, misleading the jury, undue delay, or needlessly presenting cumulative evidence.",
        ),
        Statute(
            name="FRE Rule 801-807 - Hearsay",
            code="FRE",
            section="Rules 801-807",
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Defines hearsay and its exceptions, including present sense impression, excited utterance, business records, former testimony, and residual exception.",
        ),
        Statute(
            name="FRE Rule 404 - Character Evidence",
            code="FRE",
            section="Rule 404",
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Evidence of a person's character or character trait is not admissible to prove that on a particular occasion the person acted in accordance with the character or trait, with enumerated exceptions.",
        ),
        Statute(
            name="Stored Communications Act",
            code="18 U.S.C.",
            section="\u00a72701",
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs government access to stored electronic communications and subscriber records held by third-party service providers.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Daubert v. Merrell Dow Pharmaceuticals",
            citation="509 U.S. 579",
            year=1993,
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Trial judges serve as gatekeepers for expert testimony, which must be based on reliable scientific methodology.",
            ratio_decidendi="Expert testimony must be both relevant and reliable under FRE 702.",
            relevance_keywords=["expert", "testimony", "scientific", "reliable", "evidence", "admissibility", "methodology"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Kumho Tire Co. v. Carmichael",
            citation="526 U.S. 137",
            year=1999,
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Daubert gatekeeping obligation applies to all expert testimony, not just scientific testimony.",
            ratio_decidendi="The trial judge's gatekeeping function for reliability applies to technical and specialized knowledge experts as well.",
            relevance_keywords=["expert", "testimony", "Daubert", "technical", "reliability", "gatekeeping", "specialized"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Crawford v. Washington",
            citation="541 U.S. 36",
            year=2004,
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Confrontation Clause bars admission of testimonial hearsay unless the declarant is unavailable and the defendant had a prior opportunity to cross-examine.",
            ratio_decidendi="The Sixth Amendment requires confrontation of witnesses who provide testimonial statements, not merely a judicial reliability determination.",
            relevance_keywords=["confrontation", "hearsay", "testimonial", "cross-examine", "sixth", "amendment", "witness"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Frye v. United States",
            citation="293 F. 1013",
            year=1923,
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Expert testimony based on a scientific technique is admissible only when the technique is generally accepted in the relevant scientific community.",
            ratio_decidendi="The general acceptance test determines the admissibility of novel scientific evidence.",
            relevance_keywords=["expert", "scientific", "general", "acceptance", "evidence", "admissibility", "technique"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Melendez-Diaz v. Massachusetts",
            citation="557 U.S. 305",
            year=2009,
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Forensic lab reports are testimonial in nature and their admission without the analyst's testimony violates the Confrontation Clause.",
            ratio_decidendi="Certificates of analysis are testimonial statements; the accused has the right to confront the analyst who prepared them.",
            relevance_keywords=["forensic", "lab", "report", "testimonial", "confrontation", "analyst", "certificate"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Carpenter v. United States",
            citation="585 U.S. 296",
            year=2018,
            domain=LegalDomain.EVIDENCE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The government's acquisition of historical cell-site location information constitutes a Fourth Amendment search requiring a warrant.",
            ratio_decidendi="Individuals maintain a reasonable expectation of privacy in the comprehensive record of their physical movements captured through cell phone records.",
            relevance_keywords=["privacy", "digital", "cell", "phone", "location", "warrant", "fourth", "amendment", "search"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Hearsay Rule",
            domain=LegalDomain.EVIDENCE_LAW,
            description="Out-of-court statements offered to prove the truth of the matter asserted are generally inadmissible.",
            elements=["out-of-court statement", "offered for truth", "declarant not present"],
            exceptions=["present sense impression", "excited utterance", "business records", "dying declaration", "statement against interest"],
        ),
        LegalPrinciple(
            name="Relevance and Prejudice Balancing",
            domain=LegalDomain.EVIDENCE_LAW,
            description="Relevant evidence may be excluded if its probative value is substantially outweighed by the danger of unfair prejudice.",
            elements=["probative value", "unfair prejudice", "confusion of issues", "misleading the jury"],
        ),
        LegalPrinciple(
            name="Best Evidence Rule",
            domain=LegalDomain.EVIDENCE_LAW,
            description="To prove the content of a writing, recording, or photograph, the original is required unless it is unavailable through no fault of the proponent.",
            elements=["content of writing, recording, or photograph at issue", "original required", "duplicates generally admissible"],
            exceptions=["original lost or destroyed", "original not obtainable", "collateral matters"],
        ),
        LegalPrinciple(
            name="Attorney-Client Privilege",
            domain=LegalDomain.EVIDENCE_LAW,
            description="Confidential communications between a client and attorney made for the purpose of obtaining legal advice are privileged and protected from compelled disclosure.",
            elements=["attorney-client relationship", "confidential communication", "purpose of obtaining legal advice"],
            exceptions=["crime-fraud exception", "waiver by disclosure", "fiduciary exception"],
        ),
        LegalPrinciple(
            name="Work Product Doctrine",
            domain=LegalDomain.EVIDENCE_LAW,
            description="Materials prepared by or for an attorney in anticipation of litigation are generally protected from discovery.",
            elements=["prepared in anticipation of litigation", "by or for attorney or representative", "documents and tangible things"],
            exceptions=["substantial need and undue hardship", "mental impressions (opinion work product - near absolute)"],
            related_principles=["attorney-client privilege"],
        ),
        LegalPrinciple(
            name="Burden of Proof",
            domain=LegalDomain.EVIDENCE_LAW,
            description="The obligation on a party to establish a fact in issue by the required standard of proof, varying by the type of proceeding.",
            elements=["preponderance of evidence (civil)", "clear and convincing evidence (intermediate)", "beyond a reasonable doubt (criminal)"],
            related_principles=["presumption of innocence", "burden of production vs. persuasion"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# ADMINISTRATIVE LAW
# ======================================================================


def _get_administrative_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Administrative Procedure Act",
            code="5 U.S.C.",
            section="\u00a7551",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs the process by which federal agencies develop and issue regulations, including requirements for notice-and-comment rulemaking and adjudication.",
        ),
        Statute(
            name="Freedom of Information Act",
            code="5 U.S.C.",
            section="\u00a7552",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Provides the public with the right to request access to records from any federal agency, subject to nine exemptions.",
        ),
        Statute(
            name="Regulatory Flexibility Act",
            code="5 U.S.C.",
            section="\u00a7601",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires agencies to consider the impact of their regulations on small entities and to explore less burdensome alternatives.",
        ),
        Statute(
            name="Federal Advisory Committee Act",
            code="5 U.S.C. App.",
            section="Various",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs the creation and operation of advisory committees in the executive branch, requiring openness and balanced representation.",
        ),
        Statute(
            name="Government in the Sunshine Act",
            code="5 U.S.C.",
            section="\u00a7552b",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires multi-member federal agencies to open their meetings to public observation, with limited exceptions.",
        ),
        Statute(
            name="Congressional Review Act",
            code="5 U.S.C.",
            section="\u00a7801",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Allows Congress to review and disapprove major rules issued by federal agencies through an expedited joint resolution of disapproval.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Chevron U.S.A. Inc. v. Natural Resources Defense Council",
            citation="467 U.S. 837",
            year=1984,
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Courts must defer to an agency's reasonable interpretation of an ambiguous statute that the agency administers.",
            ratio_decidendi="The two-step Chevron framework: (1) Has Congress directly spoken? (2) If not, is the agency's interpretation reasonable?",
            relevance_keywords=["deference", "agency", "interpretation", "statute", "ambiguous", "regulation", "rulemaking"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Motor Vehicle Manufacturers Association v. State Farm Mutual",
            citation="463 U.S. 29",
            year=1983,
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Agency action is arbitrary and capricious if the agency failed to consider important aspects of the problem, offered an explanation counter to evidence, or was so implausible it could not be ascribed to a difference in view.",
            ratio_decidendi="Arbitrary and capricious review under APA requires reasoned decision-making and consideration of relevant factors.",
            relevance_keywords=["arbitrary", "capricious", "agency", "rulemaking", "reasoned", "decision", "review", "APA"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Citizens to Preserve Overton Park v. Volpe",
            citation="401 U.S. 402",
            year=1971,
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Courts must conduct a thorough, probing, in-depth review of agency action under the arbitrary and capricious standard.",
            ratio_decidendi="Judicial review of agency action must be searching and careful, based on the full administrative record.",
            relevance_keywords=["judicial", "review", "agency", "arbitrary", "capricious", "record", "administrative"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Mathews v. Eldridge",
            citation="424 U.S. 319",
            year=1976,
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Due process in administrative proceedings requires a balancing test considering private interests, risk of error, and government interests.",
            ratio_decidendi="The three-factor Mathews balancing test determines what process is due before government deprivation of a protected interest.",
            relevance_keywords=["due", "process", "hearing", "administrative", "balancing", "deprivation", "interest", "procedural"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Auer v. Robbins",
            citation="519 U.S. 452",
            year=1997,
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="An agency's interpretation of its own ambiguous regulation is controlling unless plainly erroneous or inconsistent with the regulation.",
            ratio_decidendi="Courts defer to an agency's reasonable interpretation of its own regulations (Auer deference).",
            relevance_keywords=["deference", "agency", "regulation", "interpretation", "ambiguous", "administrative"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="Loper Bright Enterprises v. Raimondo",
            citation="144 S. Ct. 2244",
            year=2024,
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Courts must exercise their independent judgment in deciding whether an agency has acted within its statutory authority, overruling Chevron deference.",
            ratio_decidendi="The APA requires courts to decide all relevant questions of law and interpret statutory provisions, not defer to agency interpretations.",
            relevance_keywords=["Chevron", "overruled", "deference", "agency", "statutory", "interpretation", "judicial", "independent"],
            authority_weight=0.95,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Non-Delegation Doctrine",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            description="Congress may not delegate its legislative power to agencies without providing an intelligible principle to guide the agency's exercise of that authority.",
            elements=["delegation of legislative power", "intelligible principle", "adequate standards and guidelines"],
            exceptions=["broad delegations historically upheld with general standards"],
        ),
        LegalPrinciple(
            name="Exhaustion of Administrative Remedies",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            description="A party must pursue all available administrative remedies before seeking judicial review of an agency action.",
            elements=["available administrative remedy", "final agency action", "completion of agency process"],
            exceptions=["futility", "constitutional challenge", "agency lacks authority"],
        ),
        LegalPrinciple(
            name="Ripeness",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            description="A dispute must be sufficiently developed and present a concrete controversy before a court will review an agency action.",
            elements=["fitness of issues for judicial decision", "hardship to parties from withholding review"],
        ),
        LegalPrinciple(
            name="Arbitrary and Capricious Standard",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            description="Agency action must be based on reasoned decision-making; courts will set aside action that is arbitrary, capricious, an abuse of discretion, or not in accordance with law.",
            elements=["consideration of relevant factors", "rational connection between facts and decision", "no clear error of judgment", "reasoned explanation"],
        ),
        LegalPrinciple(
            name="Notice and Comment Rulemaking",
            domain=LegalDomain.ADMINISTRATIVE_LAW,
            description="Agencies must publish proposed rules in the Federal Register, allow public comment, and consider and respond to significant comments before issuing final rules.",
            elements=["notice of proposed rulemaking", "opportunity for public comment", "concise general statement of basis and purpose"],
            exceptions=["good cause exception", "interpretive rules", "policy statements"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# ENVIRONMENTAL LAW
# ======================================================================


def _get_environmental_law() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="National Environmental Policy Act",
            code="42 U.S.C.",
            section="\u00a74321",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Requires federal agencies to prepare environmental impact statements for major federal actions significantly affecting the quality of the human environment.",
        ),
        Statute(
            name="Clean Air Act",
            code="42 U.S.C.",
            section="\u00a77401",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Regulates air emissions from stationary and mobile sources, establishing national ambient air quality standards and emission limits.",
        ),
        Statute(
            name="Clean Water Act",
            code="33 U.S.C.",
            section="\u00a71251",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Establishes the regulatory framework for discharging pollutants into waters of the United States and regulating quality standards for surface waters.",
        ),
        Statute(
            name="Comprehensive Environmental Response, Compensation, and Liability Act (CERCLA/Superfund)",
            code="42 U.S.C.",
            section="\u00a79601",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Provides for cleanup of hazardous waste sites and imposes strict, joint, and several liability on responsible parties for contamination.",
        ),
        Statute(
            name="Resource Conservation and Recovery Act",
            code="42 U.S.C.",
            section="\u00a76901",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs the disposal of solid and hazardous waste, establishing a cradle-to-grave tracking system for hazardous materials.",
        ),
        Statute(
            name="Endangered Species Act",
            code="16 U.S.C.",
            section="\u00a71531",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Provides for the conservation of species that are endangered or threatened, prohibiting take and requiring habitat protection.",
        ),
        Statute(
            name="Toxic Substances Control Act",
            code="15 U.S.C.",
            section="\u00a72601",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Authorizes EPA to regulate the manufacture, distribution, and use of chemical substances that present unreasonable risk to health or the environment.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="Massachusetts v. EPA",
            citation="549 U.S. 497",
            year=2007,
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The EPA has authority under the Clean Air Act to regulate greenhouse gas emissions from motor vehicles, and its refusal to do so was arbitrary and capricious.",
            ratio_decidendi="Greenhouse gases are air pollutants under the Clean Air Act; EPA must regulate them if they endanger public health.",
            relevance_keywords=["EPA", "greenhouse", "gas", "climate", "clean", "air", "regulate", "emissions", "pollutant"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Lujan v. Defenders of Wildlife",
            citation="504 U.S. 555",
            year=1992,
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Plaintiffs must demonstrate concrete and particularized injury-in-fact, causation, and redressability to establish standing in environmental cases.",
            ratio_decidendi="Article III standing requires a concrete, particularized injury fairly traceable to the defendant and likely redressable by the court.",
            relevance_keywords=["standing", "injury", "fact", "environmental", "causation", "redressability", "concrete"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Rapanos v. United States",
            citation="547 U.S. 715",
            year=2006,
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Clean Water Act's jurisdiction over 'waters of the United States' does not extend to all wetlands with any hydrological connection to navigable waters.",
            ratio_decidendi="The scope of federal jurisdiction over wetlands under the CWA is limited; the significant nexus test applies.",
            relevance_keywords=["wetlands", "waters", "jurisdiction", "clean", "water", "act", "navigable", "nexus"],
            authority_weight=0.80,
        ),
        Precedent(
            case_name="TVA v. Hill",
            citation="437 U.S. 153",
            year=1978,
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Endangered Species Act requires federal agencies to ensure their actions do not jeopardize the continued existence of listed species, even at significant economic cost.",
            ratio_decidendi="The plain intent of Congress in enacting the ESA was to halt and reverse the trend toward species extinction at whatever the cost.",
            relevance_keywords=["endangered", "species", "habitat", "jeopardy", "conservation", "protection", "federal"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Burlington Northern & Santa Fe Railway Co. v. United States",
            citation="556 U.S. 599",
            year=2009,
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="CERCLA liability may be apportioned when there is a reasonable basis for determining the contribution of each party to a single harm.",
            ratio_decidendi="Joint and several liability under CERCLA is not mandatory; courts may apportion liability when harm is divisible.",
            relevance_keywords=["CERCLA", "Superfund", "liability", "contamination", "cleanup", "apportionment", "hazardous"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Sackett v. EPA",
            citation="598 U.S. 651",
            year=2023,
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The Clean Water Act's coverage of 'waters of the United States' extends only to wetlands with a continuous surface connection to traditional navigable waters.",
            ratio_decidendi="Federal jurisdiction under the CWA requires a continuous surface connection between wetlands and navigable waters, narrowing the significant nexus test.",
            relevance_keywords=["wetlands", "waters", "jurisdiction", "CWA", "continuous", "surface", "connection", "navigable"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Polluter Pays Principle",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            description="Those who produce pollution should bear the costs of managing it to prevent damage to human health or the environment.",
            elements=["identification of polluter", "causation of environmental harm", "allocation of cleanup costs"],
            related_principles=["strict liability for hazardous activities", "CERCLA liability"],
        ),
        LegalPrinciple(
            name="Precautionary Principle",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            description="When an activity threatens harm to the environment, precautionary measures should be taken even if some cause-and-effect relationships are not fully established scientifically.",
            elements=["threat of environmental harm", "scientific uncertainty", "precautionary action justified"],
        ),
        LegalPrinciple(
            name="Public Trust Doctrine",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            description="The government holds certain natural resources in trust for public use and must protect them from private appropriation or destruction.",
            elements=["navigable waters and submerged lands", "government as trustee", "public right of access and use"],
        ),
        LegalPrinciple(
            name="Environmental Impact Assessment",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            description="Major federal actions significantly affecting the environment require preparation of an environmental impact statement analyzing potential effects and alternatives.",
            elements=["major federal action", "significant environmental impact", "analysis of alternatives", "public participation"],
        ),
        LegalPrinciple(
            name="Strict Liability for Hazardous Waste",
            domain=LegalDomain.ENVIRONMENTAL_LAW,
            description="Parties responsible for hazardous waste contamination are strictly liable for cleanup costs regardless of fault, with liability that is joint and several.",
            elements=["current or former owner/operator", "arranger for disposal", "transporter", "strict liability regardless of fault"],
            exceptions=["innocent landowner defense", "third-party defense", "act of God"],
        ),
    ]

    return statutes, precedents, principles


# ======================================================================
# CIVIL PROCEDURE
# ======================================================================


def _get_civil_procedure() -> tuple[list[Statute], list[Precedent], list[LegalPrinciple]]:
    statutes = [
        Statute(
            name="Federal Rules of Civil Procedure",
            code="FRCP",
            section="Various",
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Governs the conduct of civil actions in United States federal district courts, including pleading, discovery, trial, and judgment.",
        ),
        Statute(
            name="28 U.S.C. - Federal Question Jurisdiction",
            code="28 U.S.C.",
            section="\u00a71331",
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Federal district courts have original jurisdiction over all civil actions arising under the Constitution, laws, or treaties of the United States.",
        ),
        Statute(
            name="28 U.S.C. - Diversity Jurisdiction",
            code="28 U.S.C.",
            section="\u00a71332",
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Federal courts have jurisdiction over civil actions between citizens of different states when the amount in controversy exceeds $75,000.",
        ),
        Statute(
            name="Class Action Fairness Act",
            code="28 U.S.C.",
            section="\u00a71332(d)",
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Expands federal jurisdiction over class actions with minimal diversity and aggregate amount in controversy exceeding $5 million.",
        ),
        Statute(
            name="Federal Arbitration Act",
            code="9 U.S.C.",
            section="\u00a71",
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Establishes a national policy favoring arbitration and provides for enforcement of arbitration agreements in contracts involving commerce.",
        ),
        Statute(
            name="28 U.S.C. - Removal",
            code="28 U.S.C.",
            section="\u00a71441",
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            summary="Allows defendants to remove civil actions from state court to federal court when the federal court would have had original jurisdiction.",
        ),
    ]

    precedents = [
        Precedent(
            case_name="International Shoe Co. v. Washington",
            citation="326 U.S. 310",
            year=1945,
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="A court may exercise personal jurisdiction over a defendant that has certain minimum contacts with the forum such that maintaining the suit does not offend traditional notions of fair play and substantial justice.",
            ratio_decidendi="The minimum contacts test for personal jurisdiction balances purposeful availment with fairness considerations.",
            relevance_keywords=["jurisdiction", "personal", "minimum", "contacts", "due", "process", "forum", "defendant"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Erie Railroad Co. v. Tompkins",
            citation="304 U.S. 64",
            year=1938,
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="Federal courts sitting in diversity must apply state substantive law and federal procedural law.",
            ratio_decidendi="There is no general federal common law; in diversity cases, state law governs substantive rights.",
            relevance_keywords=["Erie", "diversity", "state", "law", "substantive", "procedural", "federal", "common"],
            authority_weight=0.95,
        ),
        Precedent(
            case_name="Ashcroft v. Iqbal",
            citation="556 U.S. 662",
            year=2009,
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="To survive a motion to dismiss, a complaint must contain sufficient factual matter to state a claim for relief that is plausible on its face.",
            ratio_decidendi="The plausibility standard requires more than a sheer possibility that a defendant acted unlawfully; factual allegations must nudge claims across the line from conceivable to plausible.",
            relevance_keywords=["pleading", "motion", "dismiss", "plausibility", "complaint", "factual", "12(b)(6)"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Bell Atlantic Corp. v. Twombly",
            citation="550 U.S. 544",
            year=2007,
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="A complaint must allege enough facts to state a plausible claim for relief; conclusory allegations and formulaic recitations of elements are insufficient.",
            ratio_decidendi="The plausibility pleading standard replaced the Conley 'no set of facts' standard for evaluating motions to dismiss.",
            relevance_keywords=["pleading", "plausibility", "complaint", "dismiss", "antitrust", "motion", "12(b)(6)", "sufficiency"],
            authority_weight=0.90,
        ),
        Precedent(
            case_name="Celotex Corp. v. Catrett",
            citation="477 U.S. 317",
            year=1986,
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="The moving party on summary judgment need only point out the absence of a genuine issue of material fact; it need not negate the opposing party's claim.",
            ratio_decidendi="Summary judgment is appropriate when the record shows no genuine dispute as to any material fact and the movant is entitled to judgment as a matter of law.",
            relevance_keywords=["summary", "judgment", "material", "fact", "genuine", "dispute", "motion", "evidence"],
            authority_weight=0.85,
        ),
        Precedent(
            case_name="Wal-Mart Stores v. Dukes",
            citation="564 U.S. 338",
            year=2011,
            domain=LegalDomain.CIVIL_PROCEDURE,
            jurisdiction=JurisdictionType.FEDERAL,
            holding="A class action requires proof that all class members suffered the same injury; commonality requires common contention capable of classwide resolution.",
            ratio_decidendi="Rule 23(a) commonality requires that class claims depend on a common contention whose determination will resolve an issue central to each class member's claim.",
            relevance_keywords=["class", "action", "certification", "commonality", "Rule", "23", "class", "members"],
            authority_weight=0.85,
        ),
    ]

    principles = [
        LegalPrinciple(
            name="Personal Jurisdiction",
            domain=LegalDomain.CIVIL_PROCEDURE,
            description="A court must have power over the parties before it can adjudicate their dispute. Personal jurisdiction requires minimum contacts with the forum state such that litigation there is fair.",
            elements=["minimum contacts", "purposeful availment", "fair play and substantial justice", "relatedness of claims to contacts"],
            related_principles=["general jurisdiction", "specific jurisdiction", "long-arm statutes"],
        ),
        LegalPrinciple(
            name="Standing",
            domain=LegalDomain.CIVIL_PROCEDURE,
            description="A party must demonstrate a concrete and particularized injury, fairly traceable to the challenged conduct, and likely redressable by a favorable court decision.",
            elements=["injury in fact", "causation (traceability)", "redressability"],
        ),
        LegalPrinciple(
            name="Res Judicata (Claim Preclusion)",
            latin_name="Res Judicata",
            domain=LegalDomain.CIVIL_PROCEDURE,
            description="A final judgment on the merits bars relitigation of the same claim between the same parties or their privies.",
            elements=["final judgment on the merits", "same claim or cause of action", "same parties or privies"],
            related_principles=["collateral estoppel (issue preclusion)"],
        ),
        LegalPrinciple(
            name="Collateral Estoppel (Issue Preclusion)",
            domain=LegalDomain.CIVIL_PROCEDURE,
            description="Once an issue of fact or law is actually litigated and determined by a valid and final judgment, that determination is conclusive in subsequent litigation.",
            elements=["issue actually litigated", "issue actually decided", "determination essential to judgment", "full and fair opportunity to litigate"],
        ),
        LegalPrinciple(
            name="Forum Non Conveniens",
            latin_name="Forum Non Conveniens",
            domain=LegalDomain.CIVIL_PROCEDURE,
            description="A court may dismiss a case if there is a more appropriate forum available, considering private and public interest factors.",
            elements=["adequate alternative forum", "private interest factors (access to evidence, witnesses)", "public interest factors (court congestion, local interest)"],
        ),
        LegalPrinciple(
            name="Summary Judgment Standard",
            domain=LegalDomain.CIVIL_PROCEDURE,
            description="A court shall grant summary judgment when there is no genuine dispute as to any material fact and the movant is entitled to judgment as a matter of law.",
            elements=["no genuine dispute", "material fact", "movant entitled to judgment as matter of law", "evidence viewed in light most favorable to non-movant"],
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
        _get_corporate_law(),
        _get_ip_law(),
        _get_family_law(),
        _get_evidence_law(),
        _get_administrative_law(),
        _get_environmental_law(),
        _get_civil_procedure(),
    ]


def get_all_statutes() -> list[Statute]:
    return [s for domain in _all_domains() for s in domain[0]]


def get_all_precedents() -> list[Precedent]:
    return [p for domain in _all_domains() for p in domain[1]]


def get_all_principles() -> list[LegalPrinciple]:
    return [p for domain in _all_domains() for p in domain[2]]
