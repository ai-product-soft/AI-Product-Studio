# AI Product Studio v3.0

> My Personal AI-Powered Business Software or Factory** — Idea se leke Revenue tak, sab kuch automatically.

---

## Ye kya hai? (What is this?)

AI Product Studio ek **private automation tool** hai jo aapke liye poora business build karta hai:

1. **Client idea** aata hai → Aap system me daalte ho
2. **AI Research** karta hai market, competitors, opportunity
3. **AI Plan** banata hai — tech stack, phases, monetization
4. **AI Code** generate karta hai — poora working application
5. **AI Landing Page** banata hai — sales ke liye
6. **AI Ads & Content** banata hai — Google, Facebook, Blog, Social
7. **AI Sales Setup** karta hai — Stripe payment link + Invoice PDF
8. **ZIP Package** ready — Client ko deliver karo

**Sab kuch aapke apne server pe chalta hai. Koi bhi data bahar nahi jaata.**

---

## Not for All but its products and services can be usable for public.

- **Freelancers** jo client projects fast deliver karna chahte hain
- **Agencies** jo AI se apna kaam 10x fast karna chahte hain
- **Solopreneurs** jo ek complete product studio run karna chahte hain
- **Developers** jo boilerplate code automatically generate karwana chahte hain

---

## Tech Stack (Kya-kya use hua hai)

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI (Python 3.11), Pydantic v2, SQLAlchemy |
| **Database** | PostgreSQL + pgvector (AI embeddings ke liye) |
| **Queue** | Redis + Celery Workers |
| **AI Brain** | Ollama (Mistral 7B Q4, nomic-embed-text) |
| **Scraper** | Playwright (Chromium) |
| **Payments** | Stripe API |
| **PDF** | ReportLab |
| **Security** | Fernet Encryption |
| **Packaging** | Docker Compose |

---

## Quick Start — Pehli baar setup karna

### Step 1: Docker install karo
```bash
# Ubuntu/Debian pe
sudo apt update
sudo apt install docker.io docker-compose-plugin
sudo usermod -aG docker $USER
# Logout + Login karo ya system restart karo
```

### Step 2: Project clone karo
```bash
git clone https://github.com/YOURNAME/ai-product-studio.git
cd ai-product-studio
```

### Step 3: Environment setup karo
```bash
cp .env.example .env
# .env file me apni values daalo (Stripe key, etc.)
```

### Step 4: Sab services start karo
```bash
docker compose up -d
```

### Step 5: Database ready karo
```bash
docker compose exec backend alembic upgrade head
```

### Step 6: AI Models download karo
```bash
docker compose exec ollama ollama pull mistral:7b-instruct-v0.2-q4_K_M
docker compose exec ollama ollama pull nomic-embed-text
```

### Step 7: Dashboard open karo
```
http://localhost:5173
```

**API Docs:** `http://localhost:8000/docs`

---

## Kaise use karte hain? (How to use)

### 1. Naya Project banana
- Dashboard pe **"New Project"** button click karo
- Project name daalo (jaise "AI Resume Builder")
- Client ka idea / requirements likho
- **Create** karo

### 2. Research chalao
- Project detail page pe **"Research"** button click karo
- AI Google search karega, competitors dhundhega
- 2-3 minute me **Research Brief** ready
- Opportunity score, competitors, key insights milega

### 3. Plan generate karo
- **"Plan"** button click karo
- AI tech stack suggest karega
- Phases aur tasks bataega
- Monetization strategy dega

### 4. Code generate karo
- **"Generate"** button click karo
- AI poora application code likhega
- File-by-file generate hoga
- Auto-validation hoga (syntax check)
- 30-45 minute me ready

### 5. Promotion chalao
- **"Promote"** button click karo
- Google Ads copy banega
- Facebook Ads copy banega
- SEO Blog post banega
- Social media posts banenge

### 6. Sales setup karo
- **"Sales"** button click karo
- Stripe payment link banega
- Invoice PDF generate hoga
- Sab kuch ZIP me package hoga

### 7. Download karo
- **"Download ZIP"** button click karo
- Client ko deliver karo
- Ya directly Stripe link se payment lo

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| CPU | 4 cores | 8 cores |
| Disk | 50 GB | 100 GB |
| OS | Ubuntu 22.04+ | Ubuntu 24.04 LTS |
| GPU | Optional | NVIDIA (fast inference) |

---

