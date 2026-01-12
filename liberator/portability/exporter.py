"""
Portability exporter - creates portable, open-source project structures.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..core.extractor import ExtractionResult
from ..analyzer.dependency_analyzer import DependencyAnalyzer
from ..analyzer.code_analyzer import CodeAnalyzer


class PortableExporter:
    """Exports extracted projects to portable, open-source formats."""
    
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.dependency_analyzer = DependencyAnalyzer()
        self.code_analyzer = CodeAnalyzer()
    
    def export(self, extraction_result: ExtractionResult) -> Dict[str, Any]:
        """Export extraction result to portable format."""
        # Analyze all code files
        all_deps = set(extraction_result.dependencies)
        
        for file_path, content in extraction_result.files.items():
            # Analyze code for additional dependencies
            code_deps = self.dependency_analyzer.analyze_code(content, file_path)
            all_deps.update(code_deps)
            
            # Write file to output
            output_file = self.output_path / file_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(content, encoding='utf-8')
        
        # Normalize dependencies
        normalized_deps = self.dependency_analyzer.normalize_dependencies(list(all_deps))
        
        # Generate configuration files
        self._generate_config_files(normalized_deps, extraction_result)
        
        # Generate Docker files
        self._generate_docker_files(extraction_result)
        
        # Generate environment template
        self._generate_env_template(extraction_result)
        
        # Generate README
        self._generate_readme(extraction_result, normalized_deps)
        
        # Generate .gitignore
        self._generate_gitignore()
        
        # Generate LICENSE
        self._generate_license()
        
        return {
            'output_path': str(self.output_path),
            'files_exported': len(extraction_result.files),
            'dependencies': normalized_deps,
            'status': 'success'
        }
    
    def _generate_config_files(self, dependencies: Dict[str, List[str]], extraction_result: ExtractionResult):
        """Generate standard configuration files."""
        # Generate package.json for Node.js projects
        if dependencies.get('npm'):
            package_json = {
                'name': self._get_project_name(),
                'version': '1.0.0',
                'description': 'Liberated from proprietary platform',
                'main': 'index.js',
                'scripts': {
                    'start': 'node index.js',
                    'dev': 'node index.js'
                },
                'dependencies': {},
                'devDependencies': {}
            }
            
            # Add dependencies
            for dep in dependencies['npm']:
                if '@' in dep:
                    name, version = dep.split('@', 1)
                    package_json['dependencies'][name] = version
                else:
                    package_json['dependencies'][dep] = '*'
            
            (self.output_path / 'package.json').write_text(
                json.dumps(package_json, indent=2)
            )
        
        # Generate requirements.txt for Python projects
        if dependencies.get('pip'):
            requirements = '\n'.join(dependencies['pip'])
            (self.output_path / 'requirements.txt').write_text(requirements)
        
        # Generate go.mod for Go projects
        if dependencies.get('go'):
            go_mod = f"module {self._get_project_name()}\n\ngo 1.21\n\n"
            for dep in dependencies['go']:
                go_mod += f"require {dep} v0.0.0\n"
            (self.output_path / 'go.mod').write_text(go_mod)
        
        # Generate Cargo.toml for Rust projects
        if dependencies.get('cargo'):
            cargo_toml = f"""[package]
name = "{self._get_project_name()}"
version = "1.0.0"
edition = "2021"

[dependencies]
"""
            for dep in dependencies['cargo']:
                cargo_toml += f'{dep} = "*"\n'
            (self.output_path / 'Cargo.toml').write_text(cargo_toml)
    
    def _generate_docker_files(self, extraction_result: ExtractionResult):
        """Generate Dockerfile and docker-compose.yml."""
        # Detect primary language
        languages = self._detect_languages(extraction_result)
        
        if 'python' in languages:
            dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
"""
            (self.output_path / 'Dockerfile').write_text(dockerfile)
        
        elif 'javascript' in languages or 'typescript' in languages:
            dockerfile = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]
