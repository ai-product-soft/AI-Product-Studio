#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VERSION="3.0.0"
ARCH="amd64"

echo "=========================================="
echo "  AI Product Studio v${VERSION} Builder"
echo "=========================================="

mkdir -p "$ROOT_DIR/dist"

# 1. Build .deb
echo "[1/3] Building .deb package..."
bash "$SCRIPT_DIR/deb/build-deb.sh"

# 2. Build tar.xz
echo "[2/3] Building tar.xz archive..."
bash "$SCRIPT_DIR/tar/build-tar.sh"

# 3. Build App/Executable
echo "[3/3] Building standalone executable..."
bash "$SCRIPT_DIR/appimage/build-executable.sh"

echo ""
echo "=========================================="
echo "  All builds complete!"
echo "  Check: $ROOT_DIR/dist/"
echo "=========================================="
ls -lh "$ROOT_DIR/dist/"
