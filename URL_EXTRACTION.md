# URL Extraction Feature

## Overview

Liberator now supports extracting projects directly from URLs! You can liberate projects from GitHub, GitLab, Bitbucket, and other git repositories without having to clone them manually first.

## Supported URL Types

### Git Repositories
- **GitHub**: `https://github.com/user/repo`
- **GitLab**: `https://gitlab.com/user/repo`
- **Bitbucket**: `https://bitbucket.org/user/repo`
- **Generic Git**: `git@github.com:user/repo.git` or `git://example.com/repo.git`

### Archive Downloads
- **ZIP files**: `https://example.com/project.zip`
- **TAR files**: `https://example.com/project.tar.gz`

## Usage

### Command Line

**Extract from GitHub:**
```bash
liberator extract https://github.com/user/repo -o ./liberated-app
```

**Extract from GitLab:**
```bash
liberator extract https://gitlab.com/user/repo -o ./liberated-app
```

**Extract from archive:**
```bash
liberator extract https://example.com/project.zip -o ./liberated-app
```

### GUI

**In the Extract tab:**
1. Click "Browse/URL..." button
2. Choose "Enter URL"
3. Paste the repository URL
4. Click "Liberate Project"

**Or directly paste URL:**
1. Paste URL directly into the source field
2. Click "Liberate Project"

## How It Works

1. **URL Detection**: Liberator automatically detects if the source is a URL
2. **Download/Clone**: 
   - For git repos: Clones the repository (or downloads as archive if git not available)
   - For archives: Downloads and extracts the archive
3. **Temporary Storage**: Downloads to a temporary directory
4. **Extraction**: Extracts the project as normal
5. **Cleanup**: Automatically cleans up temporary files after extraction

## Examples

### GitHub Repository
```bash
liberator extract https://github.com/octocat/Hello-World -o ./hello-world-liberated
```

### GitLab Repository
```bash
liberator extract https://gitlab.com/gitlab-org/gitlab -o ./gitlab-liberated
```

### Private Repositories

For private repositories, you'll need to:
1. Use SSH URLs: `git@github.com:user/repo.git`
2. Or authenticate with git credentials
3. Or download manually and use local path

### Specific Branch or Tag

GitHub archive URLs support branches:
```bash
# Main branch
liberator extract https://github.com/user/repo/archive/refs/heads/main.zip -o ./output

# Specific branch
liberator extract https://github.com/user/repo/archive/refs/heads/develop.zip -o ./output

# Tag
liberator extract https://github.com/user/repo/archive/refs/tags/v1.0.0.zip -o ./output
```

## Requirements

### Git Repositories
- **Git installed**: For cloning repositories (recommended)
- **Fallback**: If git not available, downloads as ZIP archive (GitHub/GitLab)

### Archive Downloads
- **No requirements**: Works with standard Python libraries

## Limitations

1. **Private Repositories**: May require authentication
2. **Large Repositories**: May take time to download
3. **Network**: Requires internet connection
4. **Rate Limits**: GitHub/GitLab may have rate limits for unauthenticated requests

## Troubleshooting

### "Git is not installed"
- Install git: `brew install git` (macOS)
- Or use archive URLs instead

### "Permission denied"
- For private repos, use SSH URLs or authenticate
- Or download manually first

### "Download failed"
- Check internet connection
- Verify URL is correct
- Try using git clone manually first

### "Timeout"
- Large repositories may timeout
- Try downloading manually first
- Or use shallow clone: `git clone --depth 1 URL`

## Best Practices

1. **Use HTTPS URLs** for public repositories
2. **Use SSH URLs** for private repositories (if you have SSH keys set up)
3. **Specify branch/tag** if you need a specific version
4. **Check repository size** before extracting very large projects
5. **Use local paths** for repositories you've already cloned

## Technical Details

- **Temporary Storage**: Uses system temp directory (`/tmp/liberator_*`)
- **Automatic Cleanup**: Temporary files are deleted after extraction
- **Error Handling**: Graceful fallback if git clone fails
- **Progress**: Shows download progress in GUI and CLI

---

**URL extraction makes it even easier to liberate projects! 🚀**
