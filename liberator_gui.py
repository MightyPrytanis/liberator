#!/usr/bin/env python3
"""
Liberator GUI - Launch script for macOS.
"""

import sys
import os

# Add the liberator package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from liberator.gui.app import main
    main()
except ImportError as e:
    print("Error: PyQt6 is required for the GUI.")
    print("Install it with: pip install PyQt6")
    print(f"\nDetailed error: {e}")
    sys.exit(1)
