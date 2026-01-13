"""
Executive Producer Widget - Compatibility wizard GUI.
"""

from pathlib import Path
from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QCheckBox, QProgressBar, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QGroupBox, QMessageBox, QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from ..executive_producer.compatibility_wizard import ExecutiveProducer, Platform, CompatibilityIssue
from ..ai.assistant import AIAssistant


class ValidationWorker(QThread):
    """Worker thread for platform validation."""
    
    progress = pyqtSignal(str, int)  # message, percentage
    issue_found = pyqtSignal(object)  # CompatibilityIssue
    finished = pyqtSignal(dict)  # results
    error = pyqtSignal(str)
    
    def __init__(self, producer: ExecutiveProducer, platforms: List[Platform]):
        super().__init__()
        self.producer = producer
        self.platforms = platforms
    
    def run(self):
        """Run validation."""
        try:
            results = {}
            total = len(self.platforms)
            
            for i, platform in enumerate(self.platforms):
                self.progress.emit(f"Validating {platform.value}...", int((i / total) * 100))
                issues = self.producer.validate_platform(platform)
                results[platform] = issues
                
                for issue in issues:
                    self.issue_found.emit(issue)
            
            self.progress.emit("Validation complete!", 100)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class FixWorker(QThread):
    """Worker thread for auto-fixing issues."""
    
    progress = pyqtSignal(str, int)
    fix_applied = pyqtSignal(str, str)  # issue, fix
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, producer: ExecutiveProducer, platform: Platform, use_ai: bool):
        super().__init__()
        self.producer = producer
        self.platform = platform
        self.use_ai = use_ai
    
    def run(self):
        """Run auto-fix."""
        try:
            self.progress.emit(f"Fixing issues for {self.platform.value}...", 0)
            result = self.producer.auto_fix_issues(self.platform, self.use_ai)
            
            for fix in result.get('fixes_applied', []):
                self.fix_applied.emit(fix['issue'], fix.get('fix', 'Applied'))
            
            self.progress.emit("Fixes applied!", 100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ExecutiveProducerWidget(QWidget):
    """Executive Producer compatibility wizard widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.producer: Optional[ExecutiveProducer] = None
        self.ai_assistant: Optional[AIAssistant] = None
        self.current_project_path: Optional[Path] = None
        self.init_ui()
        self.load_ai_assistant()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("🎬 Executive Producer")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        
        subtitle = QLabel("Guarantee your app works on all platforms")
        from .theme import METALLIC_SILVER
        subtitle.setStyleSheet(f"color: {METALLIC_SILVER};")
        header.addWidget(subtitle)
        
        layout.addLayout(header)
        
        # Project selection
        project_group = QGroupBox("Project")
        project_layout = QHBoxLayout()
        self.project_path_label = QLabel("No project selected")
        project_layout.addWidget(self.project_path_label)
        
        select_btn = QPushButton("Select Project")
        select_btn.clicked.connect(self.select_project)
        project_layout.addWidget(select_btn)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # Platform selection
        platforms_group = QGroupBox("Target Platforms")
        platforms_layout = QVBoxLayout()
        
        platforms_row1 = QHBoxLayout()
        self.windows_check = QCheckBox("Windows")
        self.macos_check = QCheckBox("macOS")
        self.linux_check = QCheckBox("Linux")
        platforms_row1.addWidget(self.windows_check)
        platforms_row1.addWidget(self.macos_check)
        platforms_row1.addWidget(self.linux_check)
        platforms_layout.addLayout(platforms_row1)
        
        platforms_row2 = QHBoxLayout()
        self.ios_check = QCheckBox("iOS")
        self.android_check = QCheckBox("Android")
        platforms_row2.addWidget(self.ios_check)
        platforms_row2.addWidget(self.android_check)
        platforms_row2.addStretch()
        platforms_layout.addLayout(platforms_row2)
        
        select_all_btn = QPushButton("Select All")
        from .theme import BUTTON_NEUTRAL
        select_all_btn.setStyleSheet(BUTTON_NEUTRAL)
        select_all_btn.clicked.connect(self.select_all_platforms)
        platforms_layout.addWidget(select_all_btn)
        
        platforms_group.setLayout(platforms_layout)
        layout.addWidget(platforms_group)
        
        # Actions
        actions_layout = QHBoxLayout()
        
        self.validate_btn = QPushButton("🔍 Validate Compatibility")
        from .theme import BUTTON_PRIMARY
        self.validate_btn.setStyleSheet(BUTTON_PRIMARY)
        self.validate_btn.clicked.connect(self.start_validation)
        actions_layout.addWidget(self.validate_btn)
        
        self.auto_fix_btn = QPushButton("🔧 Auto-Fix Issues")
        from .theme import BUTTON_SUCCESS
        self.auto_fix_btn.setStyleSheet(BUTTON_SUCCESS)
        self.auto_fix_btn.clicked.connect(self.start_auto_fix)
        self.auto_fix_btn.setEnabled(False)
        actions_layout.addWidget(self.auto_fix_btn)
        
        self.test_btn = QPushButton("🧪 Test Compilation")
        from .theme import BUTTON_NEUTRAL
        self.test_btn.setStyleSheet(BUTTON_NEUTRAL)
        self.test_btn.clicked.connect(self.test_compilation)
        actions_layout.addWidget(self.test_btn)
        
        layout.addLayout(actions_layout)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Status log
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setMaximumHeight(150)
        self.status_log.setFont(QFont("Monaco", 9))
        layout.addWidget(self.status_log)
        
        # Issues tree
        issues_group = QGroupBox("Compatibility Issues")
        issues_layout = QVBoxLayout()
        
        self.issues_tree = QTreeWidget()
        self.issues_tree.setHeaderLabels(["Platform", "Severity", "File", "Description", "Status"])
        self.issues_tree.setColumnWidth(0, 100)
        self.issues_tree.setColumnWidth(1, 80)
        self.issues_tree.setColumnWidth(2, 200)
        issues_layout.addWidget(self.issues_tree)
        
        issues_group.setLayout(issues_layout)
        layout.addWidget(issues_group)
        
        # AI toggle
        ai_layout = QHBoxLayout()
        self.use_ai_check = QCheckBox("Use AI for automatic fixes")
        self.use_ai_check.setChecked(True)
        ai_layout.addWidget(self.use_ai_check)
        ai_layout.addStretch()
        layout.addLayout(ai_layout)
    
    def load_ai_assistant(self):
        """Load AI assistant."""
        try:
            self.ai_assistant = AIAssistant()
            if not self.ai_assistant.is_available():
                self.use_ai_check.setEnabled(False)
                self.use_ai_check.setChecked(False)
        except:
            self.use_ai_check.setEnabled(False)
            self.use_ai_check.setChecked(False)
    
    def select_project(self):
        """Select project to validate."""
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.current_project_path = Path(path)
            self.project_path_label.setText(str(self.current_project_path))
            self.producer = ExecutiveProducer(self.current_project_path, self.ai_assistant)
            self.status_log.append(f"✅ Project selected: {path}")
    
    def select_all_platforms(self):
        """Select all platforms."""
        self.windows_check.setChecked(True)
        self.macos_check.setChecked(True)
        self.linux_check.setChecked(True)
        self.ios_check.setChecked(True)
        self.android_check.setChecked(True)
    
    def get_selected_platforms(self) -> List[Platform]:
        """Get selected platforms."""
        platforms = []
        if self.windows_check.isChecked():
            platforms.append(Platform.WINDOWS)
        if self.macos_check.isChecked():
            platforms.append(Platform.MACOS)
        if self.linux_check.isChecked():
            platforms.append(Platform.LINUX)
        if self.ios_check.isChecked():
            platforms.append(Platform.IOS)
        if self.android_check.isChecked():
            platforms.append(Platform.ANDROID)
        return platforms
    
    def start_validation(self):
        """Start platform validation."""
        if not self.producer:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return
        
        platforms = self.get_selected_platforms()
        if not platforms:
            QMessageBox.warning(self, "No Platforms", "Please select at least one platform.")
            return
        
        self.issues_tree.clear()
        self.status_log.clear()
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.validate_btn.setEnabled(False)
        
        self.worker = ValidationWorker(self.producer, platforms)
        self.worker.progress.connect(self.update_progress)
        self.worker.issue_found.connect(self.add_issue)
        self.worker.finished.connect(self.validation_finished)
        self.worker.error.connect(self.validation_error)
        self.worker.start()
    
    def update_progress(self, message: str, percentage: int):
        """Update progress."""
        self.status_log.append(message)
        if percentage >= 0:
            self.progress.setRange(0, 100)
            self.progress.setValue(percentage)
    
    def add_issue(self, issue: CompatibilityIssue):
        """Add issue to tree."""
        item = QTreeWidgetItem(self.issues_tree)
        item.setText(0, issue.file_path.split('/')[0] if '/' in issue.file_path else "Unknown")
        item.setText(1, issue.severity.upper())
        item.setText(2, issue.file_path)
        item.setText(3, issue.description)
        item.setText(4, "Fixed" if issue.fixed else "Pending")
        
        # Color by severity
        if issue.severity == "error":
            item.setForeground(1, QColor(200, 0, 0))
        elif issue.severity == "warning":
            item.setForeground(1, QColor(200, 150, 0))
    
    def validation_finished(self, results: dict):
        """Handle validation completion."""
        self.progress.setVisible(False)
        self.validate_btn.setEnabled(True)
        self.auto_fix_btn.setEnabled(True)
        
        total_issues = sum(len(issues) for issues in results.values())
        self.status_log.append(f"\n✅ Validation complete! Found {total_issues} issues.")
        
        if total_issues > 0:
            QMessageBox.information(
                self,
                "Validation Complete",
                f"Found {total_issues} compatibility issues.\n\nClick 'Auto-Fix Issues' to automatically fix them."
            )
    
    def validation_error(self, error: str):
        """Handle validation error."""
        self.progress.setVisible(False)
        self.validate_btn.setEnabled(True)
        self.status_log.append(f"❌ Error: {error}")
        QMessageBox.critical(self, "Validation Error", error)
    
    def start_auto_fix(self):
        """Start auto-fixing issues."""
        if not self.producer:
            return
        
        platforms = self.get_selected_platforms()
        if not platforms:
            QMessageBox.warning(self, "No Platforms", "Please select at least one platform.")
            return
        
        use_ai = self.use_ai_check.isChecked() and self.ai_assistant and self.ai_assistant.is_available()
        
        if not use_ai:
            reply = QMessageBox.question(
                self,
                "AI Not Available",
                "AI assistant is not configured. Manual fixes will be suggested.\n\nContinue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.auto_fix_btn.setEnabled(False)
        self.status_log.append("Starting auto-fix...")
        
        # Fix for first selected platform (can be extended to all)
        platform = platforms[0]
        self.fix_worker = FixWorker(self.producer, platform, use_ai)
        self.fix_worker.progress.connect(self.update_progress)
        self.fix_worker.fix_applied.connect(self.on_fix_applied)
        self.fix_worker.finished.connect(self.fix_finished)
        self.fix_worker.error.connect(self.fix_error)
        self.fix_worker.start()
    
    def on_fix_applied(self, issue: str, fix: str):
        """Handle fix applied."""
        self.status_log.append(f"✅ Fixed: {issue}")
    
    def fix_finished(self, result: dict):
        """Handle fix completion."""
        self.progress.setVisible(False)
        self.auto_fix_btn.setEnabled(True)
        
        fixed = result.get('fixed', 0)
        total = result.get('total_issues', 0)
        self.status_log.append(f"\n✅ Auto-fix complete! Fixed {fixed} of {total} issues.")
        
        # Refresh issues tree
        self.issues_tree.clear()
        if self.producer:
            for platform in self.get_selected_platforms():
                issues = self.producer.validate_platform(platform)
                for issue in issues:
                    self.add_issue(issue)
        
        QMessageBox.information(
            self,
            "Auto-Fix Complete",
            f"Fixed {fixed} of {total} issues.\n\nPlease review the changes and test your application."
        )
    
    def fix_error(self, error: str):
        """Handle fix error."""
        self.progress.setVisible(False)
        self.auto_fix_btn.setEnabled(True)
        self.status_log.append(f"❌ Error: {error}")
        QMessageBox.critical(self, "Fix Error", error)
    
    def test_compilation(self):
        """Test compilation."""
        if not self.producer:
            QMessageBox.warning(self, "No Project", "Please select a project first.")
            return
        
        platform = self.get_selected_platforms()
        if not platform:
            platform = Platform.MACOS  # Default
        else:
            platform = platform[0]
        
        self.status_log.append(f"Testing compilation for {platform.value}...")
        success, message = self.producer.test_compilation(platform)
        
        if success:
            self.status_log.append(f"✅ {message}")
            QMessageBox.information(self, "Compilation Test", f"✅ {message}")
        else:
            self.status_log.append(f"❌ {message}")
            QMessageBox.warning(self, "Compilation Test", f"❌ {message}")
