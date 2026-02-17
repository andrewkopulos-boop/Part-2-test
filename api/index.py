"""FastAPI application serving the Legal Judge Bot API.

Vercel-compatible: this module is auto-discovered as a serverless function
at the /api route prefix.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is importable when running under Vercel.
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from legal_judge.knowledge.base import KnowledgeBase
from legal_judge.models.case import (
    Argument,
    Case,
    CaseType,
    Evidence,
    EvidenceType,
    Party,
    PartyRole,
)
from legal_judge.models.judgment import Judgment
from legal_judge.output.formatter import Formatter
from legal_judge.main import DEMO_CASES

# ---------------------------------------------------------------------------
# App + singleton engine
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Legal Judge Bot",
    version="2.0.0",
    description=(
        "AI-powered legal analysis engine that applies IRAC reasoning, "
        "matches precedents, and renders structured judicial opinions. "
        "Inspired by DeepJudge / Claude Cowork integration concepts."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_kb = KnowledgeBase.with_defaults()
_engine = _kb.create_judge()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class PartyIn(BaseModel):
    name: str
    role: str
    description: str = ""
    counsel: str = ""

class EvidenceIn(BaseModel):
    title: str
    evidence_type: str = "documentary"
    description: str = ""
    submitted_by: str = ""
    credibility_weight: float = Field(default=0.5, ge=0.0, le=1.0)
    admissible: bool = True

class ArgumentIn(BaseModel):
    party_name: str
    claim: str
    supporting_facts: list[str] = Field(default_factory=list)
    legal_basis: list[str] = Field(default_factory=list)
    cited_precedents: list[str] = Field(default_factory=list)

class CaseIn(BaseModel):
    case_id: str = "WEB-001"
    title: str
    case_type: str = "civil"
    jurisdiction: str = "General"
    summary: str = ""
    parties: list[PartyIn] = Field(default_factory=list)
    facts: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    arguments: list[ArgumentIn] = Field(default_factory=list)
    evidence: list[EvidenceIn] = Field(default_factory=list)
    applicable_statutes: list[str] = Field(default_factory=list)

class AppealIn(BaseModel):
    original_case: CaseIn
    new_arguments: list[ArgumentIn] = Field(default_factory=list)
    new_evidence: list[EvidenceIn] = Field(default_factory=list)

class CompareIn(BaseModel):
    case_a: CaseIn
    case_b: CaseIn

class PrecedentSearchIn(BaseModel):
    query: str
    domain: str = ""
    top_k: int = 10


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_case(data: CaseIn) -> Case:
    """Convert an API CaseIn to the domain Case model."""
    parties = [
        Party(
            name=p.name,
            role=PartyRole(p.role),
            description=p.description,
            counsel=p.counsel,
        )
        for p in data.parties
    ]
    evidence = [
        Evidence(
            title=e.title,
            evidence_type=EvidenceType(e.evidence_type),
            description=e.description,
            submitted_by=e.submitted_by,
            credibility_weight=e.credibility_weight,
            admissible=e.admissible,
        )
        for e in data.evidence
    ]
    arguments = [
        Argument(
            party_name=a.party_name,
            claim=a.claim,
            supporting_facts=a.supporting_facts,
            legal_basis=a.legal_basis,
            cited_precedents=a.cited_precedents,
        )
        for a in data.arguments
    ]
    return Case(
        case_id=data.case_id,
        title=data.title,
        case_type=CaseType(data.case_type),
        jurisdiction=data.jurisdiction,
        summary=data.summary,
        parties=parties,
        facts=data.facts,
        issues=data.issues,
        arguments=arguments,
        evidence=evidence,
        applicable_statutes=data.applicable_statutes,
    )


def _judgment_to_dict(j: Judgment) -> dict:
    """Serialize a Judgment to a JSON-friendly dict."""
    return {
        "case_id": j.case_id,
        "case_title": j.case_title,
        "date_decided": str(j.date_decided),
        "disposition": j.disposition.value,
        "remedy": j.remedy.value,
        "summary": j.summary,
        "facts_found": j.facts_found,
        "issues_addressed": j.issues_addressed,
        "rules_applied": j.rules_applied,
        "analysis": j.analysis,
        "holding": j.holding,
        "reasoning": j.reasoning,
        "remedy_details": j.remedy_details,
        "dissent": j.dissent,
        "confidence": round(j.confidence, 4),
        "strength_of_evidence": round(j.strength_of_evidence, 4),
        "prevailing_party": j.prevailing_party,
        "costs_awarded_to": j.costs_awarded_to,
        "sections": [
            {"heading": s.heading, "content": s.content}
            for s in j.sections
        ],
        "opinion_text": Formatter.to_text(j),
        "opinion_markdown": Formatter.to_markdown(j),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "2.0.0"}


@app.get("/api/knowledge")
def knowledge_info():
    return {
        "statutes": len(_kb.statutes),
        "precedents": len(_kb.precedents),
        "principles": len(_kb.principles),
        "domains": sorted({s.domain.value for s in _kb.statutes} | {p.domain.value for p in _kb.precedents}),
        "statutes_list": [
            {"name": s.name, "code": s.code, "domain": s.domain.value, "summary": s.summary}
            for s in _kb.statutes
        ],
        "precedents_list": [
            {
                "case_name": p.case_name,
                "citation": p.citation,
                "year": p.year,
                "domain": p.domain.value,
                "holding": p.holding,
                "authority_weight": p.authority_weight,
            }
            for p in _kb.precedents
        ],
        "principles_list": [
            {
                "name": p.name,
                "latin_name": p.latin_name,
                "domain": p.domain.value,
                "description": p.description,
                "elements": p.elements,
            }
            for p in _kb.principles
        ],
    }


@app.post("/api/precedents/search")
def search_precedents(body: PrecedentSearchIn):
    query_lower = body.query.lower()
    query_words = {w.strip(".,;:!?") for w in query_lower.split() if len(w) > 2}
    results = []
    for p in _kb.precedents:
        if body.domain and p.domain.value != body.domain:
            continue
        kw_set = {k.lower() for k in p.relevance_keywords}
        text_words = {w.lower().strip(".,;:!?") for w in (p.holding + " " + p.case_name).split() if len(w) > 2}
        overlap = query_words & (kw_set | text_words)
        if overlap:
            results.append({
                "case_name": p.case_name,
                "citation": p.citation,
                "year": p.year,
                "domain": p.domain.value,
                "holding": p.holding,
                "ratio_decidendi": p.ratio_decidendi,
                "authority_weight": p.authority_weight,
                "matched_terms": sorted(overlap),
            })
    results.sort(key=lambda r: len(r["matched_terms"]), reverse=True)
    return {"results": results[:body.top_k]}


@app.get("/api/demo/{case_name}")
def get_demo(case_name: str):
    builder = DEMO_CASES.get(case_name)
    if not builder:
        raise HTTPException(status_code=404, detail=f"Demo case '{case_name}' not found. Available: {list(DEMO_CASES.keys())}")
    case = builder()
    return case.model_dump(mode="json")


@app.post("/api/judge")
def judge_case(body: CaseIn):
    case = _to_case(body)
    judgment = _engine.adjudicate(case)
    result = _judgment_to_dict(judgment)

    # Automatically enhance with AI when available.
    case_data = body.model_dump()
    enhancement = _llm_enhancer.enhance_judgment(case_data, result)
    result["ai_enhancement"] = _enhancement_to_dict(enhancement)

    return result


@app.post("/api/appeal")
def appeal_case(body: AppealIn):
    original_case = _to_case(body.original_case)
    original_judgment = _engine.adjudicate(original_case)

    new_args = [
        Argument(
            party_name=a.party_name,
            claim=a.claim,
            supporting_facts=a.supporting_facts,
            legal_basis=a.legal_basis,
            cited_precedents=a.cited_precedents,
        )
        for a in body.new_arguments
    ]
    new_ev = [
        Evidence(
            title=e.title,
            evidence_type=EvidenceType(e.evidence_type),
            description=e.description,
            submitted_by=e.submitted_by,
            credibility_weight=e.credibility_weight,
            admissible=e.admissible,
        )
        for e in body.new_evidence
    ]

    appeal_judgment = _engine.appeal(original_case, original_judgment, new_args, new_ev)
    return {
        "original": _judgment_to_dict(original_judgment),
        "appeal": _judgment_to_dict(appeal_judgment),
    }


@app.post("/api/compare")
def compare_cases(body: CompareIn):
    case_a = _to_case(body.case_a)
    case_b = _to_case(body.case_b)
    return _engine.compare_cases(case_a, case_b)


@app.get("/api/history")
def case_history():
    return {
        "count": len(_engine.case_history),
        "cases": [
            {
                "case_id": c.case_id,
                "title": c.title,
                "disposition": j.disposition.value,
                "confidence": round(j.confidence, 4),
                "prevailing_party": j.prevailing_party,
            }
            for c, j in _engine.case_history
        ],
    }


@app.get("/api/enums")
def get_enums():
    """Return all enum values for building dynamic forms."""
    return {
        "case_types": [t.value for t in CaseType],
        "party_roles": [r.value for r in PartyRole],
        "evidence_types": [t.value for t in EvidenceType],
    }


# ---------------------------------------------------------------------------
# Multi-judge panel
# ---------------------------------------------------------------------------

@app.post("/api/panel")
def panel_decision(body: CaseIn):
    """Submit a case to a 3-judge panel with different judicial philosophies."""
    from legal_judge.engine.panel import JudicialPanel
    case = _to_case(body)
    panel = JudicialPanel(
        statutes=_kb.statutes,
        principles=_kb.principles,
        precedents=_kb.precedents,
    )
    decision = panel.decide(case)
    result = {
        "case_id": decision.case_id,
        "case_title": decision.case_title,
        "panel_size": decision.panel_size,
        "majority_disposition": decision.majority_disposition.value,
        "majority_vote": decision.majority_vote,
        "is_unanimous": decision.is_unanimous,
        "majority_confidence": decision.majority_confidence,
        "majority_opinion": decision.majority_opinion,
        "opinions": decision.opinions,
    }
    if decision.judgment:
        result["judgment"] = _judgment_to_dict(decision.judgment)

    # Automatically enhance with AI when available.
    case_data = body.model_dump()
    panel_data = {
        "majority_disposition": decision.majority_disposition.value,
        "majority_vote": decision.majority_vote,
        "is_unanimous": decision.is_unanimous,
        "majority_confidence": decision.majority_confidence,
        "opinions": decision.opinions,
    }
    enhancement = _llm_enhancer.enhance_panel(case_data, panel_data)
    result["ai_enhancement"] = _enhancement_to_dict(enhancement)

    return result


# ---------------------------------------------------------------------------
# Risk assessment
# ---------------------------------------------------------------------------

class RiskIn(BaseModel):
    case: CaseIn

@app.post("/api/risk")
def risk_assessment(body: RiskIn):
    """Assess litigation risk for each party."""
    from legal_judge.engine.risk import RiskAssessor
    case = _to_case(body.case)
    assessor = RiskAssessor()
    report = assessor.assess(case)
    result = {
        "case_id": report.case_id,
        "case_title": report.case_title,
        "litigation_risk_level": report.litigation_risk_level,
        "recommendation": report.recommendation,
        "parties": [
            {
                "party_name": pa.party_name,
                "role": pa.role,
                "win_probability": pa.win_probability,
                "overall_grade": pa.overall_grade,
                "evidence_score": pa.evidence_score,
                "argument_score": pa.argument_score,
                "strengths": pa.strengths,
                "weaknesses": pa.weaknesses,
                "risk_factors": pa.risk_factors,
            }
            for pa in report.party_assessments
        ],
    }

    # Automatically enhance with AI when available.
    case_data = body.case.model_dump()
    risk_data = {
        "litigation_risk_level": report.litigation_risk_level,
        "recommendation": report.recommendation,
        "parties": result["parties"],
    }
    enhancement = _llm_enhancer.enhance_risk(case_data, risk_data)
    result["ai_enhancement"] = _enhancement_to_dict(enhancement)

    return result


# ---------------------------------------------------------------------------
# Settlement calculator
# ---------------------------------------------------------------------------

class SettlementIn(BaseModel):
    case: CaseIn
    claimed_damages: float = 0.0

@app.post("/api/settlement")
def settlement_analysis(body: SettlementIn):
    """Calculate settlement recommendation and damages estimate."""
    from legal_judge.engine.settlement import SettlementCalculator
    case = _to_case(body.case)
    calc = SettlementCalculator()
    report = calc.analyze(case, body.claimed_damages)
    result = {
        "case_id": report.case_id,
        "case_title": report.case_title,
        "should_settle": report.should_settle,
        "settlement_recommendation": report.settlement_recommendation,
        "cost_of_litigation_estimate": report.cost_of_litigation_estimate,
        "damages_estimate": {
            "compensatory": report.damages_estimate.compensatory,
            "consequential": report.damages_estimate.consequential,
            "punitive": report.damages_estimate.punitive,
            "total": report.damages_estimate.total,
            "confidence": report.damages_estimate.confidence,
            "basis": report.damages_estimate.basis,
        },
        "settlement_range": {
            "low": report.settlement_range.low,
            "midpoint": report.settlement_range.midpoint,
            "high": report.settlement_range.high,
            "recommended": report.settlement_range.recommended,
            "rationale": report.settlement_range.rationale,
        },
        "risk_summary": {
            "litigation_risk_level": report.risk_report.litigation_risk_level,
            "parties": [
                {
                    "party_name": pa.party_name,
                    "win_probability": pa.win_probability,
                    "overall_grade": pa.overall_grade,
                }
                for pa in report.risk_report.party_assessments
            ],
        },
    }

    # Automatically enhance with AI when available.
    case_data = body.case.model_dump()
    settlement_data = {
        "should_settle": report.should_settle,
        "settlement_range": result["settlement_range"],
        "damages_estimate": result["damages_estimate"],
        "settlement_recommendation": report.settlement_recommendation,
    }
    enhancement = _llm_enhancer.enhance_settlement(case_data, settlement_data)
    result["ai_enhancement"] = _enhancement_to_dict(enhancement)

    return result


# ---------------------------------------------------------------------------
# LLM Enhancement endpoints
# ---------------------------------------------------------------------------

from legal_judge.engine.llm import LLMEnhancer, LLMEnhancement

_llm_enhancer = LLMEnhancer()


def _enhancement_to_dict(result: LLMEnhancement) -> dict:
    """Serialize an LLMEnhancement to a JSON-friendly dict."""
    return {
        "provider": result.provider,
        "model": result.model,
        "enhanced_opinion": result.enhanced_opinion,
        "enhanced_reasoning": result.enhanced_reasoning,
        "enhanced_dissent": result.enhanced_dissent,
        "key_insights": result.key_insights,
        "plain_english_summary": result.plain_english_summary,
        "error": result.error,
    }


@app.get("/api/llm/status")
def llm_status():
    """Check if an LLM provider is configured."""
    return {
        "available": _llm_enhancer.available,
        "provider": _llm_enhancer.provider_name,
    }


class EnhanceJudgmentIn(BaseModel):
    case: CaseIn
    judgment: dict

@app.post("/api/llm/enhance-judgment")
def enhance_judgment(body: EnhanceJudgmentIn):
    """Enhance a judgment with LLM-generated reasoning."""
    case_data = body.case.model_dump()
    result = _llm_enhancer.enhance_judgment(case_data, body.judgment)
    return {
        "provider": result.provider,
        "model": result.model,
        "enhanced_opinion": result.enhanced_opinion,
        "enhanced_reasoning": result.enhanced_reasoning,
        "enhanced_dissent": result.enhanced_dissent,
        "key_insights": result.key_insights,
        "plain_english_summary": result.plain_english_summary,
        "error": result.error,
    }


class EnhancePanelIn(BaseModel):
    case: CaseIn
    panel: dict

@app.post("/api/llm/enhance-panel")
def enhance_panel(body: EnhancePanelIn):
    """Enhance a panel decision with LLM-generated reasoning."""
    case_data = body.case.model_dump()
    result = _llm_enhancer.enhance_panel(case_data, body.panel)
    return {
        "provider": result.provider,
        "model": result.model,
        "enhanced_opinion": result.enhanced_opinion,
        "enhanced_reasoning": result.enhanced_reasoning,
        "enhanced_dissent": result.enhanced_dissent,
        "key_insights": result.key_insights,
        "plain_english_summary": result.plain_english_summary,
        "error": result.error,
    }


class EnhanceRiskIn(BaseModel):
    case: CaseIn
    risk: dict

@app.post("/api/llm/enhance-risk")
def enhance_risk(body: EnhanceRiskIn):
    """Enhance a risk assessment with LLM analysis."""
    case_data = body.case.model_dump()
    result = _llm_enhancer.enhance_risk(case_data, body.risk)
    return {
        "provider": result.provider,
        "model": result.model,
        "enhanced_opinion": result.enhanced_opinion,
        "enhanced_reasoning": result.enhanced_reasoning,
        "enhanced_dissent": result.enhanced_dissent,
        "key_insights": result.key_insights,
        "plain_english_summary": result.plain_english_summary,
        "error": result.error,
    }


class EnhanceSettlementIn(BaseModel):
    case: CaseIn
    settlement: dict

@app.post("/api/llm/enhance-settlement")
def enhance_settlement(body: EnhanceSettlementIn):
    """Enhance a settlement analysis with LLM reasoning."""
    case_data = body.case.model_dump()
    result = _llm_enhancer.enhance_settlement(case_data, body.settlement)
    return {
        "provider": result.provider,
        "model": result.model,
        "enhanced_opinion": result.enhanced_opinion,
        "enhanced_reasoning": result.enhanced_reasoning,
        "enhanced_dissent": result.enhanced_dissent,
        "key_insights": result.key_insights,
        "plain_english_summary": result.plain_english_summary,
        "error": result.error,
    }
