"""Legal reasoning chains and logical inference framework."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ReasoningType(str, Enum):
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ANALOGICAL = "analogical"
    POLICY_BASED = "policy_based"
    BALANCING = "balancing"


class ReasoningStep(BaseModel):
    """A single step in a chain of legal reasoning."""

    step_number: int
    reasoning_type: ReasoningType
    premise: str
    inference: str
    conclusion: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    supporting_authority: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Step {self.step_number} [{self.reasoning_type.value}]: "
            f"{self.conclusion} (confidence: {self.confidence:.0%})"
        )


class ReasoningChain(BaseModel):
    """A complete chain of legal reasoning from premises to conclusion."""

    issue: str
    steps: list[ReasoningStep] = Field(default_factory=list)
    final_conclusion: str = ""
    overall_confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    def add_step(
        self,
        reasoning_type: ReasoningType,
        premise: str,
        inference: str,
        conclusion: str,
        confidence: float = 0.5,
        supporting_authority: list[str] | None = None,
    ) -> ReasoningStep:
        step = ReasoningStep(
            step_number=len(self.steps) + 1,
            reasoning_type=reasoning_type,
            premise=premise,
            inference=inference,
            conclusion=conclusion,
            confidence=confidence,
            supporting_authority=supporting_authority or [],
        )
        self.steps.append(step)
        self._recalculate_confidence()
        return step

    def _recalculate_confidence(self) -> None:
        if not self.steps:
            self.overall_confidence = 0.0
            return
        # Chain confidence is the product of individual confidences,
        # but with a floor to avoid collapsing to zero on long chains.
        product = 1.0
        for step in self.steps:
            product *= step.confidence
        # Geometric mean gives a fairer aggregate for longer chains.
        self.overall_confidence = product ** (1.0 / len(self.steps))

    def finalize(self, conclusion: str) -> None:
        self.final_conclusion = conclusion
        self._recalculate_confidence()

    def __str__(self) -> str:
        lines = [f"Reasoning on: {self.issue}"]
        for step in self.steps:
            lines.append(f"  {step}")
        lines.append(
            f"  => {self.final_conclusion} "
            f"(overall confidence: {self.overall_confidence:.0%})"
        )
        return "\n".join(lines)
