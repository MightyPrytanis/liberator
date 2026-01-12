# Quick Start Guide

## Installation

```bash
# Clone or navigate to the liberator directory
cd liberator

# Install in development mode
pip install -e .
```

## Basic Usage

### 1. Liberate a Project

```bash
# Auto-detect platform and extract
liberator extract /path/to/captive-project -o ./liberated-app
```

### 2. Analyze Dependencies

```bash
# See what dependencies a project uses
liberator analyze /path/to/project --verbose
```

### 3. Export to Portable Format

```bash
# Export with all standard files
liberator export /path/to/project -o ./portable-app
```

## Common Workflows

### Workflow 1: Complete Liberation

```bash
# Step 1: Extract everything
liberator extract ./my-replit-app -o ./liberated --analyze --verbose

# Step 2: Review the output
cd liberated
cat README.md

# Step 3: Test the liberated app
docker-compose up
```

### Workflow 2: Dependency Audit

```bash
# Analyze what dependencies are being used
liberator analyze ./my-project --output deps.json

# Review the JSON output
cat deps.json | python3 -m json.tool
```

### Workflow 3: Platform Migration

```bash
# Extract from old platform
liberator extract ./old-platform-app -o ./migrated-app

# The output will have:
# - Standard config files
# - Docker setup
# - Documentation
# - All dependencies normalized
```

## Command Reference

### `liberator extract`

Extract a project from a proprietary platform.

**Options:**
- `-o, --output`: Output directory (required)
- `--platform`: Platform type (auto, base44, replit, generic)
- `--analyze`: Analyze code after extraction
- `--verbose`: Show detailed output

**Example:**
```bash
liberator extract ./replit-project -o ./free --analyze
```

### `liberator analyze`

Analyze project dependencies and structure.

**Options:**
- `--output`: Save analysis to JSON file
- `--verbose`: Show detailed analysis

**Example:**
```bash
liberator analyze ./project --output analysis.json --verbose
```

### `liberator export`

Export project to portable format.

**Options:**
- `-o, --output`: Output directory (required)
- `--docker`: Generate Docker files
- `--verbose`: Show detailed output

**Example:**
```bash
liberator export ./project -o ./portable --docker
```

## Troubleshooting

### "Platform not detected"

If auto-detection fails, specify the platform:
```bash
liberator extract ./project -o ./output --platform generic
```

### "No files extracted"

Check that:
1. The source path exists
2. You have read permissions
3. The project structure is recognized

### "Dependencies not found"

Some projects may not have standard dependency files. The analyzer will still try to detect dependencies from code imports.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [EXAMPLES.md](EXAMPLES.md) for more examples
- Review [MANIFEST.md](MANIFEST.md) for project philosophy

## Getting Help

- Check the documentation files
- Review example projects
- Open an issue on GitHub

---

**Happy liberating! 🎉**
