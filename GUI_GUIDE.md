# Liberator GUI Guide

## Overview

Liberator includes a fully functional graphical user interface (GUI) built with PyQt6, designed specifically for macOS. The GUI provides an intuitive way to liberate projects without using the command line.

## Installation

### Prerequisites

- macOS 10.13 or later
- Python 3.8 or later
- PyQt6

### Quick Install

```bash
# Run the installation script
./install_gui.sh

# Or install manually
pip3 install PyQt6
```

## Running the GUI

### Method 1: Direct Python Script

```bash
python3 liberator_gui.py
```

### Method 2: Using Entry Point (after installation)

```bash
liberator-gui
```

### Method 3: macOS App Bundle

Build and run as a native macOS app:

```bash
./build_macos_app.sh
open dist/Liberator.app
```

## GUI Features

### Extract Tab

The main interface for liberating projects:

1. **Source Selection**
   - Click "Browse..." to select a project folder
   - Or drag and drop a folder directly onto the source path field
   - Supports Base44, Replit, and generic projects

2. **Platform Selection**
   - **Auto-detect**: Automatically detects the platform (recommended)
   - **Base44**: Force Base44 extraction
   - **Replit**: Force Replit extraction
   - **Generic**: Generic extraction for unknown platforms

3. **Output Directory**
   - Select where to save the liberated project
   - The output will contain all extracted files plus:
     - Standard configuration files (package.json, requirements.txt, etc.)
     - Docker setup (Dockerfile, docker-compose.yml)
     - Documentation (README.md)
     - License and .gitignore

4. **Options**
   - **Analyze code after extraction**: Performs detailed code analysis after extraction

5. **Extraction Process**
   - Real-time progress updates
   - Detailed extraction log
   - Success/error notifications

### Analyze Tab

Analyze project dependencies and structure:

1. **Project Selection**
   - Select a project folder to analyze
   - Works with any project, not just proprietary platforms

2. **Analysis Results**
   - **Dependencies Tree**: Visual tree of all dependencies by type
     - npm packages
     - Python packages (pip)
     - Go modules
     - Rust crates
   - **Analysis Summary**: Detailed breakdown including:
     - Total files analyzed
     - Languages detected
     - Dependency counts by type
     - Full dependency lists

### Export Tab

The export functionality is integrated into the Extract tab. When you extract a project, it's automatically exported to a portable format.

## Keyboard Shortcuts

- **Cmd+O**: Open project
- **Cmd+Q**: Quit application
- **Cmd+,**: Preferences (coming soon)
- **F1**: Help

## macOS-Specific Features

- **Native Menu Bar**: Full macOS menu bar integration
- **Native File Dialogs**: Uses macOS file picker dialogs
- **Drag & Drop**: Drag folders directly into the interface
- **High DPI Support**: Retina display support
- **App Bundle**: Can be built as a native .app bundle

## Troubleshooting

### "PyQt6 is required for the GUI"

Install PyQt6:
```bash
pip3 install PyQt6
```

### GUI won't start

Check Python version:
```bash
python3 --version  # Should be 3.8+
```

### Import errors

Make sure you're in the liberator directory:
```bash
cd /path/to/liberator
python3 liberator_gui.py
```

### App bundle won't open

Check that the build script ran successfully:
```bash
./build_macos_app.sh
ls -la dist/Liberator.app
```

## Tips

1. **Drag & Drop**: The easiest way to select projects is to drag them from Finder
2. **Auto-detect**: Use auto-detect for platform selection - it's usually accurate
3. **Analysis**: Run analysis on projects to understand their dependencies before extraction
4. **Logs**: Check the extraction log for detailed information about the process

## Screenshots

The GUI features:
- Clean, modern interface
- Real-time progress tracking
- Visual dependency trees
- Comprehensive logging
- Native macOS look and feel

## Future Enhancements

- Preferences panel for customization
- Batch processing multiple projects
- Export analysis results to JSON/CSV
- Dark mode support
- Project templates
- Integration with version control

---

For command-line usage, see the main [README.md](README.md).
