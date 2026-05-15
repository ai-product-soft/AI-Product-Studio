#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VERSION="3.0.0"
ARCH="amd64"
PKG_NAME="ai-product-studio"
DEB_DIR="$SCRIPT_DIR/build/$PKG_NAME"

echo "Building Debian package..."

# Clean and create structure
rm -rf "$SCRIPT_DIR/build"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/opt/$PKG_NAME"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/etc/systemd/system"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/icons/hicolor/256x256/apps"

# Copy application source (exclude node_modules, venv, etc.)
rsync -av   --exclude='node_modules'   --exclude='.git'   --exclude='__pycache__'   --exclude='*.pyc'   --exclude='deliverables/*'   --exclude='dist'   --exclude='packaging'   "$ROOT_DIR/" "$DEB_DIR/opt/$PKG_NAME/"

# Create control file
cat > "$DEB_DIR/DEBIAN/control" <<EOF
Package: $PKG_NAME
Version: $VERSION
Section: web
Priority: optional
Architecture: $ARCH
Depends: docker.io (>= 24.0), docker-compose-plugin (>= 2.0), curl, bash
Maintainer: AI Product Studio <dev@aiproductstudio.local>
Description: AI Product Studio v3.0
 Private-cloud business automation suite.
 From idea to revenue — research, plan, generate, promote, and sell
 AI-built products using local LLMs (Ollama).
EOF

# Create postinst
cat > "$DEB_DIR/DEBIAN/postinst" <<'EOF'
#!/bin/bash
set -e

APP_DIR="/opt/ai-product-studio"
USER="aistudio"

# Create user if not exists
if ! id "$USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$APP_DIR" "$USER"
fi

# Add user to docker group
usermod -aG docker "$USER" 2>/dev/null || true

# Enable and start service
systemctl daemon-reload
systemctl enable ai-product-studio.service
systemctl start ai-product-studio.service || true

echo "AI Product Studio installed."
echo "Access dashboard at: http://localhost:5173"
echo "API at: http://localhost:8000"
EOF
chmod 755 "$DEB_DIR/DEBIAN/postinst"

# Create prerm
cat > "$DEB_DIR/DEBIAN/prerm" <<'EOF'
#!/bin/bash
set -e

systemctl stop ai-product-studio.service 2>/dev/null || true
systemctl disable ai-product-studio.service 2>/dev/null || true

# Stop all app containers
cd /opt/ai-product-studio || exit 0
docker compose down 2>/dev/null || true
EOF
chmod 755 "$DEB_DIR/DEBIAN/prerm"

# Create postrm
cat > "$DEB_DIR/DEBIAN/postrm" <<'EOF'
#!/bin/bash
set -e

if [ "$1" = "purge" ]; then
    rm -rf /opt/ai-product-studio
    rm -rf /var/lib/ai-product-studio
    userdel aistudio 2>/dev/null || true
fi
EOF
chmod 755 "$DEB_DIR/DEBIAN/postrm"

# Create launcher script
cat > "$DEB_DIR/usr/bin/ai-product-studio" <<'EOF'
#!/bin/bash
cd /opt/ai-product-studio || exit 1

case "$1" in
    start)
        docker compose up -d
        echo "AI Product Studio started."
        echo "Dashboard: http://localhost:5173"
        ;;
    stop)
        docker compose down
        echo "AI Product Studio stopped."
        ;;
    restart)
        docker compose down && docker compose up -d
        ;;
    status)
        docker compose ps
        ;;
    logs)
        docker compose logs -f "${2:-backend}"
        ;;
    update)
        docker compose pull
        docker compose up -d
        ;;
    shell)
        docker compose exec backend bash
        ;;
    *)
        echo "Usage: ai-product-studio {start|stop|restart|status|logs|update|shell}"
        exit 1
        ;;
esac
EOF
chmod 755 "$DEB_DIR/usr/bin/ai-product-studio"

# Create systemd service
cat > "$DEB_DIR/etc/systemd/system/ai-product-studio.service" <<EOF
[Unit]
Description=AI Product Studio v3.0
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/ai-product-studio
ExecStart=/usr/bin/ai-product-studio start
ExecStop=/usr/bin/ai-product-studio stop
User=root
Group=docker

[Install]
WantedBy=multi-user.target
EOF

# Create .desktop entry
cat > "$DEB_DIR/usr/share/applications/ai-product-studio.desktop" <<EOF
[Desktop Entry]
Name=AI Product Studio
Comment=Private-cloud AI business automation
Exec=xdg-open http://localhost:5173
Type=Application
Icon=ai-product-studio
Categories=Development;WebDevelopment;
EOF

# Build the .deb
dpkg-deb --build "$DEB_DIR" "$ROOT_DIR/dist/${PKG_NAME}_${VERSION}_${ARCH}.deb"

echo "Debian package built: dist/${PKG_NAME}_${VERSION}_${ARCH}.deb"
