"""High-level opinion writer that ties the engine and formatter together."""

from __future__ import annotations

from legal_judge.engine.judge import JudgeEngine
from legal_judge.knowledge.base import KnowledgeBase
from legal_judge.models.case import Case
from legal_judge.models.judgment import Judgment
from legal_judge.output.formatter import Formatter


class OpinionWriter:
    """Facade that accepts a case and produces a formatted opinion."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase | None = None,
        judge_engine: JudgeEngine | None = None,
    ) -> None:
        if judge_engine is not None:
            self._engine = judge_engine
        else:
            kb = knowledge_base or KnowledgeBase.with_defaults()
            self._engine = kb.create_judge()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def decide(self, case: Case) -> Judgment:
        """Adjudicate a case and return the Judgment object."""
        return self._engine.adjudicate(case)

    def render_text(self, case: Case) -> str:
        """Adjudicate and return the opinion as plain text."""
        judgment = self.decide(case)
        return Formatter.to_text(judgment)

    def render_markdown(self, case: Case) -> str:
        """Adjudicate and return the opinion as Markdown."""
        judgment = self.decide(case)
        return Formatter.to_markdown(judgment)

    @staticmethod
    def format_judgment_text(judgment: Judgment) -> str:
        return Formatter.to_text(judgment)

    @staticmethod
    def format_judgment_markdown(judgment: Judgment) -> str:
        return Formatter.to_markdown(judgment)
