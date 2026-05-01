#!/bin/bash
# AlphaVox Server Startup Script

set -e  # Exit on error

echo "=========================================="
echo "🚀 AlphaVox v7 Server Startup"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -q -e .
    python -m spacy download en_core_web_sm
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs memory static/audio templates

# Check environment variables
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Using defaults..."
    echo "   Copy .env.example to .env and configure as needed"
fi

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "📝 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set defaults if not set
export DATABASE_URL=${DATABASE_URL:-sqlite:///alphavox.db}
export SESSION_SECRET=${SESSION_SECRET:-alphavox_dev_secret}
export FLASK_APP=${FLASK_APP:-app.py}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-5000}

# Run system check
echo ""
echo "🔍 Running system check..."
if python system_check.py; then
    echo ""
    echo "✅ System check passed!"
else
    echo ""
    echo "⚠️  System check found issues but continuing..."
fi

echo ""
echo "=========================================="
echo "🌟 Starting AlphaVox Server"
echo "=========================================="
echo "Server will be available at: http://$HOST:$PORT"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask server
python app.py
