"""
Liberator GUI Application entry point.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
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
    
    # Apply global metallic theme
    from .theme import MAIN_WINDOW_STYLE
    app.setStyleSheet(MAIN_WINDOW_STYLE)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
