# Installation Features

## Setup Wizard - Installation Options

The setup wizard now includes an **Installation Options** page that allows you to automatically create shortcuts and install Liberator for easy access.

### Features

1. **Desktop Shortcut**
   - Creates a launcher script on your Desktop
   - Double-click to launch Liberator GUI
   - Automatically navigates to the project directory

2. **Applications Folder Installation**
   - Builds macOS app bundle automatically
   - Copies `Liberator.app` to `/Applications`
   - Launch from Spotlight or Applications folder
   - Command: `open -a Liberator`

3. **Dock Integration** (Optional)
   - Note: Dock addition requires manual setup
   - You can drag the app to Dock after installation

4. **Skip Option**
   - Choose to skip installation
   - Use command line only if preferred

### How It Works

**During Setup Wizard:**
1. After verification, you'll see the "Installation Options" page
2. Select your preferred installation options:
   - ✅ Create desktop shortcut (default: ON)
   - ✅ Install to Applications folder (default: ON)
   - ⬜ Add to Dock (default: OFF)
   - ⬜ Skip installation
3. Click "Install Shortcuts"
4. The wizard will:
   - Build app bundle if needed
   - Create desktop shortcut
   - Copy to Applications folder
   - Show status of each operation

### Installation Locations

**Desktop Shortcut:**
- Location: `~/Desktop/Liberator`
- Type: Executable shell script
- Launches: `python3 liberator_gui.py`

**Applications Folder:**
- Location: `/Applications/Liberator.app`
- Type: macOS app bundle
- Launch: Double-click or `open -a Liberator`

### Permissions

**Desktop Shortcut:**
- No special permissions needed
- Created automatically

**Applications Folder:**
- May require administrator password
- If permission denied, you can:
  - Run manually: `sudo cp -R dist/Liberator.app /Applications/`
  - Or drag and drop manually

### After Installation

**Launch Options:**
1. **Desktop**: Double-click `Liberator` on Desktop
2. **Applications**: 
   - Open Applications folder
   - Double-click `Liberator.app`
   - Or use Spotlight: `Cmd+Space`, type "Liberator"
3. **Command Line**: `liberator` or `liberator-gui`
4. **Terminal**: `python3 liberator_gui.py`

### Troubleshooting

**Desktop shortcut not working:**
- Check file permissions: `chmod +x ~/Desktop/Liberator`
- Verify Python path in script

**Applications installation failed:**
- Permission denied: Run with sudo or install manually
- App bundle not found: Build it first with `./build_macos_app.sh`

**App won't launch from Applications:**
- Check that Python 3 is installed
- Verify PyQt6 is installed
- Check console for error messages

### Manual Installation

If you prefer to install manually:

```bash
# Build app bundle
./build_macos_app.sh

# Copy to Applications
cp -R dist/Liberator.app /Applications/

# Create desktop shortcut
cat > ~/Desktop/Liberator << 'EOF'
#!/bin/bash
cd /path/to/liberator
python3 liberator_gui.py "$@"
EOF
chmod +x ~/Desktop/Liberator
```

---

**The installation page makes it easy to set up Liberator for daily use! 🚀**
