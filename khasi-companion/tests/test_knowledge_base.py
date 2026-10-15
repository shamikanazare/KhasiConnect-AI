from pathlib import Path
from scripts.validate_knowledge_base import validate_kb

def test_knowledge_base_schema():
    kb_path = Path("data/knowledge_base.json")
    assert validate_kb(kb_path) is True
