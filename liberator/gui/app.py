"""
Liberator GUI Application entry point.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .main_window import MainWindow


def main():
    """Main entry point for GUI application."""
    # Enable high DPI scaling on macOS
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Liberator")
    app.setOrganizationName("Liberator Project")
    
    # Set application icon
    icon_paths = [
        Path(__file__).parent.parent.parent / 'assets' / 'icon.png',
        Path(__file__).parent.parent.parent / 'assets' / 'icon_512x512.png',
        Path(__file__).parent.parent.parent / 'assets' / 'icon_256x256.png',
    ]
    
    for icon_path in icon_paths:
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
            break
    
    # Apply global metallic theme
    from .theme import MAIN_WINDOW_STYLE
    app.setStyleSheet(MAIN_WINDOW_STYLE)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
