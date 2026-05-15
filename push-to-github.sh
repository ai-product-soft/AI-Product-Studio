#!/bin/bash
set -e

REPO_URL="${1:-}"
if [ -z "$REPO_URL" ]; then
    echo "Usage: ./push-to-github.sh https://github.com/username/repo.git"
    exit 1
fi

echo "=========================================="
echo "  Preparing AI Product Studio for GitHub"
echo "=========================================="

# Initialize fresh repo (purges old history if any)
rm -rf .git
git init
git branch -M main

# Create proper .gitignore
cat > .gitignore <<'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Environment
.env
.env.local

# Build outputs
dist/
build/
*.egg-info/

# Deliverables (generated client data)
deliverables/*
!deliverables/.gitkeep

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF

touch deliverables/.gitkeep

# Add all files
git add .

# Commit
git commit -m "feat: AI Product Studio v3.0.0
- Full automation platform (idea → revenue)
- FastAPI backend with PostgreSQL + pgvector
- React + Vite + shadcn/ui frontend
- Ollama LLM integration (Mistral 7B, nomic-embed)
- Celery workers with Redis
- Playwright web scraping
- Stripe payments + PDF invoices
- Debian, tar.xz, and executable packaging"

# Add remote and push
git remote add origin "$REPO_URL"
git push -u origin main --force

echo ""
echo "=========================================="
echo "  Successfully pushed to GitHub!"
echo "  $REPO_URL"
echo "=========================================="
