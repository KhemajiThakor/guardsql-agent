#!/bin/bash

echo "🛡️  GuardSQL Agent - Quick Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "❌ Python 3.11+ required"; exit 1; }

# Check PostgreSQL
echo "Checking PostgreSQL..."
psql --version || { echo "❌ PostgreSQL required"; exit 1; }

# Check Ollama
echo "Checking Ollama..."
ollama --version || { echo "⚠️  Ollama not found. Install from https://ollama.com"; }

echo ""
echo "✅ Prerequisites check complete"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your database credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Setup database: sudo -u postgres psql -f complete_setup.sql"
echo "2. Pull Ollama model: ollama pull phi3:3.8b"
echo "3. Start Ollama: ollama serve"
echo "4. Start backend: python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
echo "5. Start frontend: streamlit run frontend/src/app.py"
echo ""
echo "📚 See README.md for detailed instructions"
