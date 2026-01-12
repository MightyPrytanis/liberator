"""
Dependency analyzer - detects and normalizes dependencies across platforms.
"""

import re
import json
from typing import Dict, List, Set, Optional
from pathlib import Path


class DependencyAnalyzer:
    """Analyzes and normalizes dependencies from extracted code."""
    
    def __init__(self):
        self.detected_deps: Set[str] = set()
        self.dep_types: Dict[str, str] = {}  # dep -> type (npm, pip, etc.)
    
    def analyze_code(self, code: str, file_path: str) -> List[str]:
        """Analyze code for import statements and dependencies."""
        deps = []
        
        # Python imports
        if file_path.endswith('.py'):
            deps.extend(self._analyze_python_imports(code))
        
        # JavaScript/TypeScript imports
        elif file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            deps.extend(self._analyze_js_imports(code))
        
        # Go imports
        elif file_path.endswith('.go'):
            deps.extend(self._analyze_go_imports(code))
        
        # Rust imports
        elif file_path.endswith('.rs'):
            deps.extend(self._analyze_rust_imports(code))
        
        return deps
    
    def _analyze_python_imports(self, code: str) -> List[str]:
        """Extract Python package names from imports."""
        deps = []
        patterns = [
            r'^import\s+(\w+)',
            r'^from\s+(\w+)',
            r'^import\s+(\w+)\.',
            r'^from\s+(\w+)\.',
        ]
        
        for line in code.split('\n'):
            line = line.strip()
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    dep = match.group(1)
                    # Filter out standard library
                    if not self._is_stdlib_python(dep):
                        deps.append(dep)
                        self.dep_types[dep] = 'pip'
        
        return deps
    
    def _analyze_js_imports(self, code: str) -> List[str]:
        """Extract JavaScript/TypeScript package names from imports."""
        deps = []
        patterns = [
            r"import\s+.*\s+from\s+['\"](\w+)['\"]",
            r"require\(['\"](\w+)['\"]\)",
            r"from\s+['\"](\w+)['\"]",
        ]
        
        for line in code.split('\n'):
            for pattern in patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    if match and not self._is_stdlib_js(match):
                        deps.append(match)
                        self.dep_types[match] = 'npm'
        
        return deps
    
    def _analyze_go_imports(self, code: str) -> List[str]:
        """Extract Go module names from imports."""
        deps = []
        pattern = r'import\s+["\']([^"\']+)["\']'
        
        for line in code.split('\n'):
            matches = re.findall(pattern, line)
            for match in matches:
                if match and not self._is_stdlib_go(match):
                    deps.append(match)
                    self.dep_types[match] = 'go'
        
        return deps
    
    def _analyze_rust_imports(self, code: str) -> List[str]:
        """Extract Rust crate names from imports."""
        deps = []
        patterns = [
            r'use\s+(\w+)::',
            r'extern\s+crate\s+(\w+)',
        ]
        
        for line in code.split('\n'):
            for pattern in patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    if match and not self._is_stdlib_rust(match):
                        deps.append(match)
                        self.dep_types[match] = 'cargo'
        
        return deps
    
    def _is_stdlib_python(self, module: str) -> bool:
        """Check if a Python module is in the standard library."""
        stdlib = {
            'os', 'sys', 'json', 're', 'math', 'datetime', 'collections',
            'itertools', 'functools', 'pathlib', 'typing', 'abc', 'io',
            'urllib', 'http', 'socket', 'threading', 'multiprocessing',
            'subprocess', 'shutil', 'tempfile', 'hashlib', 'base64',
            'random', 'string', 'copy', 'pickle', 'sqlite3', 'csv',
            'xml', 'html', 'email', 'logging', 'unittest', 'doctest'
        }
        return module in stdlib
    
    def _is_stdlib_js(self, module: str) -> bool:
        """Check if a JavaScript module is in the standard library."""
        stdlib = {
            'fs', 'path', 'http', 'https', 'url', 'util', 'events',
            'stream', 'crypto', 'os', 'child_process', 'cluster',
            'net', 'dgram', 'dns', 'readline', 'repl', 'vm', 'zlib'
        }
        return module in stdlib
    
    def _is_stdlib_go(self, module: str) -> bool:
        """Check if a Go module is in the standard library."""
        return module.startswith('golang.org') or not '.' in module
    
    def _is_stdlib_rust(self, crate: str) -> bool:
        """Check if a Rust crate is in the standard library."""
        stdlib = {
            'std', 'core', 'alloc', 'collections', 'io', 'net', 'os',
            'path', 'process', 'sync', 'thread', 'time', 'fmt', 'str'
        }
        return crate in stdlib
    
    def normalize_dependencies(self, dependencies: List[str]) -> Dict[str, List[str]]:
        """Normalize dependencies by type."""
        normalized = {
            'npm': [],
            'pip': [],
            'go': [],
            'cargo': [],
            'other': []
        }
        
        for dep in dependencies:
            dep_type = self.dep_types.get(dep, 'other')
            if dep_type in normalized:
                if dep not in normalized[dep_type]:
                    normalized[dep_type].append(dep)
            else:
                normalized['other'].append(dep)
        
        return normalized
