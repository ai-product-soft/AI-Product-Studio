#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VERSION="3.0.0"
APP_NAME="ai-product-studio"

echo "Building AppImage (requires appimagetool)..."

if ! command -v appimagetool &> /dev/null; then
    echo "WARNING: appimagetool not found. Install from https://github.com/AppImage/AppImageKit/releases"
    echo "Falling back to standalone executable..."
    bash "$SCRIPT_DIR/build-executable.sh"
    exit 0
fi

APPDIR="$SCRIPT_DIR/AppDir"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APPDIR/opt/$APP_NAME"

# Copy app source
rsync -av   --exclude='node_modules'   --exclude='.git'   --exclude='__pycache__'   --exclude='deliverables/*'   --exclude='dist'   --exclude='packaging'   "$ROOT_DIR/" "$APPDIR/opt/$APP_NAME/"

# Create AppRun
cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"

# AppImage for Docker-based app acts as a launcher
export APP_DIR="$HERE/opt/ai-product-studio"

if ! command -v docker &> /dev/null; then
    xmessage "Docker is required. Install from https://docs.docker.com/get-docker/" 2>/dev/null ||     echo "ERROR: Docker required"
    exit 1
fi

cd "$APP_DIR"
exec docker compose up -d
EOF
chmod +x "$APPDIR/AppRun"

# Desktop entry
cat > "$APPDIR/usr/share/applications/ai-product-studio.desktop" <<EOF
[Desktop Entry]
Name=AI Product Studio
Exec=AppRun
Icon=ai-product-studio
Type=Application
Categories=Development;
Comment=Private-cloud AI business automation
EOF
cp "$APPDIR/usr/share/applications/ai-product-studio.desktop" "$APPDIR/"

# Icon placeholder (create a simple SVG if none exists)
cat > "$APPDIR/usr/share/icons/hicolor/256x256/apps/ai-product-studio.svg" <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="32" fill="#1a1a2e"/>
  <text x="128" y="148" font-size="120" text-anchor="middle" fill="#e94560">AI</text>
</svg>
EOF
cp "$APPDIR/usr/share/icons/hicolor/256x256/apps/ai-product-studio.svg" "$APPDIR/ai-product-studio.svg"

# Build AppImage
mkdir -p "$ROOT_DIR/dist"
appimagetool "$APPDIR" "$ROOT_DIR/dist/${APP_NAME}-${VERSION}-x86_64.AppImage"

# Cleanup
rm -rf "$APPDIR"

echo "AppImage built: dist/${APP_NAME}-${VERSION}-x86_64.AppImage"
