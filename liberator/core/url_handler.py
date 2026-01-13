"""
URL handler for downloading and cloning projects from URLs.
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse
import shutil


class URLHandler:
    """Handles downloading and cloning projects from URLs."""
    
    @staticmethod
    def is_url(source: str) -> bool:
        """Check if source is a URL."""
        return source.startswith(('http://', 'https://', 'git@', 'git://'))
    
    @staticmethod
    def detect_url_type(url: str) -> str:
        """Detect the type of URL."""
        parsed = urlparse(url)
        
        if 'github.com' in url or 'github.io' in url:
            return 'github'
        elif 'gitlab.com' in url:
            return 'gitlab'
        elif 'bitbucket.org' in url:
            return 'bitbucket'
        elif url.startswith('git@') or url.startswith('git://'):
            return 'git'
        elif url.endswith('.git'):
            return 'git'
        elif url.endswith(('.zip', '.tar.gz', '.tar')):
            return 'archive'
        else:
            return 'generic'
    
    @staticmethod
    def download_from_url(url: str, output_dir: Optional[Path] = None) -> Path:
        """
        Download or clone a project from a URL.
        
        Args:
            url: Source URL
            output_dir: Optional output directory (creates temp dir if not provided)
        
        Returns:
            Path to downloaded/cloned project
        """
        if output_dir is None:
            output_dir = Path(tempfile.mkdtemp(prefix='liberator_'))
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        url_type = URLHandler.detect_url_type(url)
        
        if url_type in ['github', 'gitlab', 'bitbucket', 'git']:
            return URLHandler._clone_git_repo(url, output_dir)
        elif url_type == 'archive':
            return URLHandler._download_archive(url, output_dir)
        else:
            # Try git first, then fallback to download
            try:
                return URLHandler._clone_git_repo(url, output_dir)
            except:
                return URLHandler._download_generic(url, output_dir)
    
    @staticmethod
    def _clone_git_repo(url: str, output_dir: Path) -> Path:
        """Clone a git repository."""
        # Normalize GitHub URLs
        if 'github.com' in url and not url.endswith('.git'):
            if not url.endswith('/'):
                url += '/'
            url += 'archive/refs/heads/main.zip'
            return URLHandler._download_archive(url, output_dir)
        
        # Try git clone
        try:
            repo_name = url.split('/')[-1].replace('.git', '')
            clone_dir = output_dir / repo_name
            
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', url, str(clone_dir)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                return clone_dir
            else:
                raise Exception(f"Git clone failed: {result.stderr}")
        except FileNotFoundError:
            # Git not installed, try downloading as archive
            if 'github.com' in url:
                # Convert to archive URL
                if not url.endswith('.git'):
                    url = url.rstrip('/') + '.git'
                archive_url = url.replace('.git', '/archive/refs/heads/main.zip')
                return URLHandler._download_archive(archive_url, output_dir)
            raise Exception("Git is not installed and cannot download repository")
    
    @staticmethod
    def _download_archive(url: str, output_dir: Path) -> Path:
        """Download and extract an archive."""
        import urllib.request
        import zipfile
        import tarfile
        
        # Download to temp file
        temp_file = output_dir / 'archive.zip'
        
        try:
            print(f"Downloading {url}...")
            urllib.request.urlretrieve(url, temp_file)
            
            # Extract
            if url.endswith('.zip'):
                with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
                temp_file.unlink()
                
                # Find extracted directory
                extracted_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
                if extracted_dirs:
                    return extracted_dirs[0]
                return output_dir
            elif url.endswith(('.tar.gz', '.tar')):
                with tarfile.open(temp_file, 'r:*') as tar_ref:
                    tar_ref.extractall(output_dir)
                temp_file.unlink()
                
                extracted_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
                if extracted_dirs:
                    return extracted_dirs[0]
                return output_dir
            else:
                raise Exception(f"Unsupported archive format: {url}")
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()
            raise Exception(f"Failed to download archive: {str(e)}")
    
    @staticmethod
    def _download_generic(url: str, output_dir: Path) -> Path:
        """Download a generic URL (fallback)."""
        import urllib.request
        
        filename = url.split('/')[-1]
        if not filename or '.' not in filename:
            filename = 'download'
        
        output_file = output_dir / filename
        
        try:
            urllib.request.urlretrieve(url, output_file)
            return output_dir
        except Exception as e:
            raise Exception(f"Failed to download: {str(e)}")
    
    @staticmethod
    def cleanup_temp_dir(path: Path):
        """Clean up temporary directory."""
        try:
            if path.exists() and str(path).startswith(tempfile.gettempdir()):
                shutil.rmtree(path)
        except:
            pass
