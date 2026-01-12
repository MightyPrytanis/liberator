"""
Utility functions for Liberator.
"""

import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


def safe_json_load(file_path: Path) -> Optional[Dict[str, Any]]:
    """Safely load JSON file."""
    try:
        if file_path.exists():
            return json.loads(file_path.read_text(encoding='utf-8'))
    except Exception:
        pass
    return None


def safe_yaml_load(file_path: Path) -> Optional[Dict[str, Any]]:
    """Safely load YAML file."""
    try:
        if file_path.exists():
            # Try to use yaml if available, otherwise return None
            try:
                import yaml
                return yaml.safe_load(file_path.read_text(encoding='utf-8'))
            except ImportError:
                return None
    except Exception:
        pass
    return None


def detect_project_type(source_path: Path) -> str:
    """Detect project type from files."""
    # Check for package.json
    if (source_path / 'package.json').exists():
        return 'nodejs'
    
    # Check for requirements.txt or setup.py
    if (source_path / 'requirements.txt').exists() or (source_path / 'setup.py').exists():
        return 'python'
    
    # Check for go.mod
    if (source_path / 'go.mod').exists():
        return 'go'
    
    # Check for Cargo.toml
    if (source_path / 'Cargo.toml').exists():
        return 'rust'
    
    # Check for pom.xml
    if (source_path / 'pom.xml').exists():
        return 'java'
    
    return 'unknown'
