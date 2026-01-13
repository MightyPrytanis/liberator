"""
Projects Management Widget - Track and manage liberated projects.
"""

from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QTextEdit, QGroupBox, QMessageBox,
    QSplitter, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..ai.project_manager import ProjectManager


class ProjectsWidget(QWidget):
    """Projects management widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_manager = ProjectManager()
        self.current_project_id: Optional[str] = None
        self.init_ui()
        self.refresh_projects()
    
    def init_ui(self):
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("📁 Projects")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        from .theme import BUTTON_NEUTRAL
        refresh_btn.setStyleSheet(BUTTON_NEUTRAL)
        refresh_btn.clicked.connect(self.refresh_projects)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # Splitter for project list and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Project list
        list_group = QGroupBox("Your Projects")
        list_layout = QVBoxLayout()
        
        self.projects_list = QListWidget()
        self.projects_list.itemClicked.connect(self.on_project_selected)
        list_layout.addWidget(self.projects_list)
        
        list_group.setLayout(list_layout)
        splitter.addWidget(list_group)
        
        # Project details
        details_group = QGroupBox("Project Details")
        details_layout = QVBoxLayout()
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Monaco", 10))
        details_layout.addWidget(self.details_text)
        
        # Actions
        actions_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete Project")
        from .theme import BUTTON_SECONDARY
        delete_btn.setStyleSheet(BUTTON_SECONDARY)
        delete_btn.clicked.connect(self.delete_project)
        actions_layout.addWidget(delete_btn)
        
        actions_layout.addStretch()
        details_layout.addLayout(actions_layout)
        
        details_group.setLayout(details_layout)
        splitter.addWidget(details_group)
        
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
    
    def refresh_projects(self):
        """Refresh projects list."""
        self.projects_list.clear()
        projects = self.project_manager.list_projects()
        
        for project in projects:
            item = QListWidgetItem(project.get('name', 'Unnamed Project'))
            item.setData(Qt.ItemDataRole.UserRole, project.get('id'))
            status = project.get('status', 'unknown')
            item.setText(f"{project.get('name', 'Unnamed')} ({status})")
            self.projects_list.addItem(item)
    
    def on_project_selected(self, item: QListWidgetItem):
        """Handle project selection."""
        project_id = item.data(Qt.ItemDataRole.UserRole)
        if not project_id:
            return
        
        self.current_project_id = project_id
        project = self.project_manager.get_project(project_id)
        
        if project:
            stats = self.project_manager.get_project_stats(project_id)
            
            details = f"""Project: {project.get('name', 'Unknown')}
ID: {project_id}
Status: {project.get('status', 'unknown')}

Source: {project.get('source_path', 'N/A')}
Output: {project.get('output_path', 'N/A')}
Platform: {project.get('platform', 'auto')}

Created: {project.get('created_at', 'N/A')}
Updated: {project.get('updated_at', 'N/A')}

Statistics:
- Total Notes: {stats.get('total_notes', 0)}
- Total Issues: {stats.get('total_issues', 0)}
- Resolved Issues: {stats.get('resolved_issues', 0)}
- Fixes Applied: {stats.get('total_fixes', 0)}

Extraction: {'✅' if stats.get('extraction_complete') else '❌'}
Analysis: {'✅' if stats.get('analysis_complete') else '❌'}
Compatibility Tested: {'✅' if stats.get('compatibility_tested') else '❌'}

"""
            
            # Add notes
            notes = project.get('notes', [])
            if notes:
                details += "\nNotes:\n"
                for note in notes[-5:]:  # Last 5 notes
                    details += f"- {note.get('text', '')}\n"
            
            # Add issues
            issues = project.get('issues', [])
            if issues:
                details += "\nIssues:\n"
                for issue in issues:
                    resolved = "✅" if issue.get('resolved') else "❌"
                    details += f"{resolved} [{issue.get('severity', 'unknown')}] {issue.get('description', '')}\n"
            
            self.details_text.setText(details)
    
    def delete_project(self):
        """Delete selected project."""
        if not self.current_project_id:
            QMessageBox.warning(self, "No Project", "Please select a project to delete.")
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Project",
            "Are you sure you want to delete this project?\n\nThis will only delete the project tracking data, not the actual files.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.project_manager.delete_project(self.current_project_id)
            self.current_project_id = None
            self.details_text.clear()
            self.refresh_projects()
            QMessageBox.information(self, "Deleted", "Project deleted successfully.")
