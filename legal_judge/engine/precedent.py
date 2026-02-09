"""Precedent matching and analogical reasoning engine."""

from __future__ import annotations

from pydantic import BaseModel, Field

from legal_judge.models.case import Case, CaseType
from legal_judge.models.legal import LegalDomain, Precedent


# Map case types to likely legal domains for precedent searching.
_CASE_TYPE_TO_DOMAINS: dict[CaseType, list[LegalDomain]] = {
    CaseType.CIVIL: [LegalDomain.TORT_LAW, LegalDomain.CIVIL_PROCEDURE],
    CaseType.CRIMINAL: [LegalDomain.CRIMINAL_LAW, LegalDomain.EVIDENCE_LAW],
    CaseType.CONTRACT: [LegalDomain.CONTRACT_LAW],
    CaseType.TORT: [LegalDomain.TORT_LAW],
    CaseType.CONSTITUTIONAL: [LegalDomain.CONSTITUTIONAL_LAW],
    CaseType.ADMINISTRATIVE: [LegalDomain.ADMINISTRATIVE_LAW],
    CaseType.FAMILY: [LegalDomain.FAMILY_LAW],
    CaseType.PROPERTY: [LegalDomain.PROPERTY_LAW],
    CaseType.EMPLOYMENT: [LegalDomain.EMPLOYMENT_LAW],
    CaseType.INTELLECTUAL_PROPERTY: [LegalDomain.INTELLECTUAL_PROPERTY],
    CaseType.CORPORATE: [LegalDomain.CORPORATE_LAW],
    CaseType.ENVIRONMENTAL: [LegalDomain.ENVIRONMENTAL_LAW],
}


class PrecedentMatch(BaseModel):
    """A precedent matched to the current case with a relevance score."""

    precedent: Precedent
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    matching_keywords: list[str] = Field(default_factory=list)
    applicability_note: str = ""


class PrecedentMatcher:
    """Finds and ranks precedents relevant to a given case."""

    def __init__(self, precedent_library: list[Precedent] | None = None) -> None:
        self._library: list[Precedent] = precedent_library or []

    @property
    def library(self) -> list[Precedent]:
        return list(self._library)

    def add_precedent(self, precedent: Precedent) -> None:
        self._library.append(precedent)

    def add_precedents(self, precedents: list[Precedent]) -> None:
        self._library.extend(precedents)

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------

    def find_relevant(
        self, case: Case, *, top_k: int = 5
    ) -> list[PrecedentMatch]:
        """Return the top-k most relevant precedents for *case*."""
        scored: list[PrecedentMatch] = []
        case_keywords = self._extract_case_keywords(case)
        target_domains = _CASE_TYPE_TO_DOMAINS.get(case.case_type, [])

        for prec in self._library:
            score, matched_kw = self._score_precedent(
                prec, case_keywords, target_domains
            )
            if score > 0:
                scored.append(
                    PrecedentMatch(
                        precedent=prec,
                        relevance_score=min(score, 1.0),
                        matching_keywords=matched_kw,
                        applicability_note=self._build_note(prec, matched_kw),
                    )
                )

        scored.sort(key=lambda m: m.relevance_score, reverse=True)
        return scored[:top_k]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_case_keywords(case: Case) -> set[str]:
        """Pull searchable keywords from all textual fields of a case."""
        tokens: set[str] = set()
        text_sources = (
            case.facts
            + case.issues
            + [a.claim for a in case.arguments]
            + [e.description for e in case.evidence]
            + case.applicable_statutes
        )
        for text in text_sources:
            for word in text.lower().split():
                cleaned = word.strip(".,;:!?\"'()[]{}").rstrip("'s")
                if len(cleaned) > 2:
                    tokens.add(cleaned)
        return tokens

    @staticmethod
    def _score_precedent(
        precedent: Precedent,
        case_keywords: set[str],
        target_domains: list[LegalDomain],
    ) -> tuple[float, list[str]]:
        """Score a precedent against the case keywords and domains."""
        score = 0.0
        matched: list[str] = []

        # Domain match gives a base boost.
        if precedent.domain in target_domains:
            score += 0.3

        # Keyword overlap.
        prec_keywords = {k.lower() for k in precedent.relevance_keywords}
        overlap = prec_keywords & case_keywords
        if prec_keywords:
            keyword_ratio = len(overlap) / len(prec_keywords)
            score += 0.5 * keyword_ratio
            matched = sorted(overlap)

        # Authority weight contributes up to 0.2.
        score += 0.2 * precedent.authority_weight

        return score, matched

    @staticmethod
    def _build_note(precedent: Precedent, matched_kw: list[str]) -> str:
        parts: list[str] = []
        if precedent.ratio_decidendi:
            parts.append(f"Ratio: {precedent.ratio_decidendi}")
        if matched_kw:
            parts.append(f"Matched on: {', '.join(matched_kw)}")
        return "; ".join(parts) if parts else "General domain relevance."
