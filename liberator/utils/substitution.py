"""
Code substitution utilities - replace proprietary code with open-source alternatives.
"""

import re
from typing import Dict, List, Tuple


class CodeSubstitutor:
    """Substitutes proprietary code with open-source alternatives."""
    
    def __init__(self):
        self.substitution_rules = {
            # Firebase substitutions
            'firebase': {
                'import': {
                    'from': r'from firebase import (\w+)',
                    'to': r'from supabase import \1',
                },
                'initialize': {
                    'from': r'firebase\.initializeApp',
                    'to': 'supabase.create_client',
                }
            },
            # Add more substitution rules as needed
        }
    
    def substitute(self, code: str, substitutions: List[Dict[str, str]]) -> str:
        """Apply substitutions to code."""
        result = code
        
        for sub in substitutions:
            pattern = sub.get('pattern', '')
            replacement = sub.get('replacement', '')
            if pattern and replacement:
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def suggest_substitutions(self, code: str) -> List[Dict[str, str]]:
        """Suggest code substitutions based on detected patterns."""
        suggestions = []
        
        # Check for Firebase
        if re.search(r'firebase', code, re.IGNORECASE):
            suggestions.append({
                'pattern': r'firebase',
                'replacement': 'supabase',
                'description': 'Replace Firebase with Supabase (open-source)',
                'confidence': 'high'
            })
        
        # Check for proprietary APIs
        if re.search(r'stripe\.com', code, re.IGNORECASE):
            suggestions.append({
                'pattern': r'https://api\.stripe\.com',
                'replacement': 'https://api.lemonsqueezy.com',
                'description': 'Consider LemonSqueezy as open-source payment alternative',
                'confidence': 'medium'
            })
        
        return suggestions
