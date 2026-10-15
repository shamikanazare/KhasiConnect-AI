"""
Khasi Companion - Translation Engine (System A: Language Datasets & Phrasebook)
Enforces Verification Labels and Safety-Critical Protections.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

DEFAULT_PHRASEBOOK = Path(__file__).resolve().parent.parent / "data" / "phrasebook.json"
DEFAULT_VOCAB = Path(__file__).resolve().parent.parent / "datasets" / "shared_language_resource" / "verified_vocabulary.csv"

# Critical emergency / medical keywords that trigger safety warnings
SAFETY_CRITICAL_KEYWORDS = {
    "doctor", "hospital", "emergency", "ambulance", "police", "fire",
    "die", "poison", "allergy", "allergic", "bleeding", "snake", "injury", "112"
}

class TranslationService:
    def __init__(self, phrasebook_path: Optional[Path] = None):
        self.phrasebook_path = phrasebook_path or DEFAULT_PHRASEBOOK
        self.phrases: List[Dict[str, Any]] = []
        self.load_phrasebook()

    def load_phrasebook(self):
        if not self.phrasebook_path.exists():
            self.phrases = []
            return
        with open(self.phrasebook_path, "r", encoding="utf-8") as f:
            self.phrases = json.load(f)

    def is_safety_critical(self, text: str) -> bool:
        tokens = set(text.lower().replace("?", "").replace("!", "").split())
        return bool(tokens & SAFETY_CRITICAL_KEYWORDS)

    def translate(self, text: str, source_lang: str = "en", target_lang: str = "kha") -> Dict[str, Any]:
        """
        Translates text with verification status auditing and safety guards.
        """
        clean_text = text.strip()
        is_critical = self.is_safety_critical(clean_text)

        # Check phrasebook
        match = None
        for p in self.phrases:
            src_val = p.get("english", "") if source_lang == "en" else p.get("khasi", "")
            if src_val.lower().strip() == clean_text.lower():
                match = p
                break

        if match:
            tgt_val = match.get("khasi") if target_lang == "kha" else match.get("english")
            status = match.get("verification_status", "unverified")

            # Rule 6 & 7: If unverified and blank, do not fabricate
            if not tgt_val:
                return {
                    "source": clean_text,
                    "translation": "",
                    "pronunciation": "",
                    "verification_status": "unverified",
                    "safety_critical": is_critical,
                    "message": "⚠️ This phrase is logged in our phrasebook but its Khasi translation is currently marked UNVERIFIED. Per project rules, we do not fabricate unverified translations.",
                    "notes": match.get("notes", "")
                }

            return {
                "source": clean_text,
                "translation": tgt_val,
                "pronunciation": match.get("pronunciation_guide", ""),
                "verification_status": status,
                "safety_critical": is_critical,
                "message": "Verified against local phrasebook.",
                "notes": match.get("notes", "")
            }

        # Fallback response for unmapped phrases
        result = {
            "source": clean_text,
            "translation": "",
            "pronunciation": "",
            "verification_status": "needs_review",
            "safety_critical": is_critical,
            "message": "No direct verified phrasebook match found. Translation needs native speaker review.",
            "notes": "Zero-hallucination policy applied: unverified machine generation withheld."
        }

        if is_critical:
            result["emergency_alert"] = (
                "🚨 **SAFETY-CRITICAL NOTICE**: Do not rely on automated translations for medical "
                "or police emergencies. In Meghalaya, dial **112** (Pan-India Emergency) immediately "
                "or proceed to the nearest Civil Hospital / Community Health Centre."
            )

        return result
