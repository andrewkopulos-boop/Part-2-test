"""Central knowledge base that aggregates all legal knowledge."""

from __future__ import annotations

from legal_judge.engine.judge import JudgeEngine
from legal_judge.knowledge.domains import (
    get_all_precedents,
    get_all_principles,
    get_all_statutes,
)
from legal_judge.models.legal import LegalDomain, LegalPrinciple, Precedent, Statute


class KnowledgeBase:
    """Aggregates statutes, precedents, and principles and creates a JudgeEngine."""

    def __init__(self) -> None:
        self._statutes: list[Statute] = []
        self._precedents: list[Precedent] = []
        self._principles: list[LegalPrinciple] = []

    @classmethod
    def with_defaults(cls) -> KnowledgeBase:
        """Create a knowledge base pre-loaded with built-in legal knowledge."""
        kb = cls()
        kb._statutes = get_all_statutes()
        kb._precedents = get_all_precedents()
        kb._principles = get_all_principles()
        return kb

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def statutes(self) -> list[Statute]:
        return list(self._statutes)

    @property
    def precedents(self) -> list[Precedent]:
        return list(self._precedents)

    @property
    def principles(self) -> list[LegalPrinciple]:
        return list(self._principles)

    # ------------------------------------------------------------------
    # Adding knowledge
    # ------------------------------------------------------------------

    def add_statute(self, statute: Statute) -> None:
        self._statutes.append(statute)

    def add_precedent(self, precedent: Precedent) -> None:
        self._precedents.append(precedent)

    def add_principle(self, principle: LegalPrinciple) -> None:
        self._principles.append(principle)

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def statutes_for_domain(self, domain: LegalDomain) -> list[Statute]:
        return [s for s in self._statutes if s.domain == domain]

    def precedents_for_domain(self, domain: LegalDomain) -> list[Precedent]:
        return [p for p in self._precedents if p.domain == domain]

    def principles_for_domain(self, domain: LegalDomain) -> list[LegalPrinciple]:
        return [p for p in self._principles if p.domain == domain]

    # ------------------------------------------------------------------
    # Engine creation
    # ------------------------------------------------------------------

    def create_judge(self) -> JudgeEngine:
        """Create a JudgeEngine loaded with all knowledge in this base."""
        return JudgeEngine(
            statutes=self._statutes,
            principles=self._principles,
            precedents=self._precedents,
        )

    def __repr__(self) -> str:
        return (
            f"KnowledgeBase(statutes={len(self._statutes)}, "
            f"precedents={len(self._precedents)}, "
            f"principles={len(self._principles)})"
        )
