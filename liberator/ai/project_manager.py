"""
AI-powered project management and tracking.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ProjectManager:
    """AI-powered project management and tracking."""
    
    def __init__(self, projects_dir: Optional[Path] = None):
        """
        Initialize project manager.
        
        Args:
            projects_dir: Directory to store project data
        """
        if projects_dir is None:
            projects_dir = Path.home() / ".liberator" / "projects"
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project(self, name: str, source_path: str, output_path: str, 
                      platform: str = "auto") -> Dict[str, Any]:
        """
        Create a new project entry.
        
        Args:
            name: Project name
            source_path: Source project path
            output_path: Output path
            platform: Platform type
        
        Returns:
            Project data
        """
        project_id = self._generate_project_id(name)
        project_data = {
            'id': project_id,
            'name': name,
            'source_path': str(source_path),
            'output_path': str(output_path),
            'platform': platform,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'created',
            'extraction_complete': False,
            'analysis_complete': False,
            'compatibility_tested': False,
            'notes': [],
            'issues': [],
            'fixes_applied': []
        }
        
        self.save_project(project_data)
        return project_data
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        project_file = self.projects_dir / f"{project_id}.json"
        if project_file.exists():
            return json.loads(project_file.read_text())
        return None
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        projects = []
        for project_file in self.projects_dir.glob("*.json"):
            try:
                project_data = json.loads(project_file.read_text())
                projects.append(project_data)
            except:
                continue
        
        # Sort by updated_at
        projects.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        return projects
    
    def save_project(self, project_data: Dict[str, Any]):
        """Save project data."""
        project_data['updated_at'] = datetime.now().isoformat()
        project_file = self.projects_dir / f"{project_data['id']}.json"
        project_file.write_text(json.dumps(project_data, indent=2))
    
    def update_project_status(self, project_id: str, status: str, **kwargs):
        """Update project status."""
        project = self.get_project(project_id)
        if project:
            project['status'] = status
            project.update(kwargs)
            self.save_project(project)
    
    def add_note(self, project_id: str, note: str):
        """Add a note to a project."""
        project = self.get_project(project_id)
        if project:
            if 'notes' not in project:
                project['notes'] = []
            project['notes'].append({
                'text': note,
                'timestamp': datetime.now().isoformat()
            })
            self.save_project(project)
    
    def add_issue(self, project_id: str, issue: str, severity: str = "medium"):
        """Add an issue to a project."""
        project = self.get_project(project_id)
        if project:
            if 'issues' not in project:
                project['issues'] = []
            project['issues'].append({
                'description': issue,
                'severity': severity,
                'timestamp': datetime.now().isoformat(),
                'resolved': False
            })
            self.save_project(project)
    
    def mark_issue_resolved(self, project_id: str, issue_index: int):
        """Mark an issue as resolved."""
        project = self.get_project(project_id)
        if project and 'issues' in project and 0 <= issue_index < len(project['issues']):
            project['issues'][issue_index]['resolved'] = True
            project['issues'][issue_index]['resolved_at'] = datetime.now().isoformat()
            self.save_project(project)
    
    def add_fix(self, project_id: str, fix_description: str, fix_type: str = "manual"):
        """Record a fix that was applied."""
        project = self.get_project(project_id)
        if project:
            if 'fixes_applied' not in project:
                project['fixes_applied'] = []
            project['fixes_applied'].append({
                'description': fix_description,
                'type': fix_type,
                'timestamp': datetime.now().isoformat()
            })
            self.save_project(project)
    
    def delete_project(self, project_id: str):
        """Delete a project."""
        project_file = self.projects_dir / f"{project_id}.json"
        if project_file.exists():
            project_file.unlink()
    
    def get_project_stats(self, project_id: str) -> Dict[str, Any]:
        """Get project statistics."""
        project = self.get_project(project_id)
        if not project:
            return {}
        
        stats = {
            'total_notes': len(project.get('notes', [])),
            'total_issues': len(project.get('issues', [])),
            'resolved_issues': sum(1 for i in project.get('issues', []) if i.get('resolved', False)),
            'total_fixes': len(project.get('fixes_applied', [])),
            'status': project.get('status', 'unknown'),
            'extraction_complete': project.get('extraction_complete', False),
            'analysis_complete': project.get('analysis_complete', False),
            'compatibility_tested': project.get('compatibility_tested', False)
        }
        
        return stats
    
    def _generate_project_id(self, name: str) -> str:
        """Generate a unique project ID."""
        import hashlib
        timestamp = datetime.now().isoformat()
        combined = f"{name}_{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
