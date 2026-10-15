from src.retrieval import TourismKnowledgeRetriever
from src.translation import TranslationService

def test_knowledge_base_retrieval():
    retriever = TourismKnowledgeRetriever()
    results = retriever.search("Nohkalikai")
    assert len(results) > 0
    assert "Nohkalikai" in results[0]["title"]
    assert results[0]["verification_status"] in {"needs_review", "verified_official"}

def test_zero_hallucination_unknown_query():
    retriever = TourismKnowledgeRetriever()
    results = retriever.search("Eiffel Tower Paris")
    assert len(results) == 0
    answer = retriever.format_safe_answer("Eiffel Tower Paris")
    assert "Zero-Hallucination Policy" in answer

def test_translation_safety_critical_detection():
    service = TranslationService()
    result = service.translate("I need a doctor immediately")
    assert result["safety_critical"] is True

def test_translation_unverified_not_fabricated():
    service = TranslationService()
    # PHRASE-001 is unverified and blank in phrasebook.json
    result = service.translate("Hello / Greetings")
    assert result["verification_status"] == "unverified"
    assert result["translation"] == ""
