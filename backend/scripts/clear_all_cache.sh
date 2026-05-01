#!/bin/bash
# AlphaVox Cache Clearing Script
# Removes ALL Python cache and compiled files to ensure clean imports

echo "🧹 Clearing all Python cache files..."

# Remove __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✅ Removed __pycache__ directories"

# Remove .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✅ Removed .pyc files"

# Remove .pyo files
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "✅ Removed .pyo files"

# Remove .pyd files (Windows compiled)
find . -type f -name "*.pyd" -delete 2>/dev/null
echo "✅ Removed .pyd files"

# Remove .so files (compiled extensions) - CAREFUL with this one
# Commented out by default - uncomment if you're sure
# find . -type f -name "*.so" -delete 2>/dev/null
# echo "✅ Removed .so files"

# Remove pytest cache
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
echo "✅ Removed pytest cache"

# Remove coverage files
find . -type f -name ".coverage" -delete 2>/dev/null
find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null
echo "✅ Removed coverage files"

# Remove mypy cache
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null
echo "✅ Removed mypy cache"

# Remove ruff cache
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null
echo "✅ Removed ruff cache"

echo ""
echo "🎉 All Python cache cleared!"
echo ""
echo "Now run:"
echo "  python alphavox_module_loader.py"
