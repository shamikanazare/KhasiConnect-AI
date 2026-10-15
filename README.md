# KhasiConnect AI — Datasets & Language Resources

> **AI-Powered Khasi Language Learning, Translation, and Digital Accessibility**  
> Multimodal dataset pipeline and benchmarks for Khasi NLP, Machine Translation, Optical Character Recognition, and Speech Assistance.

---

## 👥 Teammate Guide: Setup in 60 Seconds

If you are a teammate joining the project, follow these simple steps in **PowerShell**:

### Step 1: Clone the Repository
```powershell
git clone https://github.com/shamikanazare/KhasiConnect-AI.git
cd KhasiConnect-AI
```

### Step 2: Run the One-Click Setup Script
```powershell
.\setup_datasets.ps1
```

> **Note**: If PowerShell shows a script execution policy error, run:
> ```powershell
> powershell -ExecutionPolicy Bypass -File .\setup_datasets.ps1
> ```

That's it! The script will automatically:
- Verify Python 3.10+
- Install dependencies (`pip install -r requirements.txt`)
- Download 1.75M+ parallel sentences, 105k+ dictionary entries, and OCR test images
- Verify file counts and run benchmark test cases (TC-01 to TC-07)

---

## 🛠 Manual Step-by-Step PowerShell Commands

If you prefer to run the setup commands manually:

```powershell
# 1. Install Python package dependencies
python -m pip install -r requirements.txt

# 2. Download and organize all datasets across modules
python scripts/download_all_datasets.py

# 3. Verify dataset counts, row numbers, and disk footprint
python scripts/verify_datasets.py

# 4. Run Chapter 7 benchmark tests (TC-01 through TC-07)
python scripts/test_suite_evaluator.py
```

---

## 🌐 How to Push This Repository to GitHub

### 1. Create an Empty Repository on GitHub
1. Open your browser and go to: **[https://github.com/new](https://github.com/new)**
2. Set the repository name to: **`KhasiConnect-AI`**
3. Choose **Public** or **Private**.
4. **Important**: Leave "Add a README file", "Add .gitignore", and "Choose a license" **UNCHECKED** (we already have them configured).
5. Click **Create repository**.

### 2. Push from PowerShell
Run either the automated push script:
```powershell
.\push_to_github.ps1
```

Or run the standard Git commands directly:
```powershell
git remote add origin https://github.com/shamikanazare/KhasiConnect-AI.git
git branch -M main
git push -u origin main
```

---

## 📂 Repository Structure

```text
KhasiConnect-AI/
├── datasets/                                      # Downloaded data (cleanly organized)
│   ├── parallel_translation/                      # Module 2: Translation (1.75M+ sentence pairs)
│   ├── learning_assistant/                        # Module 1: Dictionary & phrases (105k+ words)
│   ├── ocr_image_translation/                     # Module 3: OCR annotations & sample images
│   ├── speech_voice/                              # Module 2: Audio-aligned speech metadata
│   └── shared_language_resource/                  # Unified vocabulary & test suites
│
├── scripts/                                       # Reproducibility & Evaluation Scripts
│   ├── download_all_datasets.py                   # Master dataset downloader
│   ├── verify_datasets.py                         # Storage audit & record verification
│   └── test_suite_evaluator.py                    # Evaluator running TC-01 to TC-07
│
├── setup_datasets.ps1                             # ⚡ 1-click PowerShell setup wizard
├── push_to_github.ps1                             # 🚀 Easy GitHub push helper script
├── requirements.txt                               # Python package dependencies
├── .gitignore                                     # Clean Git configuration for GitHub
├── DATASETS_OVERVIEW.md                           # In-depth dataset specifications
└── README.md                                      # This guide
```

---

## 🤝 Daily Team Collaboration Workflow

When working with teammates on new code or features:

* **Pull latest updates before starting work:**
  ```powershell
  git pull origin main
  ```
* **Save and share your updates:**
  ```powershell
  git add .
  git commit -m "Description of changes made"
  git push origin main
  ```
* **Re-verify tests before pushing:**
  ```powershell
  python scripts/test_suite_evaluator.py
  ```
