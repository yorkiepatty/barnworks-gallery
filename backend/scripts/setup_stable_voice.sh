#!/bin/bash
# Quick Voice Fix Environment Setup

echo "🎤 Setting up AlphaVox voice stability..."

# Set basic AWS region (even without credentials, helps routing)
export AWS_REGION=us-east-1

# Voice stability flags
export ALPHAVOX_VOICE_LOCK=true
export ALPHAVOX_DEFAULT_VOICE=matthew
export ALPHAVOX_PREVENT_SWITCHING=true

# Force single TTS engine preference
export ALPHAVOX_TTS_ENGINE=gtts  # Use gTTS for consistency if no AWS

echo "✅ Voice environment configured"
echo "   Locked voice: matthew"
echo "   Switching prevention: enabled"
echo ""
echo "Now run: python app.py"