"""
            (self.output_path / 'Dockerfile').write_text(dockerfile)
        
        elif 'go' in languages:
            dockerfile = """FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o app .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/app .

CMD ["./app"]
"""
            (self.output_path / 'Dockerfile').write_text(dockerfile)
        
        # Generate docker-compose.yml
        docker_compose = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - .:/app
"""
        (self.output_path / 'docker-compose.yml').write_text(docker_compose)
    
    def _generate_env_template(self, extraction_result: ExtractionResult):
        """Generate .env.example template."""
        env_content = extraction_result.config.get('env', '')
        
        if env_content:
            # Create template by removing values
            template_lines = []
            for line in env_content.split('\n'):
                if '=' in line:
                    key = line.split('=')[0].strip()
                    template_lines.append(f"{key}=your_value_here")
                else:
                    template_lines.append(line)
            
            (self.output_path / '.env.example').write_text('\n'.join(template_lines))
        else:
            (self.output_path / '.env.example').write_text("# Add your environment variables here\n")
    
    def _generate_readme(self, extraction_result: ExtractionResult, dependencies: Dict[str, List[str]]):
        """Generate comprehensive README.md."""
        platform = extraction_result.metadata.get('platform', 'unknown')
        
        readme = f"""# {self._get_project_name()}

## Liberated from {platform}

This project was liberated from a proprietary platform and made fully portable and open-source.

## Project Structure

```
{self._get_project_structure()}
```

## Dependencies

"""
        
        if dependencies.get('npm'):
            readme += "### Node.js\n"
            for dep in dependencies['npm']:
                readme += f"- {dep}\n"
            readme += "\n"
        
        if dependencies.get('pip'):
            readme += "### Python\n"
            for dep in dependencies['pip']:
                readme += f"- {dep}\n"
            readme += "\n"
        
        if dependencies.get('go'):
            readme += "### Go\n"
            for dep in dependencies['go']:
                readme += f"- {dep}\n"
            readme += "\n"
        
        readme += """## Installation

### Using Docker

```bash
docker-compose up
```

### Manual Installation

See the appropriate installation instructions for your language above.

## Configuration

Copy `.env.example` to `.env` and fill in your configuration values.

## License

This project is now open-source and free to use, modify, and distribute.

## Original Platform Metadata

"""
        
        if extraction_result.metadata:
            readme += f"```json\n{json.dumps(extraction_result.metadata, indent=2)}\n```\n"
        
        (self.output_path / 'README.md').write_text(readme)
    
    def _generate_gitignore(self):
        """Generate .gitignore file."""
        gitignore = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Build outputs
dist/
build/
*.egg-info/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Docker
.dockerignore
"""
        (self.output_path / '.gitignore').write_text(gitignore)
    
    def _generate_license(self):
        """Generate MIT License."""
        license_text = """MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        (self.output_path / 'LICENSE').write_text(license_text)
    
    def _get_project_name(self) -> str:
        """Get project name from output path."""
        return self.output_path.name or 'liberated-app'
    
    def _detect_languages(self, extraction_result: ExtractionResult) -> List[str]:
        """Detect programming languages from files."""
        languages = set()
        for file_path in extraction_result.files.keys():
            ext = Path(file_path).suffix
            lang_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.jsx': 'javascript',
                '.ts': 'typescript',
                '.tsx': 'typescript',
                '.go': 'go',
                '.rs': 'rust',
                '.java': 'java',
                '.cpp': 'cpp',
                '.c': 'c'
            }
            if ext in lang_map:
                languages.add(lang_map[ext])
        return list(languages)
    
    def _get_project_structure(self) -> str:
        """Generate project structure tree."""
        structure = []
        for root, dirs, files in os.walk(self.output_path):
            level = root.replace(str(self.output_path), '').count(os.sep)
            indent = ' ' * 2 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # Limit to first 10 files per directory
                structure.append(f"{subindent}{file}")
        return '\n'.join(structure)
