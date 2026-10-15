# KhasiConnect AI — Datasets & Language Resources

> **AI-Powered Khasi Language Learning, Translation, and Digital Accessibility**  
> Comprehensive multimodal dataset suite for Khasi Natural Language Processing, Machine Translation, Optical Character Recognition, and Speech Assistance.

---

## 🚀 Quick Start (Automated Setup)

If you have just cloned or received this repository, you can set up all datasets, dependencies, and test benchmarks automatically with a single **PowerShell** command.

### One-Click PowerShell Command:

Open **PowerShell** in this project directory (`e:\AI Project`) and run:

```powershell
.\setup_datasets.ps1
```

> **Note**: If your system restricts running scripts, run with bypass permissions:
> ```powershell
> powershell -ExecutionPolicy Bypass -File .\setup_datasets.ps1
> ```

---

## 🛠 Manual Step-by-Step Setup (PowerShell)

If you prefer to run the steps individually, follow these PowerShell commands:

### Step 1: Install Required Python Packages
```powershell
python -m pip install -r requirements.txt
```

### Step 2: Download & Organize All Datasets
```powershell
python scripts/download_all_datasets.py
```
*This downloads the 1.75M+ parallel sentences, 105k+ dictionary words, OCR benchmarks, and sample images into their designated directories under `datasets/`.*

### Step 3: Audit & Verify Dataset Integrity
```powershell
python scripts/verify_datasets.py
```

### Step 4: Run Chapter 7 Benchmark Tests (TC-01 to TC-07)
```powershell
python scripts/test_suite_evaluator.py
```

---

## 📂 Repository Structure

```text
e:\AI Project\
├── datasets/                                      # Downloaded & organized data
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
├── requirements.txt                               # Python package dependencies
├── .gitignore                                     # Clean Git configuration for GitHub
├── DATASETS_OVERVIEW.md                           # In-depth dataset specifications
└── README.md                                      # This guide
```

---

## 🌐 How to Share this Repository on GitHub

Because this repository uses automated reproducible scripts, you **do not** need to upload 140 MB of large dataset files to GitHub. 

To share with your teammates, guide, or open-source community:

1. **Initialize Git & Commit**:
   ```powershell
   git init
   git add .
   git commit -m "Initialize KhasiConnect AI dataset pipeline, scripts, and shared language resource"
   ```

2. **Push to your GitHub repository**:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/KhasiConnect-AI.git
   git push -u origin main
   ```

3. **How Others Use It**:
   Anyone who clones your repo can simply run:
   ```powershell
   .\setup_datasets.ps1
   ```
   All datasets will immediately download and verify on their machine automatically!
