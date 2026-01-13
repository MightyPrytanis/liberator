# Liberator

**Free your apps from proprietary platforms**

Liberator is a complete, end-to-end solution for "liberating" apps originally created in Base44, Replit, and other coding platforms that keep work product "captive" to proprietary backends. It provides the ability to duplicate, recreate, reverse-engineer, modify, and substitute code, dependencies, front-end, and everything else needed to take apps built in such environments and make them fully portable and open-source.

## Features

### Core Features
- 🔍 **Automatic Platform Detection** - Automatically detects Base44, Replit, and other platforms
- 📦 **Complete Extraction** - Extracts all code, dependencies, and configuration files
- 🔬 **Code Analysis** - Reverse-engineers code structure, dependencies, and patterns
- 🐳 **Docker Support** - Generates Dockerfiles and docker-compose.yml for easy deployment
- 📝 **Standard Configs** - Creates standard configuration files (package.json, requirements.txt, etc.)
- 🌍 **Environment Management** - Handles environment variables and secrets
- 📚 **Documentation Generation** - Auto-generates comprehensive README files
- 🔓 **Open Source Ready** - Adds LICENSE, .gitignore, and open-source best practices

### 🆕 New Features
- 🎯 **Single-Click Setup Wizard** - Guided setup in just a few clicks
- 🤖 **AI-Powered Assistant** - Code repair, refactoring, troubleshooting, and help
- 🎬 **Executive Producer** - Guarantees apps work on Windows, macOS, Linux, iOS, Android
- 📁 **Project Management** - Track and manage all liberated projects

## Installation

### Quick Start (Recommended)

**Run the Setup Wizard for easy installation:**
```bash
python3 run_setup_wizard.py
```

The wizard will:
- Install all dependencies
- Configure AI assistant (optional)
- Verify everything works
- Get you ready in minutes!

### Manual Installation

**From Source:**
```bash
git clone https://github.com/yourusername/liberator.git
cd liberator
pip install -e .
```

**GUI Installation (macOS):**
```bash
# Install GUI dependencies
./install_gui.sh

# Or manually:
pip install PyQt6

# Run the GUI
python3 liberator_gui.py
# Or
liberator-gui
```

**AI Assistant (Optional):**
```bash
pip install openai anthropic
# Perplexity uses standard library (no package needed)
# Then configure API keys in setup wizard or ~/.liberator/ai_config.json
# Note: API keys are stored securely and never committed to Git
```

### Build macOS App Bundle

To create a native macOS app:

```bash
./build_macos_app.sh
open dist/Liberator.app
```

### Setting Up GitHub (For Contributors)

If you've cloned or created this repository locally and want to connect it to GitHub:

```bash
# Run the setup script
./setup_github.sh

# Or manually:
# 1. Create a new repository on GitHub
# 2. Add the remote:
git remote add origin https://github.com/YOUR_USERNAME/liberator.git
# 3. Push:
git push -u origin main
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Usage

### GUI (macOS)

Launch the graphical interface:

```bash
python3 liberator_gui.py
# Or double-click Liberator.app if built
```

The GUI provides:
- **Extract Tab**: Visual interface for liberating projects
  - Drag & drop project folders
  - Platform selection
  - Real-time progress tracking
  - Extraction logs
  
- **Analyze Tab**: Dependency and code structure analysis
  - Visual dependency tree
  - Language detection
  - Code structure overview

### Command Line

```bash
# Liberate a project (auto-detect platform)
liberator extract /path/to/captive-project -o ./liberated-app

# Liberate from URL (GitHub, GitLab, etc.)
liberator extract https://github.com/user/repo -o ./liberated-app

# Liberate with OS compatibility (Windows, macOS, Linux)
liberator extract /path/to/project -o ./liberated-app --target-os windows macos linux

# Liberate and push to GitHub (create new repo)
liberator extract /path/to/project -o ./liberated-app --github "new:my-repo"

# Liberate and push to existing GitHub repo
liberator extract /path/to/project -o ./liberated-app --github "https://github.com/user/repo"

# Specify platform explicitly
liberator extract /path/to/replit-project -o ./liberated-app --platform replit

# Analyze dependencies only
liberator analyze /path/to/project

# Export to portable format
liberator export /path/to/project -o ./portable-app
```

### Examples

#### Liberating a Replit Project

```bash
liberator extract ~/my-replit-project -o ./my-liberated-app
```

This will:
1. Detect that it's a Replit project
2. Extract all source files
3. Analyze dependencies
4. Generate standard config files
5. Create Docker setup
6. Generate README and LICENSE

#### Liberating a Base44 Project

```bash
liberator extract ~/my-base44-project -o ./my-liberated-app --platform base44
```

#### Analyzing Dependencies

```bash
liberator analyze /path/to/project --verbose
```

This will show:
- All detected dependencies by type (npm, pip, go, cargo)
- Code structure analysis
- Language detection

## Supported Platforms

- ✅ **Base44** - Full support
- ✅ **Replit** - Full support
- ✅ **Generic** - Fallback for unknown platforms

## Project Structure

After liberation, your project will have:

```
liberated-app/
├── src/                    # Your source code
├── package.json           # Node.js dependencies (if applicable)
├── requirements.txt       # Python dependencies (if applicable)
├── go.mod                # Go dependencies (if applicable)
├── Cargo.toml            # Rust dependencies (if applicable)
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # Comprehensive documentation
```

## How It Works

1. **Detection** - Automatically detects the platform type
2. **Extraction** - Extracts all files, dependencies, and configuration
3. **Analysis** - Analyzes code structure and dependencies
4. **Normalization** - Normalizes dependencies across package managers
5. **Export** - Creates portable, open-source project structure
6. **Documentation** - Generates comprehensive documentation

## Advanced Features

### Code Analysis

Liberator performs deep code analysis to:
- Detect all imports and dependencies
- Identify functions, classes, and modules
- Understand project structure
- Find hidden dependencies

### Dependency Normalization

Automatically converts dependencies to standard formats:
- npm packages → package.json
- Python packages → requirements.txt
- Go modules → go.mod
- Rust crates → Cargo.toml

### Reverse Engineering

Liberator can reverse-engineer:
- Project structure
- Build configurations
- Runtime environments
- Deployment settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Philosophy

Liberator is built on the principle that your code should be free. No platform should hold your work captive. This tool ensures that apps built on proprietary platforms can be fully extracted, understood, modified, and made portable.

## Roadmap

- [ ] Support for more platforms (CodeSandbox, StackBlitz, etc.)
- [ ] GUI interface
- [ ] Cloud extraction (direct API access)
- [ ] Automated testing after extraction
- [ ] CI/CD pipeline generation
- [ ] Database migration tools

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for the open-source community**
