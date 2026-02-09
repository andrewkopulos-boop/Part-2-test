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
