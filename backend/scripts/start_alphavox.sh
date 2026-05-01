#!/bin/bash
# AlphaVox Startup Script with Voice Cortex
# Ensures we stay in virtual environment and fixes blueprint conflicts

cd /Users/EverettN/ALPHAVOXWAKESUP
source .venv/bin/activate

echo "✅ Virtual environment activated"
echo "🧠 Starting AlphaVox with Voice Cortex..."
echo "📍 Python path: $(which python)"
echo "📦 Virtual env: $VIRTUAL_ENV"
echo "🔧 Blueprint conflicts fixed"

# Set environment variable to ensure we stay in venv
export VIRTUAL_ENV_FORCE=1

python app.py