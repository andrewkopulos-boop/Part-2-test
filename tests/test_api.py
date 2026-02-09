"""Tests for the FastAPI application."""

import sys
from pathlib import Path

# Ensure imports work.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


def test_enums():
    resp = client.get("/api/enums")
    assert resp.status_code == 200
    data = resp.json()
    assert "case_types" in data
    assert "contract" in data["case_types"]
    assert "party_roles" in data
    assert "evidence_types" in data


def test_knowledge():
    resp = client.get("/api/knowledge")
    assert resp.status_code == 200
    data = resp.json()
    assert data["statutes"] > 0
    assert data["precedents"] > 0
    assert data["principles"] > 0
    assert len(data["domains"]) > 0
    assert len(data["precedents_list"]) > 0


def test_get_demo_contract():
    resp = client.get("/api/demo/contract")
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data
    assert len(data["parties"]) >= 2


def test_get_demo_tort():
    resp = client.get("/api/demo/tort")
    assert resp.status_code == 200
    data = resp.json()
    assert "title" in data


def test_get_demo_not_found():
    resp = client.get("/api/demo/nonexistent")
    assert resp.status_code == 404


def test_judge_case():
    case = {
        "title": "Test v. Case",
        "case_type": "contract",
        "parties": [
            {"name": "Alice", "role": "plaintiff"},
            {"name": "Bob", "role": "defendant"},
        ],
        "facts": ["Contract was signed.", "Bob failed to deliver."],
        "issues": ["Whether Bob breached the contract"],
        "arguments": [
            {
                "party_name": "Alice",
                "claim": "Bob breached the contract.",
                "supporting_facts": ["Late delivery"],
                "legal_basis": ["Breach of contract"],
            }
        ],
        "evidence": [
            {
                "title": "Contract",
                "evidence_type": "documentary",
                "description": "The signed contract.",
                "submitted_by": "Alice",
                "credibility_weight": 0.9,
            }
        ],
    }
    resp = client.post("/api/judge", json=case)
    assert resp.status_code == 200
    data = resp.json()
    assert "disposition" in data
    assert "confidence" in data
    assert "opinion_text" in data
    assert "opinion_markdown" in data
    assert "sections" in data
    assert data["prevailing_party"] != ""


def test_judge_minimal_case():
    case = {"title": "Minimal Case", "case_type": "civil"}
    resp = client.post("/api/judge", json=case)
    assert resp.status_code == 200
    data = resp.json()
    assert data["disposition"] == "dismissed"


def test_precedent_search():
    body = {"query": "negligence duty care"}
    resp = client.post("/api/precedents/search", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert len(data["results"]) > 0
    assert "Donoghue v. Stevenson" in data["results"][0]["case_name"]


def test_precedent_search_no_results():
    body = {"query": "xyzzy zzzzz"}
    resp = client.post("/api/precedents/search", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"] == []


def test_compare_cases():
    body = {
        "case_a": {
            "title": "A v B",
            "case_type": "contract",
            "facts": ["Contract breach."],
            "issues": ["Whether breach occurred"],
        },
        "case_b": {
            "title": "C v D",
            "case_type": "contract",
            "facts": ["Contract breach."],
            "issues": ["Whether breach occurred"],
        },
    }
    resp = client.post("/api/compare", json=body)
    assert resp.status_code == 200
    data = resp.json()
    assert "overall_similarity" in data
    assert data["case_type_match"] is True


def test_history():
    resp = client.get("/api/history")
    assert resp.status_code == 200
    data = resp.json()
    assert "count" in data
    assert "cases" in data


# ------------------------------------------------------------------
# Panel endpoint
# ------------------------------------------------------------------

def test_panel_endpoint():
    case = {
        "title": "Panel Test v. Case",
        "case_type": "contract",
        "parties": [
            {"name": "Alice", "role": "plaintiff"},
            {"name": "Bob", "role": "defendant"},
        ],
        "facts": ["Contract was signed.", "Bob failed to deliver."],
        "issues": ["Whether Bob breached the contract"],
        "arguments": [
            {
                "party_name": "Alice",
                "claim": "Bob breached the contract.",
                "supporting_facts": ["Late delivery"],
                "legal_basis": ["Breach of contract"],
            }
        ],
        "evidence": [
            {
                "title": "Contract",
                "evidence_type": "documentary",
                "submitted_by": "Alice",
                "credibility_weight": 0.9,
            }
        ],
    }
    resp = client.post("/api/panel", json=case)
    assert resp.status_code == 200
    data = resp.json()
    assert "majority_disposition" in data
    assert "opinions" in data
    assert len(data["opinions"]) == 3
    assert "is_unanimous" in data
    assert "majority_vote" in data
    assert "majority_confidence" in data


# ------------------------------------------------------------------
# Risk endpoint
# ------------------------------------------------------------------

def test_risk_endpoint():
    case = {
        "title": "Risk Test v. Case",
        "case_type": "tort",
        "parties": [
            {"name": "Alice", "role": "plaintiff"},
            {"name": "Bob", "role": "defendant"},
        ],
        "facts": ["Bob was negligent.", "Alice was injured."],
        "issues": ["Whether Bob was negligent"],
        "arguments": [
            {
                "party_name": "Alice",
                "claim": "Bob was negligent.",
                "supporting_facts": ["Ran red light"],
                "legal_basis": ["Duty of care"],
            }
        ],
        "evidence": [
            {
                "title": "Medical records",
                "evidence_type": "documentary",
                "submitted_by": "Alice",
                "credibility_weight": 0.9,
            }
        ],
    }
    resp = client.post("/api/risk", json={"case": case})
    assert resp.status_code == 200
    data = resp.json()
    assert "litigation_risk_level" in data
    assert "recommendation" in data
    assert "parties" in data
    assert len(data["parties"]) == 2
    for p in data["parties"]:
        assert "win_probability" in p
        assert "overall_grade" in p


# ------------------------------------------------------------------
# Settlement endpoint
# ------------------------------------------------------------------

def test_settlement_endpoint():
    case = {
        "title": "Settlement Test v. Case",
        "case_type": "contract",
        "parties": [
            {"name": "Alice", "role": "plaintiff"},
            {"name": "Bob", "role": "defendant"},
        ],
        "facts": ["Contract breach with $100000 in damages."],
        "issues": ["Whether breach occurred"],
        "arguments": [
            {
                "party_name": "Alice",
                "claim": "Bob breached the contract.",
                "supporting_facts": ["Non-delivery"],
                "legal_basis": ["Breach of contract"],
            }
        ],
    }
    resp = client.post("/api/settlement", json={"case": case, "claimed_damages": 100000})
    assert resp.status_code == 200
    data = resp.json()
    assert "should_settle" in data
    assert "settlement_recommendation" in data
    assert "damages_estimate" in data
    assert "settlement_range" in data
    assert "cost_of_litigation_estimate" in data
    assert data["damages_estimate"]["total"] > 0
    assert data["settlement_range"]["low"] <= data["settlement_range"]["high"]
