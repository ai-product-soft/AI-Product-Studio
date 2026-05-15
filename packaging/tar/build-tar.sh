#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VERSION="3.0.0"
PKG_NAME="ai-product-studio-${VERSION}"

echo "Building tar.xz source archive..."

mkdir -p "$ROOT_DIR/dist"
TMP_DIR="$SCRIPT_DIR/tmp"
mkdir -p "$TMP_DIR"

# Copy to temp dir with proper name
rsync -av   --exclude='node_modules'   --exclude='.git'   --exclude='__pycache__'   --exclude='*.pyc'   --exclude='deliverables/*'   --exclude='dist'   --exclude='packaging/tmp'   "$ROOT_DIR/" "$TMP_DIR/$PKG_NAME/"

# Create install script inside archive
cat > "$TMP_DIR/$PKG_NAME/install.sh" <<'EOF'
#!/bin/bash
set -e

echo "=========================================="
echo "  AI Product Studio v3.0.0 Installer"
echo "=========================================="

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose is not installed."
    exit 1
fi

INSTALL_DIR="${1:-$HOME/ai-product-studio}"
echo "Installing to: $INSTALL_DIR"

mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"
cd "$INSTALL_DIR"

echo ""
echo "Setup complete. To start:"
echo "  cd $INSTALL_DIR"
echo "  docker compose up -d"
echo ""
echo "Then open: http://localhost:5173"
EOF
chmod +x "$TMP_DIR/$PKG_NAME/install.sh"

# Create README for archive
cat > "$TMP_DIR/$PKG_NAME/README-INSTALL.txt" <<EOF
AI Product Studio v${VERSION}
==============================

Quick Start:
  1. Extract this archive
  2. Run: ./install.sh
  3. Or manually: docker compose up -d

Requirements:
  - Docker 24.0+
  - Docker Compose 2.0+
  - 16GB RAM recommended (8GB minimum with swap)
  - 50GB free disk space

Post-install:
  - Pull Ollama models:
    docker compose exec ollama ollama pull mistral:7b-instruct-v0.2-q4_K_M
    docker compose exec ollama ollama pull nomic-embed-text

  - Run migrations:
    docker compose exec backend alembic upgrade head

Dashboard: http://localhost:5173
API Docs:  http://localhost:8000/docs
EOF

# Compress
cd "$TMP_DIR"
tar -cJf "$ROOT_DIR/dist/${PKG_NAME}.tar.xz" "$PKG_NAME"

# Cleanup
rm -rf "$TMP_DIR"

echo "tar.xz archive built: dist/${PKG_NAME}.tar.xz"
