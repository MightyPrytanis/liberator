"""
GitHub Integration Widget - Push to GitHub interface.
"""

from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QGroupBox, QRadioButton, QButtonGroup,
    QMessageBox, QCheckBox, QComboBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from ..integrations.github import GitHubIntegration


class GitHubPushWorker(QThread):
    """Worker thread for GitHub operations."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)  # success, message
    error = pyqtSignal(str)
    
    def __init__(self, github: GitHubIntegration, operation: str, **kwargs):
        super().__init__()
        self.github = github
        self.operation = operation
        self.kwargs = kwargs
    
    def run(self):
        """Run GitHub operation."""
        try:
            if self.operation == 'create_repo':
                self.progress.emit("Creating repository...")
                success, result = self.github.create_repository(
                    self.kwargs['name'],
                    self.kwargs.get('description', ''),
                    self.kwargs.get('private', False),
                    self.kwargs.get('organization')
                )
                self.finished.emit(success, result)
            
            elif self.operation == 'push':
                self.progress.emit("Initializing git repository...")
                self.progress.emit("Adding files...")
                self.progress.emit("Committing changes...")
                self.progress.emit("Pushing to GitHub...")
                success, result = self.github.push_to_repository(
                    self.kwargs['local_path'],
                    self.kwargs['repo_url'],
                    self.kwargs.get('branch', 'main'),
                    self.kwargs.get('commit_message', 'Initial commit: Liberated project')
                )
                self.finished.emit(success, result)
            
            elif self.operation == 'check_repo':
                self.progress.emit("Checking repository...")
                exists, accessible = self.github.check_repository_exists(self.kwargs['repo_url'])
                if exists and accessible:
                    self.finished.emit(True, "Repository exists and is accessible")
                else:
                    self.finished.emit(False, "Repository not found or not accessible")
        
        except Exception as e:
            self.error.emit(str(e))


class GitHubIntegrationWidget(QWidget):
    """GitHub integration widget for pushing to GitHub."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.github: Optional[GitHubIntegration] = None
        self.project_path: Optional[Path] = None
        self.init_ui()
        self.load_github()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("🐙 GitHub Integration")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Project path
        project_group = QGroupBox("Project to Push")
        project_layout = QHBoxLayout()
        self.project_path_label = QLabel("No project selected")
        project_layout.addWidget(self.project_path_label)
        
        select_btn = QPushButton("Select Project")
        from .theme import BUTTON_NEUTRAL
        select_btn.setStyleSheet(BUTTON_NEUTRAL)
        select_btn.clicked.connect(self.select_project)
        project_layout.addWidget(select_btn)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # Repository options
        repo_group = QGroupBox("Repository Options")
        repo_layout = QVBoxLayout()
        
        self.repo_option_group = QButtonGroup()
        
        create_radio = QRadioButton("Create new repository")
        create_radio.setChecked(True)
        self.repo_option_group.addButton(create_radio, 0)
        repo_layout.addWidget(create_radio)
        
        existing_radio = QRadioButton("Use existing repository")
        self.repo_option_group.addButton(existing_radio, 1)
        repo_layout.addWidget(existing_radio)
        
        repo_group.setLayout(repo_layout)
        layout.addWidget(repo_group)
        
        # New repository options
        new_repo_group = QGroupBox("New Repository")
        new_repo_layout = QVBoxLayout()
        
        new_repo_layout.addWidget(QLabel("Repository Name:"))
        self.repo_name_edit = QLineEdit()
        self.repo_name_edit.setPlaceholderText("my-liberated-app")
        new_repo_layout.addWidget(self.repo_name_edit)
        
        new_repo_layout.addWidget(QLabel("Description (optional):"))
        self.repo_desc_edit = QLineEdit()
        self.repo_desc_edit.setPlaceholderText("Liberated from proprietary platform")
        new_repo_layout.addWidget(self.repo_desc_edit)
        
        self.private_check = QCheckBox("Private repository")
        new_repo_layout.addWidget(self.private_check)
        
        new_repo_group.setLayout(new_repo_layout)
        layout.addWidget(new_repo_group)
        self.new_repo_group = new_repo_group
        
        # Existing repository options
        existing_repo_group = QGroupBox("Existing Repository")
        existing_repo_layout = QVBoxLayout()
        
        existing_repo_layout.addWidget(QLabel("Repository URL:"))
        self.repo_url_edit = QLineEdit()
        self.repo_url_edit.setPlaceholderText("https://github.com/username/repo")
        existing_repo_layout.addWidget(self.repo_url_edit)
        
        check_btn = QPushButton("Check Repository")
        check_btn.setStyleSheet(BUTTON_NEUTRAL)
        check_btn.clicked.connect(self.check_repository)
        existing_repo_layout.addWidget(check_btn)
        
        existing_repo_group.setLayout(existing_repo_layout)
        layout.addWidget(existing_repo_group)
        self.existing_repo_group = existing_repo_group
        
        # Update visibility based on selection
        create_radio.toggled.connect(lambda checked: self.new_repo_group.setVisible(checked))
        existing_radio.toggled.connect(lambda checked: self.existing_repo_group.setVisible(checked))
        self.new_repo_group.setVisible(True)
        self.existing_repo_group.setVisible(False)
        
        # Branch and commit message
        commit_group = QGroupBox("Commit Options")
        commit_layout = QVBoxLayout()
        
        commit_layout.addWidget(QLabel("Branch:"))
        self.branch_combo = QComboBox()
        self.branch_combo.addItems(["main", "master", "develop"])
        self.branch_combo.setEditable(True)
        commit_layout.addWidget(self.branch_combo)
        
        commit_layout.addWidget(QLabel("Commit Message:"))
        self.commit_message_edit = QLineEdit()
        self.commit_message_edit.setText("Initial commit: Liberated project")
        commit_layout.addWidget(self.commit_message_edit)
        
        commit_group.setLayout(commit_layout)
        layout.addWidget(commit_group)
        
        # Push button
        self.push_btn = QPushButton("🚀 Push to GitHub")
        self.push_btn.setMinimumHeight(50)
        from .theme import BUTTON_PRIMARY
        self.push_btn.setStyleSheet(BUTTON_PRIMARY + "font-size: 16px;")
        self.push_btn.clicked.connect(self.push_to_github)
        layout.addWidget(self.push_btn)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Status log
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setMaximumHeight(200)
        self.status_log.setFont(QFont("Monaco", 9))
        layout.addWidget(self.status_log)
        
        # Status label
        self.status_label = QLabel("Ready to push to GitHub")
        from .theme import METALLIC_SILVER
        self.status_label.setStyleSheet(f"color: {METALLIC_SILVER};")
        layout.addWidget(self.status_label)
    
    def load_github(self):
        """Load GitHub integration."""
        try:
            self.github = GitHubIntegration()
            if not self.github.gh_available and not self.github.token:
                self.status_label.setText("⚠️ GitHub CLI or token not configured")
                from .theme import METALLIC_COPPER
                self.status_label.setStyleSheet(f"color: {METALLIC_COPPER};")
            else:
                self.status_label.setText("✅ GitHub integration ready")
                from .theme import METALLIC_GOLD
                self.status_label.setStyleSheet(f"color: {METALLIC_GOLD};")
        except Exception as e:
            self.status_label.setText(f"❌ Error: {e}")
    
    def select_project(self):
        """Select project to push."""
        from PyQt6.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path = Path(path)
            self.project_path_label.setText(str(self.project_path))
            self.status_log.append(f"✅ Project selected: {path}")
    
    def check_repository(self):
        """Check if repository exists."""
        repo_url = self.repo_url_edit.text().strip()
        if not repo_url:
            QMessageBox.warning(self, "Error", "Please enter a repository URL.")
            return
        
        if not self.github:
            QMessageBox.warning(self, "Error", "GitHub integration not available.")
            return
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.status_log.append(f"Checking repository: {repo_url}...")
        
        self.worker = GitHubPushWorker(self.github, 'check_repo', repo_url=repo_url)
        self.worker.progress.connect(lambda msg: self.status_log.append(msg))
        self.worker.finished.connect(self.check_repo_finished)
        self.worker.error.connect(self.operation_error)
        self.worker.start()
    
    def check_repo_finished(self, success: bool, message: str):
        """Handle repository check completion."""
        self.progress.setVisible(False)
        if success:
            self.status_log.append(f"✅ {message}")
            QMessageBox.information(self, "Repository Found", message)
        else:
            self.status_log.append(f"❌ {message}")
            QMessageBox.warning(self, "Repository Not Found", message)
    
    def push_to_github(self):
        """Push project to GitHub."""
        if not self.project_path or not self.project_path.exists():
            QMessageBox.warning(self, "Error", "Please select a project directory.")
            return
        
        if not self.github:
            QMessageBox.warning(self, "Error", "GitHub integration not available.")
            return
        
        self.status_log.clear()
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.push_btn.setEnabled(False)
        
        # Determine which option is selected
        if self.repo_option_group.checkedId() == 0:
            # Create new repository
            repo_name = self.repo_name_edit.text().strip()
            if not repo_name:
                QMessageBox.warning(self, "Error", "Please enter a repository name.")
                self.progress.setVisible(False)
                self.push_btn.setEnabled(True)
                return
            
            self.status_log.append("Creating new repository...")
            self.worker = GitHubPushWorker(
                self.github,
                'create_repo',
                name=repo_name,
                description=self.repo_desc_edit.text().strip(),
                private=self.private_check.isChecked()
            )
            self.worker.progress.connect(lambda msg: self.status_log.append(msg))
            self.worker.finished.connect(self.repo_created)
            self.worker.error.connect(self.operation_error)
            self.worker.start()
        
        else:
            # Use existing repository
            repo_url = self.repo_url_edit.text().strip()
            if not repo_url:
                QMessageBox.warning(self, "Error", "Please enter a repository URL.")
                self.progress.setVisible(False)
                self.push_btn.setEnabled(True)
                return
            
            self.push_to_existing_repo(repo_url)
    
    def repo_created(self, success: bool, repo_url: str):
        """Handle repository creation."""
        if success:
            self.status_log.append(f"✅ Repository created: {repo_url}")
            # Now push to the new repository
            self.push_to_existing_repo(repo_url)
        else:
            self.progress.setVisible(False)
            self.push_btn.setEnabled(True)
            self.status_log.append(f"❌ Failed to create repository: {repo_url}")
            QMessageBox.critical(self, "Error", f"Failed to create repository:\n{repo_url}")
    
    def push_to_existing_repo(self, repo_url: str):
        """Push to existing repository."""
        self.status_log.append(f"Pushing to {repo_url}...")
        
        self.worker = GitHubPushWorker(
            self.github,
            'push',
            local_path=self.project_path,
            repo_url=repo_url,
            branch=self.branch_combo.currentText(),
            commit_message=self.commit_message_edit.text()
        )
        self.worker.progress.connect(lambda msg: self.status_log.append(msg))
        self.worker.finished.connect(self.push_finished)
        self.worker.error.connect(self.operation_error)
        self.worker.start()
    
    def push_finished(self, success: bool, message: str):
        """Handle push completion."""
        self.progress.setVisible(False)
        self.push_btn.setEnabled(True)
        
        if success:
            self.status_log.append(f"✅ {message}")
            self.status_label.setText("✅ Successfully pushed to GitHub")
            from .theme import METALLIC_GOLD
            self.status_label.setStyleSheet(f"color: {METALLIC_GOLD};")
            
            QMessageBox.information(
                self,
                "Success",
                f"{message}\n\nYour project is now on GitHub!"
            )
        else:
            self.status_log.append(f"❌ {message}")
            self.status_label.setText("❌ Push failed")
            from .theme import METALLIC_COPPER
            self.status_label.setStyleSheet(f"color: {METALLIC_COPPER};")
            
            QMessageBox.critical(self, "Error", f"Failed to push to GitHub:\n{message}")
    
    def operation_error(self, error: str):
        """Handle operation error."""
        self.progress.setVisible(False)
        self.push_btn.setEnabled(True)
        self.status_log.append(f"❌ Error: {error}")
        QMessageBox.critical(self, "Error", error)
