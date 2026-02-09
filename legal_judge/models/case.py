"""Models representing a legal case and its components."""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PartyRole(str, Enum):
    PLAINTIFF = "plaintiff"
    DEFENDANT = "defendant"
    APPELLANT = "appellant"
    APPELLEE = "appellee"
    PETITIONER = "petitioner"
    RESPONDENT = "respondent"
    PROSECUTOR = "prosecutor"
    INTERVENOR = "intervenor"


class CaseType(str, Enum):
    CIVIL = "civil"
    CRIMINAL = "criminal"
    CONTRACT = "contract"
    TORT = "tort"
    CONSTITUTIONAL = "constitutional"
    ADMINISTRATIVE = "administrative"
    FAMILY = "family"
    PROPERTY = "property"
    EMPLOYMENT = "employment"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    CORPORATE = "corporate"
    ENVIRONMENTAL = "environmental"


class CaseStatus(str, Enum):
    FILED = "filed"
    UNDER_REVIEW = "under_review"
    HEARING = "hearing"
    DELIBERATION = "deliberation"
    DECIDED = "decided"
    APPEALED = "appealed"
    CLOSED = "closed"


class EvidenceType(str, Enum):
    DOCUMENTARY = "documentary"
    TESTIMONIAL = "testimonial"
    PHYSICAL = "physical"
    DIGITAL = "digital"
    EXPERT_OPINION = "expert_opinion"
    CIRCUMSTANTIAL = "circumstantial"
    STATISTICAL = "statistical"


class Party(BaseModel):
    """A party involved in a legal case."""

    name: str
    role: PartyRole
    description: str = ""
    counsel: str = ""

    def __str__(self) -> str:
        return f"{self.name} ({self.role.value})"


class Evidence(BaseModel):
    """A piece of evidence submitted in a case."""

    title: str
    evidence_type: EvidenceType
    description: str
    submitted_by: str
    credibility_weight: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Weight from 0 (unreliable) to 1 (highly credible)",
    )
    admissible: bool = True
    relevance_summary: str = ""

    def __str__(self) -> str:
        status = "admissible" if self.admissible else "inadmissible"
        return f"[{self.evidence_type.value}] {self.title} ({status})"


class Argument(BaseModel):
    """A legal argument made by a party."""

    party_name: str
    claim: str
    supporting_facts: list[str] = Field(default_factory=list)
    legal_basis: list[str] = Field(default_factory=list)
    cited_precedents: list[str] = Field(default_factory=list)
    counter_to: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.party_name}: {self.claim[:80]}"


class Case(BaseModel):
    """A complete legal case to be adjudicated."""

    case_id: str
    title: str
    case_type: CaseType
    jurisdiction: str = "General"
    date_filed: date = Field(default_factory=date.today)
    status: CaseStatus = CaseStatus.FILED

    parties: list[Party] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    arguments: list[Argument] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    applicable_statutes: list[str] = Field(default_factory=list)

    summary: str = ""

    def get_parties_by_role(self, role: PartyRole) -> list[Party]:
        return [p for p in self.parties if p.role == role]

    def get_admissible_evidence(self) -> list[Evidence]:
        return [e for e in self.evidence if e.admissible]

    def get_arguments_by_party(self, party_name: str) -> list[Argument]:
        return [a for a in self.arguments if a.party_name == party_name]

    def __str__(self) -> str:
        parties_str = " v. ".join(p.name for p in self.parties[:2])
        return f"Case {self.case_id}: {parties_str or self.title}"
