"""
Base44 platform extractor.
Extracts apps from Base44's proprietary format.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from ..core.extractor import BaseExtractor, ExtractionResult


class Base44Extractor(BaseExtractor):
    """Extractor for Base44 platform."""
    
    def detect(self) -> bool:
        """Detect Base44 project structure."""
        # Look for Base44-specific markers
        markers = [
            '.base44',
            'base44.json',
            'base44.config',
            '.base44config'
        ]
        
        for marker in markers:
            if (self.source_path / marker).exists():
                return True
        
        # Check for Base44 in package.json or other config files
        package_json = self.source_path / 'package.json'
        if package_json.exists():
            try:
                content = package_json.read_text()
                if 'base44' in content.lower():
                    return True
            except:
                pass
        
        return False
    
    def extract(self) -> ExtractionResult:
        """Extract Base44 project."""
        result = ExtractionResult()
        
        # Read Base44 configuration
        config_files = [
            self.source_path / '.base44',
            self.source_path / 'base44.json',
            self.source_path / 'base44.config',
            self.source_path / '.base44config'
        ]
        
        base44_config = None
        for config_file in config_files:
            if config_file.exists():
                try:
                    base44_config = json.loads(self.read_file(config_file))
                    result.config['base44'] = base44_config
                    break
                except:
                    pass
        
        # Extract all source files
        # Base44 typically stores code in standard directories
        source_dirs = ['src', 'app', 'lib', 'components', 'pages', 'public']
        
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file():
                # Skip Base44-specific files but keep their content in metadata
                if any(marker in str(file_path) for marker in ['.base44', 'base44.json']):
                    continue
                
                relative_path = file_path.relative_to(self.source_path)
                content = self.read_file(file_path)
                if content is not None:
                    result.add_file(str(relative_path), content)
        
        # Extract dependencies from package.json
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
        
        # Extract environment variables if present
        env_file = self.source_path / '.env'
        if env_file.exists():
            result.config['env'] = self.read_file(env_file)
        
        result.metadata = {
            'platform': 'base44',
            'source_path': str(self.source_path),
            'base44_config': base44_config
        }
        
        return result
