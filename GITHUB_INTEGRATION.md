# GitHub Integration

## Overview

Liberator now includes full GitHub integration, allowing you to push liberated projects directly to GitHub repositories. You can either create new repositories or push to existing ones.

## Features

- ✅ **Create New Repository** - Automatically create GitHub repositories
- ✅ **Push to Existing Repository** - Push to repositories you already have
- ✅ **Automatic Git Setup** - Initializes git, commits, and pushes automatically
- ✅ **GUI Integration** - Full GUI support with dedicated GitHub tab
- ✅ **CLI Support** - Command-line options for GitHub push
- ✅ **GitHub CLI Support** - Uses `gh` CLI if available
- ✅ **API Support** - Falls back to GitHub API if CLI not available

## Setup

### Option 1: GitHub CLI (Recommended)

Install GitHub CLI:
```bash
brew install gh
gh auth login
```

### Option 2: Personal Access Token

Set environment variable:
```bash
export GITHUB_TOKEN="your_personal_access_token"
# Or
export GH_TOKEN="your_personal_access_token"
```

**Create Token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control of private repositories)
4. Copy token and set as environment variable

## Usage

### GUI

**GitHub Tab:**
1. Go to "GitHub" tab in the GUI
2. Select your liberated project directory
3. Choose option:
   - **Create new repository**: Enter name, description, privacy
   - **Use existing repository**: Enter repository URL
4. Configure branch and commit message
5. Click "🚀 Push to GitHub"

**After Extraction:**
- After successful extraction, you'll be asked if you want to push to GitHub
- Click "Yes" to automatically switch to GitHub tab with project pre-selected

### Command Line

**Create New Repository:**
```bash
liberator extract /path/to/project -o ./liberated-app --github "new:my-repo-name"
```

**Create Private Repository:**
```bash
liberator extract /path/to/project -o ./liberated-app --github "new:my-repo-name" --github-private
```

**Push to Existing Repository:**
```bash
liberator extract /path/to/project -o ./liberated-app --github "https://github.com/username/repo"
```

**Custom Branch:**
```bash
liberator extract /path/to/project -o ./liberated-app --github "new:my-repo" --github-branch develop
```

## Repository Options

### New Repository

- **Name**: Repository name (required)
- **Description**: Optional description
- **Private**: Check for private repository
- **Organization**: Can be specified via GitHub CLI

### Existing Repository

- **URL**: Full GitHub repository URL
  - `https://github.com/username/repo`
  - `https://github.com/username/repo.git`
- **Check Repository**: Verify repository exists and is accessible

## Commit Options

- **Branch**: Default is `main` (can be `master`, `develop`, or custom)
- **Commit Message**: Default is "Initial commit: Liberated project"

## Workflow Examples

### Example 1: Complete Liberation to GitHub

```bash
# Extract and push in one command
liberator extract https://github.com/user/captive-app -o ./liberated \
  --github "new:liberated-app"
```

### Example 2: GUI Workflow

1. Extract project (Extract tab)
2. After extraction, click "Yes" when asked about GitHub
3. GitHub tab opens with project selected
4. Choose "Create new repository"
5. Enter repository name
6. Click "🚀 Push to GitHub"
7. Done! Your project is on GitHub

### Example 3: Push Existing Project

```bash
# If you already have a liberated project
cd ./liberated-project
git init
liberator extract . -o . --github "https://github.com/user/existing-repo"
```

## Technical Details

### Git Operations

The integration automatically:
1. Initializes git repository (if not already)
2. Adds remote origin
3. Stages all files
4. Commits with your message
5. Pushes to specified branch

### Authentication

**GitHub CLI:**
- Uses `gh auth login` credentials
- No token needed if CLI is authenticated

**API Token:**
- Uses `GITHUB_TOKEN` or `GH_TOKEN` environment variable
- Requires `repo` scope for private repositories

### Error Handling

- **Repository exists**: Will push to existing repo
- **Permission denied**: Check authentication
- **Network error**: Check internet connection
- **Git not installed**: Install git: `brew install git`

## Troubleshooting

### "GitHub CLI or token not configured"

**Solution:**
```bash
# Option 1: Install and login to GitHub CLI
brew install gh
gh auth login

# Option 2: Set token
export GITHUB_TOKEN="your_token"
```

### "Failed to create repository"

**Possible causes:**
- Repository name already exists
- Invalid repository name
- Insufficient permissions
- Network error

**Solution:**
- Check repository name is unique
- Verify authentication
- Try again or use existing repository

### "Failed to push"

**Possible causes:**
- Repository doesn't exist
- No write permissions
- Branch conflict
- Network error

**Solution:**
- Verify repository URL is correct
- Check you have write access
- Try different branch name
- Check internet connection

### "Git is not installed"

**Solution:**
```bash
brew install git
```

## Best Practices

1. **Use GitHub CLI** for easiest setup
2. **Check repository** before pushing to existing repos
3. **Use descriptive commit messages**
4. **Set appropriate branch** (main/master/develop)
5. **Review before pushing** - check what will be committed

## Security

- Tokens are stored in environment variables (not in code)
- Private repositories require proper authentication
- Git operations use standard git authentication
- No credentials are logged or stored

## Limitations

- Requires git to be installed
- Requires GitHub CLI or API token
- Large repositories may take time to push
- Network connection required

---

**GitHub integration makes it easy to share your liberated projects! 🚀**
