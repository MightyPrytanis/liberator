"""
AI Assistant for code repair, refactoring, and help.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


class AIAssistant:
    """AI-powered assistant for Liberator."""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize AI assistant.
        
        Args:
            provider: AI provider ("openai" or "anthropic")
        """
        self.provider = provider
        self.api_key = self._load_api_key(provider)
        self.client = self._initialize_client()
    
    def _load_api_key(self, provider: str) -> Optional[str]:
        """Load API key from configuration."""
        config_file = Path.home() / ".liberator" / "ai_config.json"
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text())
                return config.get(f"{provider}_key")
            except:
                pass
        
        # Try environment variable
        env_key = f"{provider.upper()}_API_KEY"
        return os.environ.get(env_key)
    
    def _initialize_client(self):
        """Initialize AI client."""
        if not self.api_key:
            return None
        
        if self.provider == "openai":
            try:
                from openai import OpenAI
                return OpenAI(api_key=self.api_key)
            except ImportError:
                return None
        elif self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                return Anthropic(api_key=self.api_key)
            except ImportError:
                return None
        
        return None
    
    def is_available(self) -> bool:
        """Check if AI assistant is available."""
        return self.client is not None
    
    def ask(self, question: str, context: Optional[str] = None) -> str:
        """
        Ask a question to the AI assistant.
        
        Args:
            question: The question to ask
            context: Optional context (code, error message, etc.)
        
        Returns:
            AI response
        """
        if not self.is_available():
            return "AI assistant is not configured. Please set up your API key in settings."
        
        try:
            if self.provider == "openai":
                return self._ask_openai(question, context)
            elif self.provider == "anthropic":
                return self._ask_anthropic(question, context)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _ask_openai(self, question: str, context: Optional[str] = None) -> str:
        """Ask OpenAI."""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant for Liberator, a tool that extracts apps from proprietary platforms. Help users with code repair, refactoring, troubleshooting, and general questions."
            }
        ]
        
        if context:
            messages.append({
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            })
        else:
            messages.append({
                "role": "user",
                "content": question
            })
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def _ask_anthropic(self, question: str, context: Optional[str] = None) -> str:
        """Ask Anthropic."""
        system_prompt = "You are a helpful assistant for Liberator, a tool that extracts apps from proprietary platforms. Help users with code repair, refactoring, troubleshooting, and general questions."
        
        user_message = question
        if context:
            user_message = f"Context:\n{context}\n\nQuestion: {question}"
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return response.content[0].text
    
    def repair_code(self, code: str, error_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Repair code using AI.
        
        Args:
            code: The code to repair
            error_message: Optional error message
        
        Returns:
            Dict with 'fixed_code' and 'explanation'
        """
        prompt = f"""Please repair the following code. Make it functional and follow best practices.

Code:
```python
{code}
```

{f"Error message: {error_message}" if error_message else ""}

Please provide:
1. The fixed code
2. A brief explanation of what was wrong and how you fixed it

Format your response as:
FIXED_CODE:
```python
[fixed code here]
```

EXPLANATION:
[explanation here]
"""
        
        response = self.ask(prompt, code)
        
        # Parse response
        fixed_code = self._extract_code_block(response)
        explanation = self._extract_explanation(response)
        
        return {
            'fixed_code': fixed_code or code,
            'explanation': explanation or "Code repair attempted. Please review the changes.",
            'original_code': code
        }
    
    def refactor_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Refactor code using AI.
        
        Args:
            code: The code to refactor
            language: Programming language
        
        Returns:
            Dict with 'refactored_code' and 'explanation'
        """
        prompt = f"""Please refactor the following {language} code to improve:
- Readability
- Performance
- Maintainability
- Best practices

Code:
```{language}
{code}
```

Please provide:
1. The refactored code
2. A brief explanation of the improvements

Format your response as:
REFACTORED_CODE:
```{language}
[refactored code here]
```

EXPLANATION:
[explanation here]
"""
        
        response = self.ask(prompt, code)
        
        refactored_code = self._extract_code_block(response)
        explanation = self._extract_explanation(response)
        
        return {
            'refactored_code': refactored_code or code,
            'explanation': explanation or "Code refactoring attempted. Please review the changes.",
            'original_code': code
        }
    
    def troubleshoot(self, error_message: str, code_context: Optional[str] = None) -> str:
        """
        Troubleshoot an error.
        
        Args:
            error_message: The error message
            code_context: Optional code context
        
        Returns:
            Troubleshooting advice
        """
        prompt = f"""I'm encountering this error:

{error_message}

{f"Here's the relevant code:\n```\n{code_context}\n```" if code_context else ""}

Please help me troubleshoot this issue. Provide:
1. What the error means
2. Common causes
3. How to fix it
4. Prevention tips
"""
        
        return self.ask(prompt, code_context)
    
    def suggest_compatibility_fixes(self, code: str, target_platform: str) -> Dict[str, Any]:
        """
        Suggest compatibility fixes for a target platform.
        
        Args:
            code: The code to fix
            target_platform: Target platform (windows, macos, linux, ios, android)
        
        Returns:
            Dict with 'fixed_code' and 'changes'
        """
        prompt = f"""This code needs to work on {target_platform}. Please suggest compatibility fixes.

Code:
```python
{code}
```

Please provide:
1. Platform-specific fixes
2. The updated code
3. Explanation of changes

Format your response as:
FIXED_CODE:
```python
[fixed code here]
```

CHANGES:
[list of changes here]
"""
        
        response = self.ask(prompt, code)
        
        fixed_code = self._extract_code_block(response)
        changes = self._extract_explanation(response)
        
        return {
            'fixed_code': fixed_code or code,
            'changes': changes or "Compatibility fixes suggested. Please review.",
            'target_platform': target_platform
        }
    
    def _extract_code_block(self, text: str) -> Optional[str]:
        """Extract code block from AI response."""
        # Look for code blocks
        pattern = r'```(?:python|javascript|typescript|java|go|rust)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        # Look for FIXED_CODE or REFACTORED_CODE sections
        pattern = r'(?:FIXED_CODE|REFACTORED_CODE):\s*```.*?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        return None
    
    def _extract_explanation(self, text: str) -> Optional[str]:
        """Extract explanation from AI response."""
        # Look for EXPLANATION or CHANGES sections
        pattern = r'(?:EXPLANATION|CHANGES):\s*(.*?)(?:\n\n|\Z)'
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        
        return None
