"""
Metallic theme for Liberator GUI - Copper, Gold, Bronze, Silver.
"""

# Metallic color palette
METALLIC_COPPER = "#B87333"  # Rich copper
METALLIC_COPPER_LIGHT = "#CD853F"  # Light copper
METALLIC_COPPER_DARK = "#8B4513"  # Dark copper

METALLIC_GOLD = "#D4AF37"  # Classic gold
METALLIC_GOLD_LIGHT = "#FFD700"  # Bright gold
METALLIC_GOLD_DARK = "#B8860B"  # Dark gold

METALLIC_BRONZE = "#CD7F32"  # Bronze
METALLIC_BRONZE_LIGHT = "#E6A857"  # Light bronze
METALLIC_BRONZE_DARK = "#8B4513"  # Dark bronze

METALLIC_SILVER = "#C0C0C0"  # Silver
METALLIC_SILVER_LIGHT = "#E8E8E8"  # Light silver
METALLIC_SILVER_DARK = "#808080"  # Dark silver

# Gradient colors for metallic effect
COPPER_GRADIENT = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #D2691E, stop:1 #8B4513)"
GOLD_GRADIENT = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFD700, stop:1 #B8860B)"
BRONZE_GRADIENT = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E6A857, stop:1 #8B4513)"
SILVER_GRADIENT = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E8E8E8, stop:1 #808080)"

# Background colors
BG_PRIMARY = "#2C2C2C"  # Dark background
BG_SECONDARY = "#3A3A3A"  # Slightly lighter
BG_TERTIARY = "#4A4A4A"  # Even lighter

# Text colors
TEXT_PRIMARY = "#E8E8E8"  # Light text
TEXT_SECONDARY = METALLIC_SILVER  # Silver text
TEXT_ACCENT = METALLIC_GOLD  # Gold accent text

# Button styles
BUTTON_PRIMARY = f"""
    QPushButton {{
        background: {GOLD_GRADIENT};
        color: #1A1A1A;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid {METALLIC_GOLD_DARK};
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFE55C, stop:1 #D4AF37);
        border: 2px solid {METALLIC_GOLD};
    }}
    QPushButton:pressed {{
        background: {METALLIC_GOLD_DARK};
    }}
    QPushButton:disabled {{
        background: #555555;
        color: #888888;
        border: 2px solid #444444;
    }}
"""

BUTTON_SECONDARY = f"""
    QPushButton {{
        background: {COPPER_GRADIENT};
        color: #1A1A1A;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid {METALLIC_COPPER_DARK};
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #CD853F, stop:1 #B87333);
        border: 2px solid {METALLIC_COPPER};
    }}
    QPushButton:pressed {{
        background: {METALLIC_COPPER_DARK};
    }}
"""

BUTTON_SUCCESS = f"""
    QPushButton {{
        background: {BRONZE_GRADIENT};
        color: #1A1A1A;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: 2px solid {METALLIC_BRONZE_DARK};
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E6A857, stop:1 #CD7F32);
        border: 2px solid {METALLIC_BRONZE};
    }}
    QPushButton:pressed {{
        background: {METALLIC_BRONZE_DARK};
    }}
"""

BUTTON_NEUTRAL = f"""
    QPushButton {{
        background: {SILVER_GRADIENT};
        color: #1A1A1A;
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 6px;
        border: 2px solid {METALLIC_SILVER_DARK};
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F0F0F0, stop:1 #C0C0C0);
        border: 2px solid {METALLIC_SILVER};
    }}
    QPushButton:pressed {{
        background: {METALLIC_SILVER_DARK};
    }}
"""

