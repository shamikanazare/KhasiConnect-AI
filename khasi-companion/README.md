# Khasi Companion (KhasiConnect AI)

> **AI-Powered Khasi Language Learning, Translation, and Meghalaya Tourism Assistant**  
> Built with strict separation of language training datasets (System A) and zero-hallucination verified tourism facts (System B).

---

## 🌟 9 Core Principles of This Project

1. **Goal**: Build a reliable, tourist-friendly English ↔ Khasi assistant tailored for travelers and locals in Meghalaya, Northeast India.
2. **Strict Separation of Two Data Systems**:
   - **System A (Language Datasets)**: Parallel English–Khasi sentences and audio files used only to train or test translation and speech models.
   - **System B (Tourism Knowledge Base)**: A curated JSON file (`data/knowledge_base.json`) of verified Meghalaya facts (destinations, transport, culture, safety) with official source links and review dates. We never mix training data with factual tourism answers.
3. **Text-First MVP Priority**: We build a dependable text application first with **Translate**, **Explore Meghalaya**, and **Learn Khasi** modes before adding voice (ASR/TTS) or training heavy models.
4. **Zero-Hallucination Rule**: The assistant must never invent Khasi translations, cultural rules, opening hours, ticket prices, or emergency numbers. If a fact isn't in our verified Knowledge Base, the app explicitly says it doesn't know.
5. **Clear Verification Labels**: Every phrase or translation is marked: `verified_official`, `verified_native_speaker`, `needs_review`, `unverified`, or `outdated`.
6. **Safety-Critical Protections**: Emergency requests, medical questions, or severe food allergy queries never rely on unverified machine translation alone; they immediately direct users to verified human help (Emergency: **112**).
7. **Dataset & License Discipline**: Inspect columns, check empty/corrupted rows, and verify licenses in `data/source_inventory.csv` before training models.
8. **Colab / Jupyter Workflow**: Simple Jupyter/Colab notebook (`notebooks/01_inspect_and_prepare.ipynb`) for teammates to inspect and clean dataset folders without requiring ML expertise.
9. **Transparency on Testing**: Automated test suites for schema validation (`scripts/validate_knowledge_base.py`), unit testing (`pytest`), and benchmark verification (TC-01 through TC-07).

---

## ⚡ Quick Start (One-Click Setup)

Open **PowerShell** in the project directory and run:

```powershell
.\setup_datasets.ps1
```

*(If script execution permissions are restricted, run:)*
```powershell
powershell -ExecutionPolicy Bypass -File .\setup_datasets.ps1
```

### What happens automatically:
1. Validates **Python 3.10+**.
2. Installs dependencies (`streamlit`, `datasets`, `pandas`, `pytest`, `huggingface_hub`, etc.).
3. Verifies local datasets across all modules.
4. Audits the Tourism Knowledge Base schema (0 errors).
5. Runs the automated `pytest` suite.
6. Runs the Chapter 7 benchmark tests (TC-01 to TC-07).

---

## 🖥️ Launching the Web App (Text MVP)

To start the interactive Streamlit assistant:

```powershell
streamlit run app.py
```

This launches the web interface with 3 modes:
* **🔤 Translate (English ↔ Khasi)**: Verified phrase lookup with safety warnings for medical/emergency phrases.
* **🗺️ Explore Meghalaya**: Search destinations, transport hubs, and safety rules strictly backed by the verified knowledge base.
* **📖 Learn Khasi**: Essential everyday phrasebook and traditional cultural pillars (*Tip Kur, Tip Kha*, *Kamai ïa ka Hok*).

---

## 📓 Google Colab / Jupyter Notebook Guide

For teammates who prefer Google Colab or Jupyter without terminal commands:

1. Open **[Google Colab](https://colab.research.google.com/)** and open `notebooks/01_inspect_and_prepare.ipynb`.
2. Run **Cell 1** to mount Google Drive or access the local dataset folder.
3. Run **Cell 2** to automatically inspect row counts, columns, nulls, duplicates, and audio files.
4. Run **Cell 3** to validate `data/knowledge_base.json`.

---

## 🛠 Useful Terminal / PowerShell Commands

| Task | Command |
| :--- | :--- |
| **Launch App** | `streamlit run app.py` |
| **Inspect Datasets** | `python scripts/inspect_datasets.py` |
| **Validate Knowledge Base** | `python scripts/validate_knowledge_base.py` |
| **Run Pytest Tests** | `python -m pytest` |
| **Run TC-01 to TC-07 Benchmark** | `python scripts/test_suite_evaluator.py` |
| **Push Updates to GitHub** | `git add . ; git commit -m "update message" ; git push origin main` |

---

## 📂 Project Structure

```text
khasi-companion/
├── app.py                           # Main Streamlit web app (Text MVP)
├── README.md                        # Project guide for your team
├── requirements.txt                 # Pinned dependencies
├── pytest.ini                       # Pytest test configuration
├── setup_datasets.ps1               # 1-click automated setup wizard
├── push_to_github.ps1               # Git push helper script
│
├── notebooks/
│   └── 01_inspect_and_prepare.ipynb # Colab/Jupyter inspection guide
│
├── data/
│   ├── knowledge_base.json          # Verified tourism facts (System B)
│   ├── phrasebook.json              # Reviewed & unverified phrases
│   ├── source_inventory.csv         # Dataset license & source tracker
│   └── raw_datasets/                # Shared raw dataset folder
│
├── datasets/                        # Full multi-modal dataset archive
│   ├── parallel_translation/       # 1.75M+ parallel sentence pairs
│   ├── learning_assistant/         # 105k+ dictionary & phrases
│   ├── ocr_image_translation/      # 2,000 OCR lines & sample crops
│   ├── speech_voice/               # BhasaFlow audio alignment metadata
│   └── shared_language_resource/   # Chapter 7 test suite (TC-01 to TC-07)
│
├── scripts/
│   ├── inspect_datasets.py          # Automatic dataset scanner
│   ├── validate_knowledge_base.py   # Schema & safety rules validator
│   ├── download_all_datasets.py     # Master dataset downloader
│   ├── verify_datasets.py           # Integrity checker
│   └── test_suite_evaluator.py      # Benchmark runner (TC-01 to TC-07)
│
├── src/
│   ├── __init__.py
│   ├── retrieval.py                 # Safe tourism search (Zero-Hallucination)
│   └── translation.py               # Phrasebook lookup & safety guards
│
└── tests/
    ├── test_knowledge_base.py       # Automated test for knowledge base schema
    └── test_retrieval.py            # Automated tests for tourism retrieval & safety
```
