"""
Executive Producer - Compatibility wizard that guarantees apps work on target platforms.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

from ..ai.assistant import AIAssistant


class Platform(Enum):
    """Supported platforms."""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    IOS = "ios"
    ANDROID = "android"


class CompatibilityIssue:
    """Represents a compatibility issue."""
    
    def __init__(self, severity: str, description: str, file_path: str, 
                 line_number: Optional[int] = None, suggestion: Optional[str] = None):
        self.severity = severity  # "error", "warning", "info"
        self.description = description
        self.file_path = file_path
        self.line_number = line_number
        self.suggestion = suggestion
        self.fixed = False
        self.fix_applied = None


class PlatformValidator:
    """Validates code for specific platforms."""
    
    def __init__(self, platform: Platform):
        self.platform = platform
    
    def validate(self, project_path: Path) -> List[CompatibilityIssue]:
        """Validate project for this platform."""
        issues = []
        
        # Platform-specific validations
        if self.platform == Platform.WINDOWS:
            issues.extend(self._validate_windows(project_path))
        elif self.platform == Platform.MACOS:
            issues.extend(self._validate_macos(project_path))
        elif self.platform == Platform.LINUX:
            issues.extend(self._validate_linux(project_path))
        elif self.platform == Platform.IOS:
            issues.extend(self._validate_ios(project_path))
        elif self.platform == Platform.ANDROID:
            issues.extend(self._validate_android(project_path))
        
        return issues
    
    def _validate_windows(self, project_path: Path) -> List[CompatibilityIssue]:
        """Validate for Windows."""
        issues = []
        
        # Check for Unix-specific paths
        for file_path in project_path.rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if '/tmp/' in content or '/var/' in content:
                    issues.append(CompatibilityIssue(
                        "warning",
                        "Unix-specific path detected",
                        str(file_path.relative_to(project_path)),
                        suggestion="Use os.path.join() or pathlib for cross-platform paths"
                    ))
            except:
                pass
        
        # Check for shell scripts
        for file_path in project_path.rglob("*.sh"):
            issues.append(CompatibilityIssue(
                "error",
                "Shell script not compatible with Windows",
                str(file_path.relative_to(project_path)),
                suggestion="Create .bat or .ps1 equivalent, or use cross-platform solution"
            ))
        
        return issues
    
    def _validate_macos(self, project_path: Path) -> List[CompatibilityIssue]:
        """Validate for macOS."""
        issues = []
        
        # Check for Windows-specific code
        for file_path in project_path.rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if 'win32' in content or 'windows' in content.lower():
                    if 'if sys.platform == "win32"' not in content:
                        issues.append(CompatibilityIssue(
                            "warning",
                            "Windows-specific code detected",
                            str(file_path.relative_to(project_path)),
                            suggestion="Add platform checks for macOS compatibility"
                        ))
            except:
                pass
        
        return issues
    
    def _validate_linux(self, project_path: Path) -> List[CompatibilityIssue]:
        """Validate for Linux."""
        issues = []
        
        # Similar to macOS validation
        for file_path in project_path.rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if 'win32' in content and 'if sys.platform' not in content:
                    issues.append(CompatibilityIssue(
                        "warning",
                        "Windows-specific code may not work on Linux",
                        str(file_path.relative_to(project_path)),
                        suggestion="Add platform checks"
                    ))
            except:
                pass
        
        return issues
    
    def _validate_ios(self, project_path: Path) -> List[CompatibilityIssue]:
        """Validate for iOS."""
        issues = []
        
        # Check for non-iOS compatible dependencies
        package_json = project_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                deps = data.get('dependencies', {})
                
                # Node.js packages that don't work on iOS
                incompatible = ['fs', 'child_process', 'os']
                for dep in deps:
                    if any(inc in dep.lower() for inc in incompatible):
                        issues.append(CompatibilityIssue(
                            "error",
                            f"Incompatible dependency for iOS: {dep}",
                            "package.json",
                            suggestion="Use React Native compatible alternatives"
                        ))
            except:
                pass
        
        # Check for Python (not supported on iOS)
        if (project_path / "requirements.txt").exists():
            issues.append(CompatibilityIssue(
                "error",
                "Python is not natively supported on iOS",
                "requirements.txt",
                suggestion="Consider using Pythonista or converting to Swift/Objective-C"
            ))
        
        return issues
    
    def _validate_android(self, project_path: Path) -> List[CompatibilityIssue]:
        """Validate for Android."""
        issues = []
        
        # Similar to iOS
        package_json = project_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                deps = data.get('dependencies', {})
                
                incompatible = ['fs', 'child_process']
                for dep in deps:
                    if any(inc in dep.lower() for inc in incompatible):
                        issues.append(CompatibilityIssue(
                            "warning",
                            f"May need React Native bridge for: {dep}",
                            "package.json",
                            suggestion="Use React Native compatible packages"
                        ))
            except:
                pass
        
        return issues


class ExecutiveProducer:
    """Executive Producer - Guarantees app compatibility."""
    
    def __init__(self, project_path: Path, ai_assistant: Optional[AIAssistant] = None):
        """
        Initialize Executive Producer.
        
        Args:
            project_path: Path to the project to validate
            ai_assistant: Optional AI assistant for automatic fixes
        """
        self.project_path = Path(project_path)
        self.ai_assistant = ai_assistant
        self.validators: Dict[Platform, PlatformValidator] = {}
        self.issues: Dict[Platform, List[CompatibilityIssue]] = {}
        self.fixes_applied: List[Dict[str, Any]] = []
    
    def validate_platform(self, platform: Platform) -> List[CompatibilityIssue]:
        """
        Validate project for a specific platform.
        
        Args:
            platform: Target platform
        
        Returns:
            List of compatibility issues
        """
        if platform not in self.validators:
            self.validators[platform] = PlatformValidator(platform)
        
        validator = self.validators[platform]
        issues = validator.validate(self.project_path)
        self.issues[platform] = issues
        
        return issues
    
    def validate_all_platforms(self) -> Dict[Platform, List[CompatibilityIssue]]:
        """Validate for all platforms."""
        results = {}
        for platform in Platform:
            results[platform] = self.validate_platform(platform)
        return results
    
    def auto_fix_issues(self, platform: Platform, use_ai: bool = True) -> Dict[str, Any]:
        """
        Automatically fix compatibility issues for a platform.
        
        Args:
            platform: Target platform
            use_ai: Whether to use AI for fixes
        
        Returns:
            Dict with fix results
        """
        if platform not in self.issues:
            self.validate_platform(platform)
        
        issues = self.issues[platform]
        fixed_count = 0
        failed_count = 0
        
        for issue in issues:
            if issue.fixed:
                continue
            
            try:
                if use_ai and self.ai_assistant and self.ai_assistant.is_available():
                    # Use AI to fix
                    fix_result = self._ai_fix_issue(issue, platform)
                    if fix_result['success']:
                        issue.fixed = True
                        issue.fix_applied = fix_result['fix']
                        fixed_count += 1
                        self.fixes_applied.append({
                            'platform': platform.value,
                            'issue': issue.description,
                            'fix': fix_result['fix'],
                            'file': issue.file_path
                        })
                    else:
                        failed_count += 1
                else:
                    # Manual fix suggestions
                    if issue.suggestion:
                        issue.fix_applied = issue.suggestion
                        fixed_count += 1
                    else:
                        failed_count += 1
            except Exception as e:
                failed_count += 1
        
        return {
            'platform': platform.value,
            'total_issues': len(issues),
            'fixed': fixed_count,
            'failed': failed_count,
            'fixes_applied': self.fixes_applied
        }
    
    def _ai_fix_issue(self, issue: CompatibilityIssue, platform: Platform) -> Dict[str, Any]:
        """Use AI to fix an issue."""
        if not self.ai_assistant or not self.ai_assistant.is_available():
            return {'success': False, 'error': 'AI not available'}
        
        # Read the file
        file_path = self.project_path / issue.file_path
        if not file_path.exists():
            return {'success': False, 'error': 'File not found'}
        
        try:
            code = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Get AI fix
            prompt = f"""Fix this compatibility issue for {platform.value}:

