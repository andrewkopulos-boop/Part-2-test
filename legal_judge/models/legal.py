"""Models for legal concepts: statutes, precedents, principles."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LegalDomain(str, Enum):
    CONTRACT_LAW = "contract_law"
    TORT_LAW = "tort_law"
    CRIMINAL_LAW = "criminal_law"
    CONSTITUTIONAL_LAW = "constitutional_law"
    PROPERTY_LAW = "property_law"
    EMPLOYMENT_LAW = "employment_law"
    FAMILY_LAW = "family_law"
    CORPORATE_LAW = "corporate_law"
    ADMINISTRATIVE_LAW = "administrative_law"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    ENVIRONMENTAL_LAW = "environmental_law"
    CIVIL_PROCEDURE = "civil_procedure"
    EVIDENCE_LAW = "evidence_law"


class JurisdictionType(str, Enum):
    FEDERAL = "federal"
    STATE = "state"
    INTERNATIONAL = "international"
    GENERAL = "general"


class Statute(BaseModel):
    """A statute or legislative provision."""

    name: str
    code: str
    section: str = ""
    domain: LegalDomain
    jurisdiction: JurisdictionType = JurisdictionType.GENERAL
    text: str = ""
    summary: str = ""

    def __str__(self) -> str:
        ref = f"{self.code}"
        if self.section:
            ref += f" {self.section}"
        return f"{self.name} ({ref})"


class Precedent(BaseModel):
    """A judicial precedent (case law)."""

    case_name: str
    citation: str
    year: int
    domain: LegalDomain
    jurisdiction: JurisdictionType = JurisdictionType.GENERAL
    holding: str = ""
    ratio_decidendi: str = ""
    relevance_keywords: list[str] = Field(default_factory=list)
    authority_weight: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="How authoritative this precedent is (0-1)",
    )

    def __str__(self) -> str:
        return f"{self.case_name}, {self.citation} ({self.year})"


class LegalPrinciple(BaseModel):
    """A fundamental legal principle or doctrine."""

    name: str
    latin_name: Optional[str] = None
    domain: LegalDomain
    description: str
    elements: list[str] = Field(default_factory=list)
    exceptions: list[str] = Field(default_factory=list)
    related_principles: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        if self.latin_name:
            return f"{self.name} ({self.latin_name})"
        return self.name
