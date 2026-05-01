#!/bin/bash

# 🚀 The Christman AI Project - Complete Experience Launcher
# This script provides easy access to all project materials

clear

echo "🌍 Welcome to The Christman AI Project!"
echo "======================================"
echo ""
echo "Available options:"
echo ""
echo "1. 🎯 Complete Interactive Experience"
echo "2. 🚀 Manifesto Presentation Only"
echo "3. 📚 View Documentation Files"
echo "4. 📦 Access Revolution Package"
echo "5. 🔧 Technical: Run AlphaVox System"
echo ""
echo "0. Exit"
echo ""

read -p "Enter your choice (0-5): " choice

case $choice in
    1)
        echo "🌟 Launching complete Christman AI experience..."
        python3 christman_ai_experience.py
        ;;
    2)
        echo "🚀 Launching manifesto presentation..."
        python3 manifesto_presentation.py
        ;;
    3)
        echo "📚 Available documentation files:"
        echo ""
        echo "📄 THE_CHRISTMAN_AI_PROJECT.md - Project vision and heart"
        echo "📄 THE_CHRISTMAN_AI_MANIFESTO.md - Complete technical manifesto"
        echo "📄 THE_CHRISTMAN_AI_REVOLUTION.md - Revolutionary documentation"
        echo "📄 simple_message.txt - Professional assessment for sharing"
        echo ""
        echo "💡 Tip: Use 'cat filename.md' to view or open in your editor"
        ;;
    4)
        echo "📦 Revolution package contents:"
        echo ""
        if [ -d "christman_ai_revolution_package" ]; then
            ls -la christman_ai_revolution_package/
            echo ""
            echo "✅ Revolution package is ready!"
            echo "🔗 Use ./christman_ai_revolution_package/launch_revolution.sh to deploy"
        else
            echo "❌ Revolution package not found. Run ./create_revolution_package.sh first"
        fi
        ;;
    5)
        echo "🔧 Starting AlphaVox system..."
        echo "📡 Server will run on http://localhost:3000"
        python3 app.py
        ;;
    0)
        echo "Thank you for your interest in The Christman AI Project! 🌟"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please try again."
        ;;
esac

echo ""
echo "Press Enter to continue..."
read
