#!/bin/bash
# Install GUI dependencies for Liberator

set -e

echo "🎨 Installing Liberator GUI dependencies..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python ${PYTHON_VERSION}"

# Install PyQt6
echo "📦 Installing PyQt6..."
pip3 install PyQt6>=6.6.0

echo ""
echo "✅ GUI dependencies installed successfully!"
echo ""
echo "To run the GUI:"
echo "  python3 liberator_gui.py"
echo ""
echo "Or use the launcher:"
echo "  ./liberator_gui.py"
