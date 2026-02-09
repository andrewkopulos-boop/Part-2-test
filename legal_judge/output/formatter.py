"""Formatting utilities for rendering judgments as text."""

from __future__ import annotations

from legal_judge.models.judgment import Judgment, JudgmentSection


class Formatter:
    """Renders a Judgment into formatted plain text or Markdown."""

    DIVIDER = "=" * 72
    THIN_DIVIDER = "-" * 72

    # ------------------------------------------------------------------
    # Plain text
    # ------------------------------------------------------------------

    @classmethod
    def to_text(cls, judgment: Judgment) -> str:
        lines: list[str] = []
        lines.append(cls.DIVIDER)
        lines.append(cls._center("JUDICIAL OPINION"))
        lines.append(cls.DIVIDER)
        lines.append("")
        lines.append(f"Case:        {judgment.case_title}")
        lines.append(f"Case ID:     {judgment.case_id}")
        lines.append(f"Date:        {judgment.date_decided}")
        lines.append(f"Disposition: {judgment.disposition.value.upper()}")
        if judgment.remedy.value != "none":
            lines.append(f"Remedy:      {judgment.remedy.value}")
        lines.append(f"Prevailing:  {judgment.prevailing_party}")
        lines.append(f"Confidence:  {judgment.confidence:.0%}")
        lines.append("")
        lines.append(cls.THIN_DIVIDER)

        for section in judgment.sections:
            lines.append("")
            lines.extend(cls._render_section_text(section, level=0))

        lines.append("")
        lines.append(cls.THIN_DIVIDER)
        lines.append("")
        lines.append("HOLDING:")
        lines.append(f"  {judgment.holding}")

        if judgment.remedy_details:
            lines.append("")
            lines.append("REMEDY:")
            lines.append(f"  {judgment.remedy_details}")

        if judgment.costs_awarded_to:
            lines.append("")
            lines.append(f"Costs awarded to: {judgment.costs_awarded_to}")

        lines.append("")
        lines.append(cls.DIVIDER)
        lines.append(cls._center("END OF OPINION"))
        lines.append(cls.DIVIDER)
        return "\n".join(lines)

    @classmethod
    def _render_section_text(
        cls, section: JudgmentSection, level: int
    ) -> list[str]:
        indent = "  " * level
        lines = [f"{indent}{section.heading}", ""]
        for line in section.content.split("\n"):
            lines.append(f"{indent}  {line}")
        for sub in section.subsections:
            lines.append("")
            lines.extend(cls._render_section_text(sub, level + 1))
        return lines

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    @classmethod
    def to_markdown(cls, judgment: Judgment) -> str:
        lines: list[str] = []
        lines.append(f"# Judicial Opinion: {judgment.case_title}")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.append(f"| **Case ID** | {judgment.case_id} |")
        lines.append(f"| **Date** | {judgment.date_decided} |")
        lines.append(f"| **Disposition** | {judgment.disposition.value.upper()} |")
        if judgment.remedy.value != "none":
            lines.append(f"| **Remedy** | {judgment.remedy.value} |")
        lines.append(f"| **Prevailing Party** | {judgment.prevailing_party} |")
        lines.append(f"| **Confidence** | {judgment.confidence:.0%} |")
        lines.append(f"| **Evidence Strength** | {judgment.strength_of_evidence:.0%} |")
        lines.append("")

        for section in judgment.sections:
            lines.extend(cls._render_section_md(section, heading_level=2))

        lines.append("---")
        lines.append("")
        lines.append("## Holding")
        lines.append("")
        lines.append(judgment.holding)

        if judgment.remedy_details:
            lines.append("")
            lines.append("## Remedy")
            lines.append("")
            lines.append(judgment.remedy_details)

        if judgment.rules_applied:
            lines.append("")
            lines.append("## Rules Applied")
            lines.append("")
            for rule in judgment.rules_applied:
                lines.append(f"- {rule}")

        lines.append("")
        lines.append("---")
        lines.append(f"*Opinion rendered on {judgment.date_decided}.*")
        return "\n".join(lines)

    @classmethod
    def _render_section_md(
        cls, section: JudgmentSection, heading_level: int
    ) -> list[str]:
        prefix = "#" * heading_level
        lines = [f"{prefix} {section.heading}", ""]
        lines.append(section.content)
        lines.append("")
        for sub in section.subsections:
            lines.extend(cls._render_section_md(sub, heading_level + 1))
        return lines

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _center(text: str, width: int = 72) -> str:
        return text.center(width)
