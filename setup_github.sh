#!/bin/bash
# Script to connect Liberator to GitHub

echo "🚀 Setting up GitHub repository for Liberator"
echo ""
echo "This script will help you connect your local repository to GitHub."
echo ""

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "✓ Remote 'origin' already exists:"
    git remote -v
    echo ""
    read -p "Do you want to update it? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing remote."
        exit 0
    fi
fi

echo "To connect to GitHub, you have two options:"
echo ""
echo "Option 1: Create a new repository on GitHub first, then run:"
echo "  git remote add origin https://github.com/YOUR_USERNAME/liberator.git"
echo "  git push -u origin main"
echo ""
echo "Option 2: Use GitHub CLI (if installed):"
echo "  gh repo create liberator --public --source=. --remote=origin --push"
echo ""

read -p "Enter your GitHub username (or press Enter to skip): " GITHUB_USER
if [ -z "$GITHUB_USER" ]; then
    echo "Skipping automatic setup. Please set up the remote manually."
    exit 0
fi

read -p "Enter repository name (default: liberator): " REPO_NAME
REPO_NAME=${REPO_NAME:-liberator}

echo ""
echo "Choose remote URL type:"
echo "1) HTTPS (https://github.com/$GITHUB_USER/$REPO_NAME.git)"
echo "2) SSH (git@github.com:$GITHUB_USER/$REPO_NAME.git)"
read -p "Enter choice (1 or 2): " URL_TYPE

if [ "$URL_TYPE" == "1" ]; then
    REMOTE_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"
elif [ "$URL_TYPE" == "2" ]; then
    REMOTE_URL="git@github.com:$GITHUB_USER/$REPO_NAME.git"
else
    echo "Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "Adding remote: $REMOTE_URL"
git remote add origin "$REMOTE_URL" 2>/dev/null || git remote set-url origin "$REMOTE_URL"

echo "✓ Remote configured!"
echo ""
echo "Next steps:"
echo "1. Create the repository on GitHub (if it doesn't exist):"
echo "   Visit: https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo "   (Don't initialize with README, .gitignore, or license - we already have them)"
echo ""
echo "2. Push your code:"
echo "   git push -u origin main"
echo ""
