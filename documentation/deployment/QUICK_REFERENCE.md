# AlphaVox Quick Reference Guide

## 🚀 Starting the System

```bash

# Easiest method - use the startup script

./start_server.sh

# Or manually

source venv/bin/activate
python app.py
```text
## 🔍 System Check

```bash

# Run full system diagnostics

python system_check.py

# Should show: ✅ SYSTEM IS OPERATIONAL

```text
## 🌐 Access URLs

| Feature | URL |
|---------|-----|
| Main Interface | <http://localhost:5000> |
| Hardware Test | <http://localhost:5000/public/hardware-test> |
| Voice Test | <http://localhost:5000/simple_voice_test> |
| Symbol Interface | <http://localhost:5000/symbols> |
| AI Control | <http://localhost:5000/ai_control> |
| Learning Hub | <http://localhost:5000/learning> |
| Behavior Capture | <http://localhost:5000/behavior-test> |

## 📝 Common Commands

### Database

```bash

# Reset database

rm alphavox.db
python -c "from app_init import app, db; app.app_context().push(); db.create_all()"

# Backup database

cp alphavox.db alphavox.db.backup
```text
### Dependencies

```bash

# Install/update dependencies

pip install -e .

# Install spaCy language model

python -m spacy download en_core_web_sm

# Install missing OpenGL libraries (if needed)

sudo apt-get install -y libgl1 libglib2.0-0
```text
### Maintenance

```bash

# Clear audio cache

rm -rf static/audio/*.mp3

# Clear logs

rm -rf logs/*.log

# Check disk usage

du -sh data/ logs/ memory/ static/audio/
```text
## 🔧 Configuration

### Environment Variables (.env file)

```bash
DATABASE_URL=sqlite:///alphavox.db
SESSION_SECRET=your-secret-key
ANTHROPIC_API_KEY=your-api-key  # Optional
OPENAI_API_KEY=your-api-key     # Optional
PORT=5000
```text
## 🎯 Key Features

### 1. Text Communication

- Navigate to main interface
- Enter text in input box
- System analyzes intent and emotional context
- Generates appropriate speech response

### 2. Symbol Communication

- Click symbols on interface
- System translates to speech
- Customizable symbol sets

### 3. Gesture Recognition

- Uses camera/simulated gestures
- Interprets emotional states
- Generates appropriate responses

### 4. Learning System

- Tracks user progress
- Adapts to communication patterns
- Provides caregiver insights

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Change PORT in .env or use `PORT=8080 python app.py` |
| Module not found | Run `pip install -e .` |
| Database locked | Close other connections, restart server |
| Audio not playing | Check browser audio permissions |
| Camera access denied | Grant browser camera permissions |

## 📊 Module Overview

| Module | Purpose |
|--------|---------|
| **app.py** | Main Flask application |
| **main.py** | alphavox AI dashboard |
| **alphavox_input_nlu.py** | Advanced NLU with root cause analysis |
| **nonverbal_engine.py** | Gesture and emotion recognition |
| **conversation_engine.py** | Advanced conversational AI |
| **memory_engine.py** | Persistent context management |
| **ai_learning_engine.py** | Self-improvement system |
| **neural_learning_core.py** | Deep learning integration |
| **advanced_tts_service.py** | Emotional text-to-speech |
| **learning_analytics.py** | Progress tracking |
| **behavior_capture.py** | Behavioral analysis |

## 🔐 Production Deployment

```bash

# Install production dependencies

pip install gunicorn

# Run with Gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or use the AWS deployment guide

cat AWS_DEPLOYMENT.md
```text
## 📈 Monitoring

```bash

# View logs

tail -f logs/alphavox_dashboard.log
tail -f logs/alphavox.log

# Monitor system resources

htop
df -h
```text
## 💡 Tips

1. **First Time Setup:** Run system_check.py to verify everything
2. **API Keys:** Only needed for advanced AI features
3. **Database:** SQLite is fine for development, PostgreSQL for production
4. **Audio:** Make sure browser has audio permissions
5. **Camera:** Required for eye tracking and behavior capture

## 🆘 Getting Help

1. Check SYSTEM_OPERATIONAL_REPORT.md for detailed info
2. Review logs in logs/ directory
3. Run system_check.py for diagnostics
4. Check README.md for feature documentation
5. Review AWS_DEPLOYMENT.md for deployment issues

---

**Status:** ✅ System Operational
**Last Checked:** October 12, 2025
**Version:** AlphaVox v7
