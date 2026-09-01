#!/bin/bash

# Resume Analyzer - Quick Start Script for macOS/Linux

echo "============================================"
echo "Sales & Business Development Resume Analyzer"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python found: $PYTHON_VERSION"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

echo ""
echo "============================================"
echo "🚀 Launching Resume Analyzer..."
echo "============================================"
echo ""
echo "The app will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit app
streamlit run app.py
