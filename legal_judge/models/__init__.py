"""Data models for legal cases, judgments, and legal concepts."""

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

__all__ = [
    "Argument",
    "Case",
    "CaseStatus",
    "CaseType",
    "Disposition",
    "Evidence",
    "EvidenceType",
    "Judgment",
    "JudgmentSection",
    "JurisdictionType",
    "LegalDomain",
    "LegalPrinciple",
    "Party",
    "PartyRole",
    "Precedent",
    "RemedyType",
    "Statute",
]