## Services kya-kya chalte hain?

| Service | Port | Kaam |
|---------|------|------|
| Frontend (React) | 5173 | Dashboard UI |
| Backend (FastAPI) | 8000 | API + Business Logic |
| Worker (Celery) | — | Background jobs |
| Database (PostgreSQL) | 5432 | Data storage |
| Vector DB (pgvector) | 5432 | AI embeddings |
| Queue (Redis) | 6379 | Job queue |
| AI (Ollama) | 11434 | LLM inference |

---

## Packaging Options (Distribution ke liye)

### 1. Debian Package (.deb)
```bash
cd packaging
./build-all.sh
# Output: dist/ai-product-studio_3.0.0_amd64.deb

sudo dpkg -i dist/ai-product-studio_3.0.0_amd64.deb
sudo apt-get install -f
ai-product-studio start
```

### 2. Tar.xz Archive
```bash
# dist/ai-product-studio-3.0.0.tar.xz
tar -xJf ai-product-studio-3.0.0.tar.xz
cd ai-product-studio-3.0.0
./install.sh
docker compose up -d
```

### 3. Standalone Executable
```bash
# dist/ai-product-studio-3.0.0-x86_64
chmod +x ai-product-studio-3.0.0-x86_64
./ai-product-studio-3.0.0-x86_64 start
```

---

## Commands Reference

```bash
# Sab services start/stop
docker compose up -d
docker compose down

# Logs dekhna
docker compose logs -f backend
docker compose logs -f worker

# Database migrate
docker compose exec backend alembic upgrade head

# New migration banani hai
docker compose exec backend alembic revision --autogenerate -m "description"

# Worker scale karna (3 workers)
docker compose up -d --scale worker=3

# Ollama models check karo
docker compose exec ollama ollama list

# Backend shell me jaana
docker compose exec backend bash

# Database backup
docker compose exec db pg_dump -U aps_user ai_product_studio > backup.sql
```

---

## Project Structure

```
ai-product-studio/
├── docker-compose.yml          # Sab services ka config
├── .env.example               # Environment variables template
├── .env                       # Aapki actual settings (gitignore me)
│
├── backend/                   # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py           # FastAPI app entry
│   │   ├── config.py         # Settings management
│   │   ├── api/              # REST API routes
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic validation
│   │   ├── services/         # Business logic
│   │   ├── prompts/          # AI prompts
│   │   └── workers/          # Celery background tasks
│   ├── alembic/              # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                  # React Dashboard
│   ├── src/
│   │   ├── pages/            # Dashboard, NewProject, ProjectDetail
│   │   ├── components/       # UI components (shadcn/ui)
│   │   ├── services/         # API calls
│   │   └── lib/              # Utilities
│   ├── Dockerfile
│   └── package.json
│
├── packaging/                 # Distribution builders
│   ├── deb/                  # .deb package
│   ├── tar/                  # .tar.xz archive
│   └── appimage/             # Standalone executable
│
└── deliverables/              # Generated client packages (gitignored)
```

---

## Security & Privacy

- **100% Local**: Sab kuch aapke server pe — koi cloud API nahi
- **Encryption**: Client data Fernet encryption se protected
- **Secure Downloads**: ZIP files HMAC-signed token se protected (1 hour expiry)
- **No Data Leak**: Client ideas, research, code — kuch bahar nahi jaata

---

## Troubleshooting

### Problem: Frontend "Connection Failed" dikha raha hai
**Solution:** Backend check karo — `docker compose ps` se status dekho

### Problem: AI slow hai / timeout aa raha hai
**Solution:** 
- RAM check karo — minimum 8GB chahiye
- Swap space add karo
- Model chhota use karo: `mistral:7b-instruct-v0.2-q4_0`

### Problem: Playwright scraping fail ho rahi hai
**Solution:** 
- `docker compose exec backend playwright install chromium`
- Internet connectivity check karo

### Problem: Database connection error
**Solution:**
- `docker compose ps` — db healthy hai?
- `.env` me DATABASE_URL check karo

---

## License

Private Use License — Ye aapka personal tool hai. Resell nahi karna.

---

## Support

Koi problem ho to:
1. `docker compose logs` check karo
2. API docs: `http://localhost:8000/docs`
3. Health check: `http://localhost:8000/api/v1/health`

---

**Built with AI Product Studio v3.0** | Private Cloud | 100% Local Intelligence
