#!/usr/bin/env python3
"""
Run the Liberator Setup Wizard.
"""

import sys
import os

# Add the liberator package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from liberator.gui.setup_wizard import run_setup_wizard
    run_setup_wizard()
except ImportError as e:
    print("Error: PyQt6 is required for the setup wizard.")
    print("Install it with: pip install PyQt6")
    print(f"\nDetailed error: {e}")
    sys.exit(1)
