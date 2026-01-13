"""
macOS-specific menu bar integration.
"""

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt


def create_macos_menu_bar(window, app):
    """Create macOS-style menu bar."""
    menubar = window.menuBar()
    
    # App menu (macOS specific)
    app_menu = menubar.addMenu("Liberator")
    
    about_action = QAction("About Liberator", window)
    about_action.triggered.connect(lambda: window.show_about_dialog())
    app_menu.addAction(about_action)
    
    app_menu.addSeparator()
    
    preferences_action = QAction("Preferences...", window)
    preferences_action.setShortcut(QKeySequence("Ctrl+,"))
    preferences_action.triggered.connect(lambda: window.show_preferences())
    app_menu.addAction(preferences_action)
    
    app_menu.addSeparator()
    
    quit_action = QAction("Quit Liberator", window)
    quit_action.setShortcut(QKeySequence("Ctrl+Q"))
    quit_action.triggered.connect(app.quit)
    app_menu.addAction(quit_action)
    
    # File menu
    file_menu = menubar.addMenu("File")
    
    open_action = QAction("Open Project...", window)
    open_action.setShortcut(QKeySequence("Ctrl+O"))
    open_action.triggered.connect(window.select_source_path)
    file_menu.addAction(open_action)
    
    file_menu.addSeparator()
    
    exit_action = QAction("Exit", window)
    exit_action.setShortcut(QKeySequence("Ctrl+Q"))
    exit_action.triggered.connect(app.quit)
    file_menu.addAction(exit_action)
    
    # Edit menu
    edit_menu = menubar.addMenu("Edit")
    
    # View menu
    view_menu = menubar.addMenu("View")
    
    # Help menu
    help_menu = menubar.addMenu("Help")
    
    help_action = QAction("Liberator Help", window)
    help_action.setShortcut(QKeySequence("F1"))
    help_action.triggered.connect(lambda: window.show_help())
    help_menu.addAction(help_action)
    
    help_menu.addSeparator()
    
    about_qt_action = QAction("About Qt", window)
    about_qt_action.triggered.connect(lambda: QMessageBox.aboutQt(window))
    help_menu.addAction(about_qt_action)
    
    return menubar
