"""CLI entry point for the Legal Judge Bot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from legal_judge.models.case import (
    Argument,
    Case,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)
from legal_judge.output.opinion import OpinionWriter


def _build_demo_contract_case() -> Case:
    """Build a sample contract dispute case for demonstration."""
    return Case(
        case_id="DEMO-2026-001",
        title="Acme Corp v. Widget Industries",
        case_type=CaseType.CONTRACT,
        jurisdiction="General",
        summary="Breach of supply contract with consequential damages claim.",
        parties=[
            Party(
                name="Acme Corp",
                role=PartyRole.PLAINTIFF,
                description="Technology manufacturer",
                counsel="J. Smith, Esq.",
            ),
            Party(
                name="Widget Industries",
                role=PartyRole.DEFENDANT,
                description="Components supplier",
                counsel="A. Johnson, Esq.",
            ),
        ],
        facts=[
            "Acme Corp and Widget Industries entered into a supply contract on January 15, 2025.",
            "Widget Industries agreed to deliver 10,000 units of Component X by March 1, 2025.",
            "Widget Industries failed to deliver by the agreed date.",
            "Acme Corp suffered production delays costing $500,000.",
            "Widget Industries cited supply chain disruptions as the cause of delay.",
            "The contract contained a force majeure clause.",
            "Widget Industries did not formally invoke the force majeure clause within the contractually required 48-hour notice period.",
        ],
        issues=[
            "Whether Widget Industries breached the supply contract",
            "Whether the force majeure clause excuses Widget Industries' non-performance",
            "Whether Acme Corp is entitled to consequential damages",
        ],
        arguments=[
            Argument(
                party_name="Acme Corp",
                claim="Widget Industries materially breached the contract by failing to deliver on time.",
                supporting_facts=[
                    "Delivery deadline was March 1, 2025",
                    "No delivery was made by that date",
                    "No force majeure notice was given within 48 hours",
                ],
                legal_basis=["Breach of contract", "UCC Article 2"],
                cited_precedents=["Hadley v. Baxendale"],
            ),
            Argument(
                party_name="Acme Corp",
                claim="Consequential damages of $500,000 were foreseeable at the time of contracting.",
                supporting_facts=[
                    "Widget Industries knew Acme Corp's production schedule",
                    "Production delays were a natural consequence of non-delivery",
                ],
                legal_basis=["Hadley v. Baxendale foreseeability test"],
                cited_precedents=["Hadley v. Baxendale"],
            ),
            Argument(
                party_name="Widget Industries",
                claim="Supply chain disruptions constitute force majeure excusing performance.",
                supporting_facts=["Global supply chain disruptions occurred in Q1 2025"],
                legal_basis=["Force majeure clause in contract"],
            ),
            Argument(
                party_name="Widget Industries",
                claim="Acme Corp failed to mitigate damages by not seeking alternative suppliers.",
                supporting_facts=["Alternative suppliers were available"],
                legal_basis=["Duty to mitigate"],
            ),
        ],
        evidence=[
            Evidence(
                title="Supply Contract",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Original signed contract between parties with delivery and force majeure terms.",
                submitted_by="Acme Corp",
                credibility_weight=0.95,
                relevance_summary="Establishes contractual obligations and deadlines.",
            ),
            Evidence(
                title="Delivery Records",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Shipping and logistics records showing no delivery attempt before deadline.",
                submitted_by="Acme Corp",
                credibility_weight=0.90,
                relevance_summary="Proves non-delivery by contract deadline.",
            ),
            Evidence(
                title="Production Loss Report",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Audited financial report showing $500,000 in production losses.",
                submitted_by="Acme Corp",
                credibility_weight=0.85,
                relevance_summary="Quantifies consequential damages.",
            ),
            Evidence(
                title="Supply Chain Disruption Report",
                evidence_type=EvidenceType.EXPERT_OPINION,
                description="Industry analyst report on Q1 2025 supply chain issues.",
                submitted_by="Widget Industries",
                credibility_weight=0.60,
                relevance_summary="Supports force majeure defense.",
            ),
            Evidence(
                title="Email Correspondence",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Emails between parties; no force majeure notice sent within 48 hours.",
                submitted_by="Acme Corp",
                credibility_weight=0.90,
                relevance_summary="Shows failure to invoke force majeure per contract terms.",
            ),
        ],
        applicable_statutes=["UCC Article 2", "Restatement (Second) of Contracts"],
    )


def _build_demo_tort_case() -> Case:
    """Build a sample tort/negligence case."""
    return Case(
        case_id="DEMO-2026-002",
        title="Johnson v. SafeRide Transportation",
        case_type=CaseType.TORT,
        jurisdiction="General",
        summary="Negligence claim arising from a ride-sharing vehicle accident.",
        parties=[
            Party(
                name="Maria Johnson",
                role=PartyRole.PLAINTIFF,
                description="Passenger injured during ride-share trip",
                counsel="R. Davis, Esq.",
            ),
            Party(
                name="SafeRide Transportation",
                role=PartyRole.DEFENDANT,
                description="Ride-sharing company",
                counsel="T. Williams, Esq.",
            ),
        ],
        facts=[
            "Maria Johnson booked a ride through SafeRide's app on February 10, 2025.",
            "The assigned driver, employed by SafeRide, ran a red light.",
            "The vehicle collided with another car at the intersection.",
            "Johnson sustained a broken arm and whiplash injuries.",
            "The driver had two prior traffic violations on record.",
            "SafeRide's hiring policy requires a clean driving record.",
            "SafeRide did not perform an updated background check in the past 12 months.",
        ],
        issues=[
            "Whether SafeRide owed a duty of care to Johnson as a passenger",
            "Whether SafeRide was negligent in hiring and supervising the driver",
            "Whether SafeRide is vicariously liable for the driver's negligence",
        ],
        arguments=[
            Argument(
                party_name="Maria Johnson",
                claim="SafeRide breached its duty of care by failing to properly vet and monitor its driver.",
                supporting_facts=[
                    "Driver had prior violations",
                    "No recent background check",
                    "SafeRide's own policy requires clean records",
                ],
                legal_basis=["Negligent hiring", "Duty of care to passengers"],
                cited_precedents=["Donoghue v. Stevenson"],
            ),
            Argument(
                party_name="Maria Johnson",
                claim="SafeRide is vicariously liable for the driver's actions during the scope of employment.",
                supporting_facts=[
                    "Driver was working a SafeRide shift",
                    "Accident occurred during a paid ride",
                ],
                legal_basis=["Respondeat superior"],
            ),
            Argument(
                party_name="SafeRide Transportation",
                claim="The driver was an independent contractor, not an employee.",
                supporting_facts=["Driver agreement classifies drivers as independent contractors"],
                legal_basis=["Independent contractor doctrine"],
            ),
        ],
        evidence=[
            Evidence(
                title="Medical Records",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Hospital records documenting broken arm and whiplash diagnosis.",
                submitted_by="Maria Johnson",
                credibility_weight=0.95,
            ),
            Evidence(
                title="Police Accident Report",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Report confirming driver ran a red light and was at fault.",
                submitted_by="Maria Johnson",
                credibility_weight=0.90,
            ),
            Evidence(
                title="Driver's Record",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="DMV records showing two prior moving violations.",
                submitted_by="Maria Johnson",
                credibility_weight=0.85,
            ),
            Evidence(
                title="SafeRide Hiring Policy",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Company policy requiring clean driving records for all drivers.",
                submitted_by="Maria Johnson",
                credibility_weight=0.80,
            ),
            Evidence(
                title="Driver Contract",
                evidence_type=EvidenceType.DOCUMENTARY,
                description="Agreement between driver and SafeRide classifying driver as independent contractor.",
                submitted_by="SafeRide Transportation",
                credibility_weight=0.70,
            ),
        ],
        applicable_statutes=["Restatement (Third) of Torts"],
    )


def _load_case_from_json(path: str) -> Case:
    """Load a case from a JSON file."""
    data = json.loads(Path(path).read_text())
    return Case(**data)


DEMO_CASES = {
    "contract": _build_demo_contract_case,
    "tort": _build_demo_tort_case,
}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="legal-judge",
        description="Legal Judge Bot - AI-powered legal analysis and judgment engine",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- demo command ---
    demo_parser = subparsers.add_parser("demo", help="Run a demo case")
    demo_parser.add_argument(
        "case_name",
        nargs="?",
        default="contract",
        choices=list(DEMO_CASES.keys()),
        help="Which demo case to run (default: contract)",
    )
    demo_parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Output format (default: text)",
    )

    # --- judge command ---
    judge_parser = subparsers.add_parser("judge", help="Judge a case from a JSON file")
    judge_parser.add_argument("file", help="Path to a JSON case file")
    judge_parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Output format (default: text)",
    )

    # --- info command ---
    subparsers.add_parser("info", help="Show knowledge base info")

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "info":
        _cmd_info()
    elif args.command == "demo":
        case = DEMO_CASES[args.case_name]()
        _cmd_judge(case, args.format)
    elif args.command == "judge":
        case = _load_case_from_json(args.file)
        _cmd_judge(case, args.format)


def _cmd_info() -> None:
    from legal_judge.knowledge.base import KnowledgeBase

    kb = KnowledgeBase.with_defaults()
    print("Legal Judge Bot - Knowledge Base Summary")
    print("=" * 42)
    print(f"  Statutes:   {len(kb.statutes)}")
    print(f"  Precedents: {len(kb.precedents)}")
    print(f"  Principles: {len(kb.principles)}")
    print()
    print("Domains covered:")
    domains = {s.domain.value for s in kb.statutes} | {p.domain.value for p in kb.precedents}
    for d in sorted(domains):
        print(f"  - {d}")


def _cmd_judge(case: Case, fmt: str) -> None:
    writer = OpinionWriter()
    if fmt == "markdown":
        print(writer.render_markdown(case))
    else:
        print(writer.render_text(case))


if __name__ == "__main__":
    main()
