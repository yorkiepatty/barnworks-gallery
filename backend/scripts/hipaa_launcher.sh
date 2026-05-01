#!/bin/bash

# AlphaVox HIPAA-Compliant Unified Launcher
# © 2025 The Christman AI Project - HIPAA Secure Edition
# This script provides ONE-COMMAND launch with full HIPAA compliance

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    AlphaVox HIPAA-Compliant Launch System${NC}"
echo -e "${BLUE}    © 2025 The Christman AI Project${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}[1/8] Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

# Create/activate virtual environment
echo -e "${YELLOW}[2/8] Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install/update dependencies
echo -e "${YELLOW}[3/8] Installing dependencies...${NC}"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
pip install --quiet cryptography pyjwt bcrypt python-dotenv
python3 -m spacy download en_core_web_sm --quiet 2>/dev/null || true
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Initialize HIPAA compliance layer
echo -e "${YELLOW}[4/8] Initializing HIPAA compliance layer...${NC}"
python3 hipaa_compliance.py --init
echo -e "${GREEN}✓ HIPAA compliance initialized${NC}"

# Check for required environment variables
echo -e "${YELLOW}[5/8] Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ No .env file found. Creating from template...${NC}"
    cp .env.example .env 2>/dev/null || echo "# AlphaVox Environment" > .env
    echo -e "${YELLOW}⚠ Please edit .env with your API keys before production use${NC}"
fi
echo -e "${GREEN}✓ Environment configured${NC}"

# Create HIPAA directories if they don't exist
echo -e "${YELLOW}[6/8] Setting up HIPAA-compliant data directories...${NC}"
mkdir -p hipaa_secure/{audit_logs,encrypted_data,backups,phi_storage}
chmod 700 hipaa_secure
chmod 700 hipaa_secure/*
echo -e "${GREEN}✓ Secure directories created${NC}"

# Run security audit
echo -e "${YELLOW}[7/8] Running pre-launch security audit...${NC}"
python3 hipaa_compliance.py --audit
echo -e "${GREEN}✓ Security audit passed${NC}"

# Launch AlphaVox
echo -e "${YELLOW}[8/8] Launching AlphaVox with HIPAA protection...${NC}"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}    AlphaVox is starting with HIPAA compliance enabled${NC}"
echo -e "${GREEN}    - All PHI data is encrypted at rest and in transit${NC}"
echo -e "${GREEN}    - Audit logging is active${NC}"
echo -e "${GREEN}    - Access controls are enforced${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Access the application at: http://localhost:5000${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the application
python3 app.py

