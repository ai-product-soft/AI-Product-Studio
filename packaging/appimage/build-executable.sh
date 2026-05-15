#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
VERSION="3.0.0"
APP_NAME="ai-product-studio"

echo "Building standalone executable (self-extracting Docker launcher)..."

mkdir -p "$ROOT_DIR/dist"

# This creates a single executable script that embeds the docker-compose.yml
# and extracts/runs it. It's not a true AppImage but acts as a portable "app exe"
# for a Docker-based application.

EXE_PATH="$ROOT_DIR/dist/${APP_NAME}-${VERSION}-x86_64"

cat > "$EXE_PATH" <<'SELFEXTRACT'
#!/bin/bash
set -e

# AI Product Studio Self-Extracting Launcher
VERSION="3.0.0"
APP_DIR="${HOME}/.local/share/ai-product-studio"
COMPOSE_FILE="$APP_DIR/docker-compose.yml"

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "ERROR: Docker is required but not installed."
        echo "Install: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
}

extract_embedded() {
    mkdir -p "$APP_DIR"

    # Extract embedded docker-compose.yml from this script
    # Everything after '#EMBED_START' is the compose file
    sed -n '/^#EMBED_START$/,$p' "$0" | tail -n +2 > "$COMPOSE_FILE"

    # Create minimal .env if not exists
    if [ ! -f "$APP_DIR/.env" ]; then
        cat > "$APP_DIR/.env" <<EOF
POSTGRES_USER=aps_user
POSTGRES_PASSWORD=aps_password
POSTGRES_DB=ai_product_studio
DATABASE_URL=postgresql+psycopg2://aps_user:aps_password@db:5432/ai_product_studio
REDIS_PASSWORD=redis_password
REDIS_URL=redis://:redis_password@redis:6379/0
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b-instruct-v0.2-q4_K_M
EMBED_MODEL=nomic-embed-text
STRIPE_API_KEY=sk_test_your_key_here
DELIVERY_SECRET=change-me-in-production
ENCRYPTION_KEY=your-32-byte-base64-fernet-key=
EOF
    fi
}

run_app() {
    cd "$APP_DIR"
    export COMPOSE_PROJECT_NAME=aistudio

    case "$1" in
        start|"")
            docker compose -f "$COMPOSE_FILE" up -d
            echo ""
            echo "=========================================="
            echo "  AI Product Studio v${VERSION} is running!"
            echo "=========================================="
            echo "  Dashboard: http://localhost:5173"
            echo "  API:      http://localhost:8000"
            echo "  Docs:     http://localhost:8000/docs"
            echo ""
            echo "  First time? Pull models:"
            echo "    $0 pull-models"
            echo ""
            ;;
        stop)
            docker compose -f "$COMPOSE_FILE" down
            echo "Stopped."
            ;;
        restart)
            docker compose -f "$COMPOSE_FILE" down
            docker compose -f "$COMPOSE_FILE" up -d
            ;;
        status)
            docker compose -f "$COMPOSE_FILE" ps
            ;;
        logs)
            docker compose -f "$COMPOSE_FILE" logs -f "${2:-backend}"
            ;;
        pull-models)
            docker compose -f "$COMPOSE_FILE" exec ollama ollama pull mistral:7b-instruct-v0.2-q4_K_M
            docker compose -f "$COMPOSE_FILE" exec ollama ollama pull nomic-embed-text
            echo "Models pulled."
            ;;
        migrate)
            docker compose -f "$COMPOSE_FILE" exec backend alembic upgrade head
            echo "Migrations complete."
            ;;
        update)
            docker compose -f "$COMPOSE_FILE" pull
            docker compose -f "$COMPOSE_FILE" up -d
            ;;
        uninstall)
            docker compose -f "$COMPOSE_FILE" down --volumes --remove-orphans
            rm -rf "$APP_DIR"
            echo "Uninstalled. Remove this script manually if desired."
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|logs|pull-models|migrate|update|uninstall}"
            exit 1
            ;;
    esac
}

main() {
    check_docker
    extract_embedded
    run_app "$@"
    exit 0
}

main "$@"
SELFEXTRACT

# Now append the embedded docker-compose.yml
echo "#EMBED_START" >> "$EXE_PATH"
cat "$ROOT_DIR/docker-compose.yml" >> "$EXE_PATH"

chmod +x "$EXE_PATH"

echo ""
echo "Standalone executable built: dist/$(basename "$EXE_PATH")"
echo ""
echo "Usage:"
echo "  ./$(basename "$EXE_PATH") start       # Start all services"
echo "  ./$(basename "$EXE_PATH") stop        # Stop"
echo "  ./$(basename "$EXE_PATH") pull-models # Download Ollama models"
echo ""
echo "This is a self-contained Docker launcher. It extracts config to:"
echo "  ~/.local/share/ai-product-studio/"
