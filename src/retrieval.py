"""
Khasi Companion - Safe Retrieval Engine (System B: Tourism Knowledge Base)
Enforces the Zero-Hallucination rule. Never invents facts, prices, hours, or emergency advice.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DEFAULT_KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"

class TourismKnowledgeRetriever:
    def __init__(self, kb_path: Optional[Path] = None):
        self.kb_path = kb_path or DEFAULT_KB_PATH
        self.records: List[Dict[str, Any]] = []
        self.load_knowledge_base()

    def load_knowledge_base(self):
        if not self.kb_path.exists():
            self.records = []
            return
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.records = json.load(f)

    def search(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Searches the verified knowledge base using keyword matching across title,
        content, location, and safety notes.
        """
        query_tokens = query.lower().strip().split()
        if not query_tokens and not category:
            return self.records

        results = []
        for rec in self.records:
            if category and rec.get("category") != category:
                continue

            searchable_text = " ".join([
                rec.get("title", ""),
                rec.get("location", ""),
                rec.get("content", {}).get("en", ""),
                rec.get("safety_notes", ""),
                rec.get("notes", "")
            ]).lower()

            # Match if any token is present
            match_score = sum(1 for token in query_tokens if token in searchable_text)
            if match_score > 0 or not query_tokens:
                results.append((match_score, rec))

        # Sort by match score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results]

    def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        for rec in self.records:
            if rec.get("id") == record_id:
                return rec
        return None

    def get_categories(self) -> List[str]:
        return sorted(list({rec.get("category") for rec in self.records if rec.get("category")}))

    def format_safe_answer(self, query: str) -> str:
        """
        Zero-hallucination query response generator:
        If facts exist, presents them with source URLs and verification status.
        If facts do not exist, explicitly states that the information is unverified.
        """
        matches = self.search(query)
        if not matches:
            return (
                "⚠️ **Fact Not Found in Verified Knowledge Base (Zero-Hallucination Policy)**\n\n"
                f"We currently have no verified official record answering: *'{query}'*.\n\n"
                "To protect travelers from incorrect opening hours, ticket rates, or directions, "
                "we never invent or estimate travel facts. Please consult the official "
                "[Meghalaya Tourism Portal](https://www.meghalayatourism.in/) or ask local registered guides."
            )

        top = matches[0]
        content_en = top.get("content", {}).get("en", "")
        status = top.get("verification_status", "unverified")
        source = top.get("source_name", "Official Source")
        source_url = top.get("source_url", "#")
        location = top.get("location", "Meghalaya")
        safety = top.get("safety_notes", "")
        price = top.get("price_info", "")

        response = [
            f"### 📍 {top.get('title', 'Information')}",
            f"**Location**: {location}",
            f"**Status**: `{status}` | **Source**: [{source}]({source_url})",
            "",
            content_en,
        ]

        if price:
            response.append(f"\n💵 **Tickets / Pricing**: {price}")
        if safety:
            response.append(f"\n⚠️ **Safety Guidance**: {safety}")

        return "\n".join(response)
