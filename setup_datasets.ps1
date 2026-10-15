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
Write-Host "      KHASI COMPANION / KHASICONNECT AI - SETUP WIZARD       " -ForegroundColor Green
Write-Host "  AI-Powered Tourist and Language Assistant for Meghalaya    " -ForegroundColor Yellow
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
    python -m pip install streamlit datasets pandas pytest huggingface_hub openpyxl pyarrow tqdm
}

# 3. Download & Organize Datasets
Print-Header "Step 3: Checking and Fetching Datasets"
Write-Host "Checking datasets across all modules..." -ForegroundColor Gray
try {
    python scripts/download_all_datasets.py
    Print-Success "Datasets verified in datasets/ and data/raw_datasets/ directories."
} catch {
    Print-Failure "An error occurred during dataset download: $_"
    exit 1
}

# 4. Validate Tourism Knowledge Base (System B)
Print-Header "Step 4: Validating Tourism Knowledge Base (Zero-Hallucination Schema)"
try {
    python scripts/validate_knowledge_base.py
    Print-Success "Knowledge base schema validated with 0 errors."
} catch {
    Print-Failure "Knowledge base validation failed: $_"
    exit 1
}

# 5. Run Automated Tests
Print-Header "Step 5: Running Pytest Test Suite"
try {
    python -m pytest tests --quiet
    Print-Success "All automated tests passed."
} catch {
    Print-Failure "Tests failed: $_"
    exit 1
}

# 6. Run Chapter 7 Benchmark Evaluator
Print-Header "Step 6: Executing Chapter 7 Benchmark Tests (TC-01 to TC-07)"
try {
    python scripts/test_suite_evaluator.py
    Print-Success "Benchmark evaluations (TC-01 to TC-07) executed successfully."
} catch {
    Print-Failure "Benchmark evaluation failed: $_"
    exit 1
}

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "  SETUP COMPLETE! Khasi Companion is ready to run.            " -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "`nCommands you can run right now:" -ForegroundColor White
Write-Host "  * Launch Web App:       streamlit run app.py" -ForegroundColor Yellow
Write-Host "  * Inspect Datasets:     python scripts/inspect_datasets.py" -ForegroundColor Yellow
Write-Host "  * Validate Knowledge:   python scripts/validate_knowledge_base.py" -ForegroundColor Yellow
Write-Host "  * Run Test Suite:       python -m pytest" -ForegroundColor Yellow
Write-Host ""
