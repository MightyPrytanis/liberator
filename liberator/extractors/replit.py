"""
Replit platform extractor.
Extracts apps from Replit's proprietary format.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from ..core.extractor import BaseExtractor, ExtractionResult


class ReplitExtractor(BaseExtractor):
    """Extractor for Replit platform."""
    
    def detect(self) -> bool:
        """Detect Replit project structure."""
        # Replit-specific markers
        markers = [
            '.replit',
            'replit.nix',
            '.config/replit',
            'replit.json'
        ]
        
        for marker in markers:
            if (self.source_path / marker).exists():
                return True
        
        return False
    
    def extract(self) -> ExtractionResult:
        """Extract Replit project."""
        result = ExtractionResult()
        
        # Read Replit configuration
        replit_config = None
        config_file = self.source_path / '.replit'
        if config_file.exists():
            try:
                replit_config = json.loads(self.read_file(config_file))
                result.config['replit'] = replit_config
            except:
                pass
        
        # Read replit.nix if present
        replit_nix = self.source_path / 'replit.nix'
        if replit_nix.exists():
            result.config['replit_nix'] = self.read_file(replit_nix)
        
        # Extract all source files
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file():
                # Skip Replit-specific config but preserve in metadata
                if any(marker in str(file_path) for marker in ['.replit', 'replit.nix', '.config/replit']):
                    continue
                
                relative_path = file_path.relative_to(self.source_path)
                content = self.read_file(file_path)
                if content is not None:
                    result.add_file(str(relative_path), content)
        
        # Extract dependencies from various package managers
        # Python - requirements.txt
        requirements = self.source_path / 'requirements.txt'
        if requirements.exists():
            content = self.read_file(requirements)
            if content:
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        result.add_dependency(line)
        
        # Python - pyproject.toml
        pyproject = self.source_path / 'pyproject.toml'
        if pyproject.exists():
            content = self.read_file(pyproject)
            if content and '[project]' in content:
                # Simple extraction
                for line in content.split('\n'):
                    if '=' in line and ('dependencies' in line.lower() or 'requires' in line.lower()):
                        result.add_dependency(line.strip())
        
        # Node.js - package.json
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
        
        # Go - go.mod
        go_mod = self.source_path / 'go.mod'
        if go_mod.exists():
            content = self.read_file(go_mod)
            if content:
                for line in content.split('\n'):
                    if line.strip().startswith('require'):
                        import re
                        matches = re.findall(r'(\S+)\s+v[\d.]+', line)
                        result.dependencies.extend(matches)
        
        # Rust - Cargo.toml
        cargo_toml = self.source_path / 'Cargo.toml'
        if cargo_toml.exists():
            content = self.read_file(cargo_toml)
            if content:
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
        
        # Extract environment variables
        env_file = self.source_path / '.env'
        if env_file.exists():
            result.config['env'] = self.read_file(env_file)
        
        # Extract run command from Replit config
        if replit_config:
            run_cmd = replit_config.get('run', '')
            if run_cmd:
                result.config['run_command'] = run_cmd
        
        result.metadata = {
            'platform': 'replit',
            'source_path': str(self.source_path),
            'replit_config': replit_config
        }
        
        return result