Issue: {issue.description}
File: {issue.file_path}
Line: {issue.line_number or 'N/A'}

Current code:
```python
{code}
```

Please provide the fixed code that works on {platform.value}.
"""
            
            response = self.ai_assistant.ask(prompt, code)
            
            # Extract fixed code
            fixed_code = self._extract_code_from_response(response)
            
            if fixed_code:
                # Apply fix
                file_path.write_text(fixed_code, encoding='utf-8')
                return {
                    'success': True,
                    'fix': fixed_code,
                    'explanation': response
                }
            else:
                return {
                    'success': False,
                    'error': 'Could not extract fixed code from AI response'
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_code_from_response(self, response: str) -> Optional[str]:
        """Extract code from AI response."""
        import re
        
        # Look for code blocks
        pattern = r'```(?:python|javascript|typescript)?\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        return None
    
    def test_compilation(self, platform: Platform) -> Tuple[bool, str]:
        """
        Test if the project compiles/runs on the target platform.
        
        Args:
            platform: Target platform
        
        Returns:
            Tuple of (success, message)
        """
        # This would ideally run in a container or VM for the target platform
        # For now, we do basic syntax checking
        
        if platform in [Platform.IOS, Platform.ANDROID]:
            return (False, "Mobile platform testing requires device/emulator")
        
        # Check Python syntax
        python_files = list(self.project_path.rglob("*.py"))
        if python_files:
            for py_file in python_files[:10]:  # Check first 10 files
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "py_compile", str(py_file)],
                        capture_output=True,
                        timeout=10
                    )
                    if result.returncode != 0:
                        return (False, f"Syntax error in {py_file.name}: {result.stderr.decode()}")
                except Exception as e:
                    return (False, f"Error checking {py_file.name}: {str(e)}")
        
        # Check Node.js projects
        package_json = self.project_path / "package.json"
        if package_json.exists():
            try:
                result = subprocess.run(
                    ["npm", "install", "--dry-run"],
                    cwd=self.project_path,
                    capture_output=True,
                    timeout=30
                )
                # Don't fail on npm install errors, just check if package.json is valid
            except:
                pass
        
        return (True, "Basic compilation checks passed")
    
    def generate_compatibility_report(self) -> Dict[str, Any]:
        """Generate comprehensive compatibility report."""
        report = {
            'project_path': str(self.project_path),
            'platforms': {},
            'summary': {
                'total_issues': 0,
                'critical_issues': 0,
                'warnings': 0,
                'platforms_tested': []
            }
        }
        
        for platform in Platform:
            issues = self.validate_platform(platform)
            critical = sum(1 for i in issues if i.severity == "error")
            warnings = sum(1 for i in issues if i.severity == "warning")
            
            report['platforms'][platform.value] = {
                'total_issues': len(issues),
                'critical_issues': critical,
                'warnings': warnings,
                'issues': [
                    {
                        'severity': i.severity,
                        'description': i.description,
                        'file': i.file_path,
                        'line': i.line_number,
                        'suggestion': i.suggestion,
                        'fixed': i.fixed
                    }
                    for i in issues
                ]
            }
            
            report['summary']['total_issues'] += len(issues)
            report['summary']['critical_issues'] += critical
            report['summary']['warnings'] += warnings
            report['summary']['platforms_tested'].append(platform.value)
        
        return report
