#!/bin/bash
# Build macOS app bundle for Liberator

set -e

APP_NAME="Liberator"
APP_DIR="dist/${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

echo "🍎 Building macOS app bundle for ${APP_NAME}..."

# Create directory structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>liberator_gui</string>
    <key>CFBundleIdentifier</key>
    <string>com.liberator.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>${APP_NAME}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
EOF

# Create launcher script
cat > "${MACOS_DIR}/liberator_gui" << 'EOF'
#!/bin/bash
# Liberator GUI Launcher

# Get the directory where the app bundle is located
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LIBERATOR_DIR="$(dirname "$APP_DIR")"

# Activate virtual environment if it exists
if [ -d "${LIBERATOR_DIR}/venv" ]; then
    source "${LIBERATOR_DIR}/venv/bin/activate"
fi

# Run the GUI
cd "${LIBERATOR_DIR}"
python3 liberator_gui.py "$@"
EOF

chmod +x "${MACOS_DIR}/liberator_gui"

# Copy icon if it exists
if [ -f "assets/icon.icns" ]; then
    cp "assets/icon.icns" "${RESOURCES_DIR}/icon.icns"
    # Update Info.plist to include icon
    /usr/libexec/PlistBuddy -c "Add :CFBundleIconFile string icon" "${CONTENTS_DIR}/Info.plist" 2>/dev/null || \
    /usr/libexec/PlistBuddy -c "Set :CFBundleIconFile icon" "${CONTENTS_DIR}/Info.plist"
fi

echo "✅ App bundle created at: ${APP_DIR}"
echo ""
echo "To run the app:"
echo "  open ${APP_DIR}"
echo ""
echo "To create a DMG installer, use:"
echo "  hdiutil create -volname ${APP_NAME} -srcfolder ${APP_DIR} -ov -format UDZO dist/${APP_NAME}.dmg"