# Main window style
MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {BG_PRIMARY};
        color: {TEXT_PRIMARY};
    }}
    
    QWidget {{
        background-color: {BG_PRIMARY};
        color: {TEXT_PRIMARY};
    }}
    
    QTabWidget::pane {{
        border: 2px solid {METALLIC_SILVER_DARK};
        background-color: {BG_SECONDARY};
        border-radius: 5px;
    }}
    
    QTabBar::tab {{
        background: {SILVER_GRADIENT};
        color: #1A1A1A;
        padding: 10px 20px;
        margin-right: 2px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        border: 1px solid {METALLIC_SILVER_DARK};
    }}
    
    QTabBar::tab:selected {{
        background: {GOLD_GRADIENT};
        color: #1A1A1A;
        border: 2px solid {METALLIC_GOLD};
    }}
    
    QTabBar::tab:hover {{
        background: {COPPER_GRADIENT};
    }}
    
    QGroupBox {{
        border: 2px solid {METALLIC_COPPER};
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
        font-weight: bold;
        color: {METALLIC_GOLD};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        color: {METALLIC_GOLD};
    }}
    
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
        border: 2px solid {METALLIC_SILVER_DARK};
        border-radius: 5px;
        padding: 5px;
    }}
    
    QLineEdit:focus, QTextEdit:focus {{
        border: 2px solid {METALLIC_GOLD};
    }}
    
    QComboBox {{
        background-color: {BG_TERTIARY};
        color: {TEXT_PRIMARY};
        border: 2px solid {METALLIC_SILVER_DARK};
        border-radius: 5px;
        padding: 5px;
    }}
    
    QComboBox:hover {{
        border: 2px solid {METALLIC_COPPER};
    }}
    
    QComboBox::drop-down {{
        border: none;
        background: {COPPER_GRADIENT};
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {BG_SECONDARY};
        color: {TEXT_PRIMARY};
        selection-background-color: {METALLIC_GOLD};
        selection-color: #1A1A1A;
    }}
    
    QProgressBar {{
        border: 2px solid {METALLIC_SILVER_DARK};
        border-radius: 5px;
        text-align: center;
        color: {TEXT_PRIMARY};
    }}
    
    QProgressBar::chunk {{
        background: {GOLD_GRADIENT};
        border-radius: 3px;
    }}
    
    QCheckBox {{
        color: {TEXT_PRIMARY};
        spacing: 5px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {METALLIC_SILVER};
        border-radius: 3px;
        background-color: {BG_TERTIARY};
    }}
    
    QCheckBox::indicator:checked {{
        background: {GOLD_GRADIENT};
        border: 2px solid {METALLIC_GOLD};
    }}
    
    QCheckBox::indicator:hover {{
        border: 2px solid {METALLIC_COPPER};
    }}
    
    QLabel {{
        color: {TEXT_PRIMARY};
    }}
    
    QTreeWidget, QListWidget {{
        background-color: {BG_SECONDARY};
        color: {TEXT_PRIMARY};
        border: 2px solid {METALLIC_SILVER_DARK};
        border-radius: 5px;
        alternate-background-color: {BG_TERTIARY};
    }}
    
    QTreeWidget::item:selected, QListWidget::item:selected {{
        background: {GOLD_GRADIENT};
        color: #1A1A1A;
    }}
    
    QTreeWidget::item:hover, QListWidget::item:hover {{
        background: {COPPER_GRADIENT};
    }}
    
    QHeaderView::section {{
        background: {BRONZE_GRADIENT};
        color: #1A1A1A;
        padding: 5px;
        border: 1px solid {METALLIC_BRONZE_DARK};
        font-weight: bold;
    }}
    
    QMenuBar {{
        background-color: {BG_SECONDARY};
        color: {TEXT_PRIMARY};
        border-bottom: 2px solid {METALLIC_COPPER};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 5px 10px;
    }}
    
    QMenuBar::item:selected {{
        background: {COPPER_GRADIENT};
        color: #1A1A1A;
    }}
    
    QMenu {{
        background-color: {BG_SECONDARY};
        color: {TEXT_PRIMARY};
        border: 2px solid {METALLIC_SILVER_DARK};
    }}
    
    QMenu::item:selected {{
        background: {GOLD_GRADIENT};
        color: #1A1A1A;
    }}
    
    QStatusBar {{
        background-color: {BG_SECONDARY};
        color: {TEXT_SECONDARY};
        border-top: 2px solid {METALLIC_SILVER_DARK};
    }}
"""
