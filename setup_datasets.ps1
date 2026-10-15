[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

function Print-Header {
    param([string]$Text)
    Write-Host "`n========================================================" -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host "========================================================" -ForegroundColor Cyan
}

function Print-Success {
    param([string]$Text)
    Write-Host "[SUCCESS] $Text" -ForegroundColor Green
}

function Print-Warning {
    param([string]$Text)
    Write-Host "[WARNING] $Text" -ForegroundColor Yellow
}

function Print-Failure {
    param([string]$Text)
    Write-Host "[ERROR] $Text" -ForegroundColor Red
}

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "          KHASICONNECT AI - DATASET SETUP WIZARD             " -ForegroundColor Green
Write-Host " AI-Powered Khasi Language Learning, Translation and OCR      " -ForegroundColor Yellow
Write-Host "==============================================================" -ForegroundColor Green

# 1. Check Python
Print-Header "Step 1: Checking Python Environment"
try {
    $pythonVersion = python --version 2>&1
    Print-Success "Python detected: $pythonVersion"
} catch {
    Print-Failure "Python was not found in your PATH!"
    Write-Host "Please install Python 3.10+ from https://www.python.org/ or Microsoft Store."
    exit 1
}

# 2. Install Dependencies
Print-Header "Step 2: Installing Python Dependencies"
Write-Host "Installing requirements from requirements.txt..." -ForegroundColor Gray
try {
    python -m pip install -r requirements.txt --quiet
    Print-Success "All dependencies installed successfully."
} catch {
    Print-Warning "Pip encountered an issue. Retrying with direct install..."
    python -m pip install huggingface_hub pyarrow pandas tqdm
}

# 3. Download & Organize Datasets
Print-Header "Step 3: Downloading and Organizing Khasi Datasets"
Write-Host "Checking and fetching datasets across all modules..." -ForegroundColor Gray
try {
    python scripts/download_all_datasets.py
    Print-Success "Datasets verified in datasets/ directory."
} catch {
    Print-Failure "An error occurred during dataset download: $_"
    exit 1
}

# 4. Audit & Verification
Print-Header "Step 4: Running Dataset Integrity Audit"
try {
    python scripts/verify_datasets.py
    Print-Success "Dataset verification completed successfully."
} catch {
    Print-Failure "Verification check failed: $_"
    exit 1
}

# 5. Run Test Suite Evaluator (TC-01 to TC-07)
Print-Header "Step 5: Executing Chapter 7 Benchmark Tests (TC-01 to TC-07)"
try {
    python scripts/test_suite_evaluator.py
    Print-Success "Benchmark evaluations (TC-01 to TC-07) executed successfully."
} catch {
    Print-Failure "Benchmark evaluation failed: $_"
    exit 1
}

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "  SETUP COMPLETE! KhasiConnect AI datasets are ready to use.  " -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "`nNext commands you can run in PowerShell:" -ForegroundColor White
Write-Host "  • Audit files:        python scripts/verify_datasets.py" -ForegroundColor Yellow
Write-Host "  • Run Test Cases:     python scripts/test_suite_evaluator.py" -ForegroundColor Yellow
Write-Host "  • Dataset Catalog:    Get-Content DATASETS_OVERVIEW.md" -ForegroundColor Yellow
Write-Host ""
