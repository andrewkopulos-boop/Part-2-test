"""Models representing judicial judgments and opinions."""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class Disposition(str, Enum):
    GRANTED = "granted"
    DENIED = "denied"
    GRANTED_IN_PART = "granted_in_part"
    DISMISSED = "dismissed"
    SUSTAINED = "sustained"
    OVERRULED = "overruled"
    REMANDED = "remanded"
    SETTLED = "settled"
    GUILTY = "guilty"
    NOT_GUILTY = "not_guilty"


class RemedyType(str, Enum):
    DAMAGES = "damages"
    INJUNCTION = "injunction"
    SPECIFIC_PERFORMANCE = "specific_performance"
    DECLARATORY = "declaratory"
    RESTITUTION = "restitution"
    RESCISSION = "rescission"
    NONE = "none"


class JudgmentSection(BaseModel):
    """A section of a judicial opinion."""

    heading: str
    content: str
    subsections: list[JudgmentSection] = Field(default_factory=list)


class Judgment(BaseModel):
    """A complete judicial judgment/opinion on a case."""

    case_id: str
    case_title: str
    date_decided: date = Field(default_factory=date.today)
    disposition: Disposition
    remedy: RemedyType = RemedyType.NONE

    # Structured opinion sections
    summary: str = ""
    facts_found: list[str] = Field(default_factory=list)
    issues_addressed: list[str] = Field(default_factory=list)
    rules_applied: list[str] = Field(default_factory=list)
    analysis: str = ""
    holding: str = ""
    reasoning: str = ""
    remedy_details: str = ""
    dissent: str = ""
    obiter_dicta: str = ""

    # Scoring
    confidence: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Confidence in the judgment from 0 to 1",
    )
    strength_of_evidence: float = Field(
        default=0.5, ge=0.0, le=1.0,
    )

    prevailing_party: str = ""
    costs_awarded_to: str = ""

    sections: list[JudgmentSection] = Field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Judgment on {self.case_title}: {self.disposition.value} "
            f"(confidence: {self.confidence:.0%})"
        )
