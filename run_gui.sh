#!/bin/bash
# Quick launcher for Liberator GUI

cd "$(dirname "$0")"

# Check if PyQt6 is installed
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "⚠️  PyQt6 is not installed."
    echo "Installing PyQt6..."
    pip3 install PyQt6
    echo ""
fi

# Run the GUI
python3 liberator_gui.py "$@"
