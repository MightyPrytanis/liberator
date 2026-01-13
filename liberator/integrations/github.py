"""
GitHub integration for pushing liberated projects to GitHub.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import tempfile


class GitHubIntegration:
    """GitHub integration for Liberator."""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub integration.
        
        Args:
            token: GitHub personal access token (optional, can use gh CLI)
        """
        self.token = token or self._get_token_from_env()
        self.gh_available = self._check_gh_cli()
    
    def _get_token_from_env(self) -> Optional[str]:
        """Get GitHub token from environment."""
        return os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    
    def _check_gh_cli(self) -> bool:
        """Check if GitHub CLI is available."""
        try:
            result = subprocess.run(
                ['gh', '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def create_repository(self, name: str, description: str = "", 
                         private: bool = False, organization: Optional[str] = None) -> Tuple[bool, str]:
        """
        Create a new GitHub repository.
        
        Args:
            name: Repository name
            description: Repository description
            private: Whether repository is private
            organization: Organization name (optional)
        
        Returns:
            Tuple of (success, repo_url or error_message)
        """
        if self.gh_available:
            return self._create_repo_with_gh(name, description, private, organization)
        elif self.token:
            return self._create_repo_with_api(name, description, private, organization)
        else:
            return (False, "GitHub CLI or token required. Install 'gh' CLI or set GITHUB_TOKEN environment variable.")
    
    def _create_repo_with_gh(self, name: str, description: str, 
                             private: bool, organization: Optional[str]) -> Tuple[bool, str]:
        """Create repository using GitHub CLI."""
        try:
            cmd = ['gh', 'repo', 'create', name]
            
            if description:
                cmd.extend(['--description', description])
            
            if private:
                cmd.append('--private')
            else:
                cmd.append('--public')
            
            if organization:
                cmd.extend(['--org', organization])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Extract URL from output
                output = result.stdout.strip()
                if 'github.com' in output:
                    repo_url = output.split()[0] if output.split() else f"https://github.com/{organization or 'user'}/{name}"
                else:
                    repo_url = f"https://github.com/{organization or self._get_username()}/{name}"
                return (True, repo_url)
            else:
                return (False, f"Failed to create repository: {result.stderr}")
        except Exception as e:
            return (False, f"Error creating repository: {str(e)}")
    
    def _create_repo_with_api(self, name: str, description: str, 
                              private: bool, organization: Optional[str]) -> Tuple[bool, str]:
        """Create repository using GitHub API."""
        import urllib.request
        import urllib.parse
        
        try:
            url = "https://api.github.com/user/repos"
            if organization:
                url = f"https://api.github.com/orgs/{organization}/repos"
            
            data = {
                "name": name,
                "description": description,
                "private": private
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Authorization': f'token {self.token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                repo_url = result.get('html_url', '')
                return (True, repo_url)
        except Exception as e:
            return (False, f"Error creating repository via API: {str(e)}")
    
    def _get_username(self) -> str:
        """Get GitHub username."""
        if self.gh_available:
            try:
                result = subprocess.run(
                    ['gh', 'api', 'user', '--jq', '.login'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
        return "user"
    
    def push_to_repository(self, local_path: Path, repo_url: str, 
                          branch: str = "main", commit_message: str = "Initial commit: Liberated project") -> Tuple[bool, str]:
        """
        Push local project to GitHub repository.
        
        Args:
            local_path: Path to local project
            repo_url: GitHub repository URL
            branch: Branch name (default: main)
            commit_message: Commit message
        
        Returns:
            Tuple of (success, message)
        """
        local_path = Path(local_path)
        if not local_path.exists():
            return (False, f"Local path does not exist: {local_path}")
        
        try:
            # Initialize git if not already
            if not (local_path / '.git').exists():
                subprocess.run(
                    ['git', 'init'],
                    cwd=local_path,
                    check=True,
                    timeout=10
                )
            
            # Add remote if not exists
            try:
                subprocess.run(
                    ['git', 'remote', 'get-url', 'origin'],
                    cwd=local_path,
                    check=True,
                    capture_output=True,
                    timeout=5
                )
                # Remote exists, update it
                subprocess.run(
                    ['git', 'remote', 'set-url', 'origin', repo_url],
                    cwd=local_path,
                    check=True,
                    timeout=5
                )
            except:
                # Remote doesn't exist, add it
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', repo_url],
                    cwd=local_path,
                    check=True,
                    timeout=5
                )
            
            # Add all files
            subprocess.run(
                ['git', 'add', '.'],
                cwd=local_path,
                check=True,
                timeout=30
            )
            
            # Check if there are changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=local_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if not result.stdout.strip():
                return (True, "No changes to commit (repository already up to date)")
            
            # Commit
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=local_path,
                check=True,
                timeout=30,
                env={**os.environ, 'GIT_AUTHOR_NAME': 'Liberator', 'GIT_AUTHOR_EMAIL': 'liberator@example.com'}
            )
            
            # Set branch
            subprocess.run(
                ['git', 'branch', '-M', branch],
                cwd=local_path,
                check=True,
                timeout=5
            )
            
            # Push
            push_result = subprocess.run(
                ['git', 'push', '-u', 'origin', branch],
                cwd=local_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if push_result.returncode == 0:
                return (True, f"Successfully pushed to {repo_url}")
            else:
                # Try with force if needed (for existing repos)
                force_result = subprocess.run(
                    ['git', 'push', '-u', 'origin', branch, '--force'],
                    cwd=local_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if force_result.returncode == 0:
                    return (True, f"Successfully pushed to {repo_url} (force push)")
                else:
                    return (False, f"Failed to push: {push_result.stderr}")
        
        except subprocess.CalledProcessError as e:
            return (False, f"Git operation failed: {str(e)}")
        except Exception as e:
            return (False, f"Error pushing to repository: {str(e)}")
    
    def push_to_existing_repo(self, local_path: Path, repo_url: str, 
                              branch: str = "main", commit_message: str = "Update: Liberated project") -> Tuple[bool, str]:
        """
        Push to an existing GitHub repository.
        
        Args:
            local_path: Path to local project
            repo_url: GitHub repository URL
            branch: Branch name
            commit_message: Commit message
        
        Returns:
            Tuple of (success, message)
        """
        return self.push_to_repository(local_path, repo_url, branch, commit_message)
    
    def check_repository_exists(self, repo_url: str) -> Tuple[bool, bool]:
        """
        Check if a repository exists and is accessible.
        
        Args:
            repo_url: GitHub repository URL
        
        Returns:
            Tuple of (exists, is_accessible)
        """
        if self.gh_available:
            try:
                # Extract owner/repo from URL
                parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    result = subprocess.run(
                        ['gh', 'repo', 'view', f'{owner}/{repo}'],
                        capture_output=True,
                        timeout=10
                    )
                    return (True, result.returncode == 0)
            except:
                pass
        
        # Fallback: try to access via API
        if self.token:
            try:
                import urllib.request
                parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    url = f"https://api.github.com/repos/{owner}/{repo}"
                    req = urllib.request.Request(
                        url,
                        headers={
                            'Authorization': f'token {self.token}',
                            'Accept': 'application/vnd.github.v3+json'
                        }
                    )
                    with urllib.request.urlopen(req, timeout=10) as response:
                        return (True, response.status == 200)
            except:
                pass
        
        return (False, False)
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict]:
        """Get repository information."""
        if self.gh_available:
            try:
                parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                    result = subprocess.run(
                        ['gh', 'api', f'repos/{owner}/{repo}'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        return json.loads(result.stdout)
            except:
                pass
        return None
