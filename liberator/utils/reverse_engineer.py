"""
Reverse engineering utilities for understanding and modifying extracted code.
"""

import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class ReverseEngineer:
    """Reverse engineers code to understand structure and dependencies."""
    
    def __init__(self):
        self.patterns = {
            'api_endpoints': [],
            'database_connections': [],
            'external_services': [],
            'secrets': [],
            'hardcoded_values': []
        }
    
    def analyze_api_calls(self, code: str) -> List[Dict[str, Any]]:
        """Extract API endpoint calls from code."""
        endpoints = []
        
        # Common patterns
        patterns = [
            r'fetch\(["\']([^"\']+)["\']',
            r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']',
            r'\.get\(["\']([^"\']+)["\']',
            r'\.post\(["\']([^"\']+)["\']',
            r'http://[^\s"\']+',
            r'https://[^\s"\']+',
            r'api\.\w+\.com/[^\s"\']+',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                url = match.group(1) if match.lastindex else match.group(0)
                endpoints.append({
                    'url': url,
                    'pattern': pattern,
                    'type': 'api_call'
                })
        
        return endpoints
    
    def analyze_database_connections(self, code: str) -> List[Dict[str, Any]]:
        """Extract database connection strings and queries."""
        connections = []
        
        patterns = [
            r'mongodb://[^\s"\']+',
            r'postgresql://[^\s"\']+',
            r'mysql://[^\s"\']+',
            r'sqlite://[^\s"\']+',
            r'DATABASE_URL\s*=\s*["\']([^"\']+)["\']',
            r'connectionString\s*[:=]\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                conn_str = match.group(1) if match.lastindex else match.group(0)
                # Mask sensitive parts
                masked = self._mask_sensitive(conn_str)
                connections.append({
                    'connection_string': masked,
                    'original': conn_str,
                    'type': 'database'
                })
        
        return connections
    
    def analyze_secrets(self, code: str) -> List[Dict[str, Any]]:
        """Find potential secrets and API keys in code."""
        secrets = []
        
        patterns = [
            r'api[_-]?key\s*[:=]\s*["\']([^"\']+)["\']',
            r'secret\s*[:=]\s*["\']([^"\']+)["\']',
            r'password\s*[:=]\s*["\']([^"\']+)["\']',
            r'token\s*[:=]\s*["\']([^"\']+)["\']',
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key
            r'sk_live_[0-9a-zA-Z]{24,}',  # Stripe
            r'ghp_[0-9a-zA-Z]{36}',  # GitHub Personal Access Token
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                secret = match.group(1) if match.lastindex else match.group(0)
                secrets.append({
                    'type': 'secret',
                    'pattern': pattern,
                    'location': 'code',
                    'masked': self._mask_secret(secret)
                })
        
        return secrets
    
    def analyze_external_services(self, code: str) -> List[str]:
        """Identify external services and APIs used."""
        services = []
        
        service_patterns = {
            'aws': r'aws\.\w+\.com',
            'google': r'googleapis\.com',
            'stripe': r'stripe\.com',
            'twilio': r'twilio\.com',
            'sendgrid': r'sendgrid\.com',
            'firebase': r'firebase\.com',
            'mongodb': r'mongodb\.com',
            'heroku': r'heroku\.com',
        }
        
        for service, pattern in service_patterns.items():
            if re.search(pattern, code, re.IGNORECASE):
                services.append(service)
        
        return list(set(services))
    
    def suggest_substitutions(self, code: str) -> List[Dict[str, Any]]:
        """Suggest open-source alternatives for proprietary services."""
        substitutions = []
        
        proprietary_services = {
            'firebase': {
                'alternatives': ['supabase', 'appwrite', 'pocketbase'],
                'reason': 'Open-source Firebase alternatives'
            },
            'stripe': {
                'alternatives': ['lemonsqueezy', 'paddle'],
                'reason': 'Open-source payment processing'
            },
            'sendgrid': {
                'alternatives': ['sendinblue', 'mailgun', 'postmark'],
                'reason': 'Email service alternatives'
            },
            'mongodb': {
                'alternatives': ['postgresql', 'cockroachdb'],
                'reason': 'Open-source database alternatives'
            }
        }
        
        for service, info in proprietary_services.items():
            if service.lower() in code.lower():
                substitutions.append({
                    'proprietary': service,
                    'alternatives': info['alternatives'],
                    'reason': info['reason']
                })
        
        return substitutions
    
    def _mask_sensitive(self, value: str) -> str:
        """Mask sensitive parts of connection strings."""
        if '@' in value:
            parts = value.split('@')
            if len(parts) == 2:
                return f"***@{parts[1]}"
        return "***"
    
    def _mask_secret(self, secret: str) -> str:
        """Mask a secret value."""
        if len(secret) > 8:
            return secret[:4] + '*' * (len(secret) - 8) + secret[-4:]
        return '*' * len(secret)
