"""
Base extractor class and utilities for platform-specific extraction.
"""

import os
import json
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


class ExtractionResult:
    """Result of an extraction operation."""
    
    def __init__(self):
        self.files: Dict[str, str] = {}  # path -> content
        self.dependencies: List[str] = []
        self.config: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def add_file(self, path: str, content: str):
        """Add a file to the extraction result."""
        self.files[path] = content
    
    def add_dependency(self, dep: str):
        """Add a dependency."""
        if dep not in self.dependencies:
            self.dependencies.append(dep)
    
    def add_error(self, error: str):
        """Add an error message."""
        self.errors.append(error)
    
    def add_warning(self, warning: str):
        """Add a warning message."""
        self.warnings.append(warning)


class BaseExtractor(ABC):
    """Base class for platform-specific extractors."""
    
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        if not self.source_path.exists():
            raise ValueError(f"Source path does not exist: {source_path}")
    
    @abstractmethod
    def detect(self) -> bool:
        """Detect if this extractor can handle the source."""
        pass
    
    @abstractmethod
    def extract(self) -> ExtractionResult:
        """Extract all files and metadata from the source."""
        pass
    
    def read_file(self, path: Path) -> Optional[str]:
        """Safely read a file."""
        try:
            if path.exists() and path.is_file():
                return path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return None
        return None
    
    def find_files(self, pattern: str, recursive: bool = True) -> List[Path]:
        """Find files matching a pattern."""
        matches = []
        if recursive:
            matches = list(self.source_path.rglob(pattern))
        else:
            matches = list(self.source_path.glob(pattern))
        return [m for m in matches if m.is_file()]


class GenericExtractor(BaseExtractor):
    """Generic extractor for unknown or custom platforms."""
    
    def detect(self) -> bool:
        """Always returns True as a fallback."""
        return True
    
    def extract(self) -> ExtractionResult:
        """Extract all files from the source directory."""
        result = ExtractionResult()
        
        # Extract all files
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.source_path)
                content = self.read_file(file_path)
                if content is not None:
                    result.add_file(str(relative_path), content)
        
        # Try to detect dependencies from common files
        self._detect_dependencies(result)
        
        result.metadata = {
            'platform': 'generic',
            'source_path': str(self.source_path)
        }
        
        return result
    
    def _detect_dependencies(self, result: ExtractionResult):
        """Detect dependencies from common configuration files."""
        # Check for package.json
        package_json = self.source_path / 'package.json'
        if package_json.exists():
            try:
                data = json.loads(self.read_file(package_json))
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                for dep, version in {**deps, **dev_deps}.items():
                    result.add_dependency(f"{dep}@{version}")
            except:
                pass
        
        # Check for requirements.txt
        requirements = self.source_path / 'requirements.txt'
        if requirements.exists():
            content = self.read_file(requirements)
            if content:
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        result.add_dependency(line)
        
        # Check for Pipfile
        pipfile = self.source_path / 'Pipfile'
        if pipfile.exists():
            try:
                content = self.read_file(pipfile)
                # Simple regex to extract package names
                for match in re.finditer(r'^(\w+)\s*=', content, re.MULTILINE):
                    result.add_dependency(match.group(1))
            except:
                pass
        
        # Check for go.mod
        go_mod = self.source_path / 'go.mod'
        if go_mod.exists():
            content = self.read_file(go_mod)
            if content:
                for line in content.split('\n'):
                    if line.strip().startswith('require'):
                        # Extract module names
                        matches = re.findall(r'(\S+)\s+v[\d.]+', line)
                        result.dependencies.extend(matches)
        
        # Check for Cargo.toml
        cargo_toml = self.source_path / 'Cargo.toml'
        if cargo_toml.exists():
            content = self.read_file(cargo_toml)
            if content:
                # Simple extraction of dependencies
                in_deps = False
                for line in content.split('\n'):
                    if line.strip().startswith('[dependencies]'):
                        in_deps = True
                        continue
                    if line.strip().startswith('['):
                        in_deps = False
                        continue
                    if in_deps and '=' in line:
                        dep = line.split('=')[0].strip()
                        if dep:
                            result.add_dependency(f"{dep} (Rust)")
