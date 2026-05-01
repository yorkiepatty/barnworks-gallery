#!/bin/bash
echo "🚀 Launching The Christman AI Revolution Experience..."
echo ""
echo "Choose your experience:"
echo "1) Read the complete revolution story"
echo "2) Watch the interactive demo"
echo "3) Both - full revolutionary experience"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "📖 Opening the revolution document..."
        if command -v code &> /dev/null; then
            code THE_CHRISTMAN_AI_REVOLUTION.md
        elif command -v open &> /dev/null; then
            open THE_CHRISTMAN_AI_REVOLUTION.md
        else
            cat THE_CHRISTMAN_AI_REVOLUTION.md
        fi
        ;;
    2)
        echo "🎭 Starting interactive demo..."
        python3 revolution_demo.py
        ;;
    3)
        echo "🌟 Full revolutionary experience..."
        echo "First, the interactive demo..."
        python3 revolution_demo.py
        echo ""
        echo "📖 Now opening the complete document..."
        if command -v code &> /dev/null; then
            code THE_CHRISTMAN_AI_REVOLUTION.md
        elif command -v open &> /dev/null; then
            open THE_CHRISTMAN_AI_REVOLUTION.md
        else
            cat THE_CHRISTMAN_AI_REVOLUTION.md
        fi
        ;;
    *)
        echo "Invalid choice. Starting demo..."
        python3 revolution_demo.py
        ;;
esac
