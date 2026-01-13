"""
AI Assistant Widget - Chat interface for AI-powered help.
"""

import os
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLineEdit, QLabel, QComboBox, QSplitter, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QColor

from ..ai.assistant import AIAssistant
from ..ai.project_manager import ProjectManager


class AIWorker(QThread):
    """Worker thread for AI operations."""
    
    response_ready = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, assistant: AIAssistant, question: str, context: Optional[str] = None):
        super().__init__()
        self.assistant = assistant
        self.question = question
        self.context = context
    
    def run(self):
        """Run AI query."""
        try:
            response = self.assistant.ask(self.question, self.context)
            self.response_ready.emit(response)
        except Exception as e:
            self.error.emit(str(e))


class AIAssistantWidget(QWidget):
    """AI Assistant chat widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.assistant: Optional[AIAssistant] = None
        self.project_manager = ProjectManager()
        self.current_project_id: Optional[str] = None
        self.init_ui()
        self.load_assistant()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("🤖 AI Assistant")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        
        # Provider selection
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "Anthropic"])
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        header.addWidget(QLabel("Provider:"))
        header.addWidget(self.provider_combo)
        
        layout.addLayout(header)
        
        # Status
        self.status_label = QLabel("Not configured")
        from .theme import METALLIC_SILVER
        self.status_label.setStyleSheet(f"color: {METALLIC_SILVER};")
        layout.addWidget(self.status_label)
        
        # Chat area
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setFont(QFont("Monaco", 10))
        splitter.addWidget(self.chat_history)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QVBoxLayout()
        
        repair_btn = QPushButton("🔧 Repair Code")
        from .theme import BUTTON_SECONDARY
        repair_btn.setStyleSheet(BUTTON_SECONDARY)
        repair_btn.clicked.connect(self.show_repair_dialog)
        actions_layout.addWidget(repair_btn)
        
        refactor_btn = QPushButton("♻️ Refactor Code")
        refactor_btn.setStyleSheet(BUTTON_SECONDARY)
        refactor_btn.clicked.connect(self.show_refactor_dialog)
        actions_layout.addWidget(refactor_btn)
        
        troubleshoot_btn = QPushButton("🔍 Troubleshoot Error")
        troubleshoot_btn.setStyleSheet(BUTTON_SECONDARY)
        troubleshoot_btn.clicked.connect(self.show_troubleshoot_dialog)
        actions_layout.addWidget(troubleshoot_btn)
        
        actions_group.setLayout(actions_layout)
        splitter.addWidget(actions_group)
        
        splitter.setSizes([400, 150])
        layout.addWidget(splitter)
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a question or request help...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        from .theme import BUTTON_NEUTRAL
        self.send_btn.setStyleSheet(BUTTON_NEUTRAL)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        
        # Add welcome message
        self.add_message("assistant", "Hello! I'm your AI assistant. I can help with:\n- Code repair and refactoring\n- Troubleshooting\n- Compatibility guidance\n- General questions about Liberator\n\nHow can I help you today?")
    
    def load_assistant(self):
        """Load AI assistant."""
        provider = self.provider_combo.currentText().lower()
        self.assistant = AIAssistant(provider=provider)
        
        if self.assistant.is_available():
            self.status_label.setText("✅ Connected")
            from .theme import METALLIC_GOLD
            self.status_label.setStyleSheet(f"color: {METALLIC_GOLD};")
        else:
            self.status_label.setText("⚠️ Not configured - Set API key in Settings")
            from .theme import METALLIC_COPPER
            self.status_label.setStyleSheet(f"color: {METALLIC_COPPER};")
    
    def on_provider_changed(self):
        """Handle provider change."""
        self.load_assistant()
    
    def send_message(self):
        """Send a message to the AI."""
        message = self.input_field.text().strip()
        if not message:
            return
        
        if not self.assistant or not self.assistant.is_available():
            QMessageBox.warning(
                self,
                "AI Not Available",
                "Please configure your AI API key in Settings first."
            )
            return
        
        # Add user message to chat
        self.add_message("user", message)
        self.input_field.clear()
        self.send_btn.setEnabled(False)
        
        # Get context if available
        context = None
        if self.current_project_id:
            project = self.project_manager.get_project(self.current_project_id)
            if project:
                context = f"Project: {project.get('name', 'Unknown')}\nPlatform: {project.get('platform', 'auto')}"
        
        # Query AI
        self.worker = AIWorker(self.assistant, message, context)
        self.worker.response_ready.connect(self.on_ai_response)
        self.worker.error.connect(self.on_ai_error)
        self.worker.start()
    
    def on_ai_response(self, response: str):
        """Handle AI response."""
        self.add_message("assistant", response)
        self.send_btn.setEnabled(True)
    
    def on_ai_error(self, error: str):
        """Handle AI error."""
        self.add_message("assistant", f"Error: {error}")
        self.send_btn.setEnabled(True)
    
    def add_message(self, role: str, content: str):
        """Add a message to the chat."""
        if role == "user":
            prefix = "You: "
            color = QColor(0, 100, 200)
        else:
            prefix = "Assistant: "
            color = QColor(50, 150, 50)
        
        self.chat_history.append(f"<b style='color: {color.name()};'>{prefix}</b>")
        self.chat_history.append(content)
        self.chat_history.append("")  # Blank line
    
    def show_repair_dialog(self):
        """Show code repair dialog."""
        from PyQt6.QtWidgets import QDialog, QTextEdit, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Repair Code")
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Paste the code to repair:"))
        code_input = QTextEdit()
        code_input.setFont(QFont("Monaco", 10))
        layout.addWidget(code_input)
        
        layout.addWidget(QLabel("Error message (optional):"))
        error_input = QLineEdit()
        layout.addWidget(error_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec():
            code = code_input.toPlainText()
            error = error_input.text()
            
            if code and self.assistant and self.assistant.is_available():
                self.add_message("user", f"Repair this code:\n```\n{code}\n```")
                result = self.assistant.repair_code(code, error)
                self.add_message("assistant", f"Fixed code:\n```\n{result['fixed_code']}\n```\n\n{result['explanation']}")
    
    def show_refactor_dialog(self):
        """Show refactor dialog."""
        from PyQt6.QtWidgets import QDialog, QTextEdit, QDialogButtonBox, QComboBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Refactor Code")
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Language:"))
        lang_combo = QComboBox()
        lang_combo.addItems(["python", "javascript", "typescript", "java", "go", "rust"])
        layout.addWidget(lang_combo)
        
        layout.addWidget(QLabel("Paste the code to refactor:"))
        code_input = QTextEdit()
        code_input.setFont(QFont("Monaco", 10))
        layout.addWidget(code_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec():
            code = code_input.toPlainText()
            language = lang_combo.currentText()
            
            if code and self.assistant and self.assistant.is_available():
                self.add_message("user", f"Refactor this {language} code:\n```\n{code}\n```")
                result = self.assistant.refactor_code(code, language)
                self.add_message("assistant", f"Refactored code:\n```\n{result['refactored_code']}\n```\n\n{result['explanation']}")
    
    def show_troubleshoot_dialog(self):
        """Show troubleshoot dialog."""
        from PyQt6.QtWidgets import QDialog, QTextEdit, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Troubleshoot Error")
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Error message:"))
        error_input = QTextEdit()
        error_input.setFont(QFont("Monaco", 10))
        layout.addWidget(error_input)
        
        layout.addWidget(QLabel("Code context (optional):"))
        code_input = QTextEdit()
        code_input.setFont(QFont("Monaco", 10))
        layout.addWidget(code_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec():
            error = error_input.toPlainText()
            code = code_input.toPlainText()
            
            if error and self.assistant and self.assistant.is_available():
                self.add_message("user", f"Troubleshoot this error:\n{error}")
                response = self.assistant.troubleshoot(error, code)
                self.add_message("assistant", response)
    
    def set_project_context(self, project_id: Optional[str]):
        """Set current project context."""
        self.current_project_id = project_id
