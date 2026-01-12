"""
Code analyzer - reverse engineers code structure and patterns.
"""

import re
import ast
from typing import Dict, List, Optional, Any
from pathlib import Path


class CodeAnalyzer:
    """Analyzes code to understand structure, patterns, and dependencies."""
    
    def __init__(self):
        self.analysis_results: Dict[str, Any] = {}
    
    def analyze_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze a single file."""
        result = {
            'file_path': file_path,
            'language': self._detect_language(file_path),
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': [],
            'dependencies': [],
            'patterns': []
        }
        
        if file_path.endswith('.py'):
            result.update(self._analyze_python(content))
        elif file_path.endswith(('.js', '.jsx')):
            result.update(self._analyze_javascript(content))
        elif file_path.endswith(('.ts', '.tsx')):
            result.update(self._analyze_typescript(content))
        elif file_path.endswith('.go'):
            result.update(self._analyze_go(content))
        elif file_path.endswith('.rs'):
            result.update(self._analyze_rust(content))
        
        return result
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin'
        }
        
        ext = Path(file_path).suffix
        return ext_map.get(ext, 'unknown')
    
    def _analyze_python(self, content: str) -> Dict[str, Any]:
        """Analyze Python code."""
        result = {
            'imports': [],
            'functions': [],
            'classes': []
        }
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result['imports'].append(node.module)
                elif isinstance(node, ast.FunctionDef):
                    result['functions'].append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'line': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    result['classes'].append({
                        'name': node.name,
                        'bases': [self._get_name(base) for base in node.bases],
                        'line': node.lineno
                    })
        except:
            # Fallback to regex if AST parsing fails
            result['imports'] = re.findall(r'^(?:import|from)\s+(\S+)', content, re.MULTILINE)
            result['functions'] = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
            result['classes'] = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        
        return result
    
    def _analyze_javascript(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript code."""
        result = {
            'imports': [],
            'exports': [],
            'functions': [],
            'classes': []
        }
        
        # Extract imports
        import_pattern = r"(?:import|require)\(?['\"]([^'\"]+)['\"]\)?"
        result['imports'] = re.findall(import_pattern, content)
        
        # Extract exports
        export_pattern = r"export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)"
        result['exports'] = re.findall(export_pattern, content)
        
        # Extract functions
        func_pattern = r"(?:function|const|let|var)\s+(\w+)\s*=\s*(?:\(|function)"
        result['functions'] = re.findall(func_pattern, content)
        
        # Extract classes
        class_pattern = r"class\s+(\w+)"
        result['classes'] = re.findall(class_pattern, content)
        
        return result
    
    def _analyze_typescript(self, content: str) -> Dict[str, Any]:
        """Analyze TypeScript code (similar to JavaScript)."""
        return self._analyze_javascript(content)
    
    def _analyze_go(self, content: str) -> Dict[str, Any]:
        """Analyze Go code."""
        result = {
            'imports': [],
            'functions': [],
            'types': []
        }
        
        # Extract imports
        import_pattern = r'import\s+["\']([^"\']+)["\']'
        result['imports'] = re.findall(import_pattern, content)
        
        # Extract functions
        func_pattern = r'func\s+(\w+)'
        result['functions'] = re.findall(func_pattern, content)
        
        # Extract types
        type_pattern = r'type\s+(\w+)'
        result['types'] = re.findall(type_pattern, content)
        
        return result
    
    def _analyze_rust(self, content: str) -> Dict[str, Any]:
        """Analyze Rust code."""
        result = {
            'imports': [],
            'functions': [],
            'structs': [],
            'traits': []
        }
        
        # Extract use statements
        use_pattern = r'use\s+([^;]+);'
        result['imports'] = re.findall(use_pattern, content)
        
        # Extract functions
        func_pattern = r'fn\s+(\w+)'
        result['functions'] = re.findall(func_pattern, content)
        
        # Extract structs
        struct_pattern = r'struct\s+(\w+)'
        result['structs'] = re.findall(struct_pattern, content)
        
        # Extract traits
        trait_pattern = r'trait\s+(\w+)'
        result['traits'] = re.findall(trait_pattern, content)
        
        return result
    
    def _get_name(self, node) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
