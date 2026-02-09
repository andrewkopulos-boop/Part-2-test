"""Legal knowledge base: statutes, precedents, and principles."""

from legal_judge.knowledge.base import KnowledgeBase
from legal_judge.knowledge.domains import (
    get_all_precedents,
    get_all_principles,
    get_all_statutes,
    get_contract_law,
    get_criminal_law,
    get_tort_law,
)

__all__ = [
    "KnowledgeBase",
    "get_all_precedents",
    "get_all_principles",
    "get_all_statutes",
    "get_contract_law",
    "get_criminal_law",
    "get_tort_law",
]
