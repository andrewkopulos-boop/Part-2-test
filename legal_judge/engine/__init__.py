"""Legal reasoning engine for analyzing cases and rendering judgments."""

from legal_judge.engine.analyzer import LegalAnalyzer
from legal_judge.engine.judge import JudgeEngine
from legal_judge.engine.panel import JudicialPanel, JudicialPhilosophy, PanelDecision
from legal_judge.engine.precedent import PrecedentMatcher
from legal_judge.engine.reasoning import ReasoningChain, ReasoningStep
from legal_judge.engine.risk import RiskAssessor, RiskReport
from legal_judge.engine.settlement import SettlementCalculator, SettlementReport

__all__ = [
    "JudgeEngine",
    "JudicialPanel",
    "JudicialPhilosophy",
    "LegalAnalyzer",
    "PanelDecision",
    "PrecedentMatcher",
    "ReasoningChain",
    "ReasoningStep",
    "RiskAssessor",
    "RiskReport",
    "SettlementCalculator",
    "SettlementReport",
]
