import json
import sys
from pathlib import Path

REQUIRED_KB_FIELDS = {
    "id",
    "category",
    "title",
    "content",
    "language",
    "source_name",
    "source_url",
    "verification_status",
    "last_reviewed",
    "notes"
}

ALLOWED_STATUSES = {
    "verified_official",
    "verified_native_speaker",
    "needs_review",
    "unverified",
    "outdated"
}

def validate_kb(kb_path: Path) -> bool:
    if not kb_path.exists():
        print(f"[ERROR] File not found: {kb_path}")
        return False

    with open(kb_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list) or len(records) == 0:
        print("[ERROR] knowledge_base.json must be a non-empty list of records.")
        return False

    all_valid = True
    seen_ids = set()

    for idx, rec in enumerate(records):
        rec_id = rec.get("id", f"index_{idx}")
        if rec_id in seen_ids:
            print(f"[ERROR] Duplicate ID found: {rec_id}")
            all_valid = False
        seen_ids.add(rec_id)

        missing = REQUIRED_KB_FIELDS - set(rec.keys())
        if missing:
            print(f"[ERROR] Record {rec_id} is missing required fields: {missing}")
            all_valid = False

        status = rec.get("verification_status")
        if status not in ALLOWED_STATUSES:
            print(f"[ERROR] Record {rec_id} has invalid verification_status: '{status}'")
            all_valid = False

        if not str(rec.get("source_url", "")).startswith(("http://", "https://")):
            print(f"[ERROR] Record {rec_id} must have a valid http/https source_url.")
            all_valid = False

    if all_valid:
        print(f"[SUCCESS] Validated {len(records)} records in {kb_path} with 0 errors!")
    return all_valid

if __name__ == "__main__":
    kb_file = Path("data/knowledge_base.json")
    success = validate_kb(kb_file)
    sys.exit(0 if success else 1)
