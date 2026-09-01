# Resume Analyzer - Quick Start Script for Windows PowerShell

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Sales & Business Development Resume Analyzer" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
$venvPath = ".\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

Write-Host ""

# Install requirements
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q
Write-Host "✅ Dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🚀 Launching Resume Analyzer..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your browser at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

# Run Streamlit app
streamlit run app.py
