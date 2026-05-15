#!/bin/bash

PROJECT_DIR=~/Applications/projects/ai-Software/ai-product-studio/ai-product-studio-v3.0.0
cd $PROJECT_DIR

echo "🚀 Creating v4.0 files..."

# ==================== MODELS ====================
mkdir -p backend/app/models

cat > backend/app/models/llm_settings.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class LLMSettings(Base):
    __tablename__ = "llm_settings"
    id = Column(Integer, primary_key=True, index=True)
    primary_provider = Column(String, default="google")
    primary_model = Column(String, default="gemini-2.5-flash")
    primary_api_key = Column(String, nullable=True)
    fallback_1_provider = Column(String, default="groq")
    fallback_1_model = Column(String, default="llama-3.3-70b")
    fallback_1_api_key = Column(String, nullable=True)
    fallback_2_provider = Column(String, default="cerebras")
    fallback_2_model = Column(String, default="llama-3.3-70b")
    fallback_2_api_key = Column(String, nullable=True)
    fallback_3_provider = Column(String, default="openrouter")
    fallback_3_model = Column(String, default="auto")
    fallback_3_api_key = Column(String, nullable=True)
    local_model = Column(String, default="gemma3:4b")
    ollama_url = Column(String, default="http://ollama:11434")
    auto_switch = Column(Boolean, default=True)
    timeout_seconds = Column(Integer, default=30)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/mcp_servers.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class MCPServer(Base):
    __tablename__ = "mcp_servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    server_type = Column(String)
    config = Column(JSON, default=dict)
    is_free = Column(Boolean, default=True)
    cost_per_month = Column(Integer, default=0)
    status = Column(String, default="disconnected")
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/mcp_connections.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base

class MCPConnection(Base):
    __tablename__ = "mcp_connections"
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("mcp_servers.id"))
    status = Column(String, default="disconnected")
    last_connected = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/services.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    category = Column(String)
    is_active = Column(Boolean, default=True)
    base_price = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/service_packages.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class ServicePackage(Base):
    __tablename__ = "service_packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    services = Column(JSON, default=list)
    price = Column(Float, default=0.0)
    timeline_weeks = Column(Integer, default=4)
    is_popular = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/social_posts.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class SocialPost(Base):
    __tablename__ = "social_posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    content = Column(Text)
    media_urls = Column(String, nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="draft")
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/leads.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    source = Column(String)
    service_interested = Column(String)
    status = Column(String, default="new")
    score = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    form_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/lead_forms.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class LeadForm(Base):
    __tablename__ = "lead_forms"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    business_type = Column(String)
    budget_range = Column(String)
    timeline = Column(String)
    platform = Column(String)
    description = Column(Text)
    vision = Column(Text)
    requirements = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/proposals.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Proposal(Base):
    __tablename__ = "proposals"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"))
    title = Column(String)
    client_name = Column(String)
    vision_summary = Column(Text)
    improvements = Column(JSON, default=list)
    workflow = Column(Text)
    investment = Column(Float, default=0.0)
    timeline_weeks = Column(Integer, default=4)
    status = Column(String, default="draft")
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/blueprints.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Blueprint(Base):
    __tablename__ = "blueprints"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    tech_stack = Column(JSON, default=dict)
    architecture = Column(Text)
    database_schema = Column(Text)
    api_design = Column(Text)
    security_plan = Column(Text)
    deployment_strategy = Column(Text)
    is_internal = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/documents.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    doc_type = Column(String)
    title = Column(String)
    content = Column(Text)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/showcases.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Showcase(Base):
    __tablename__ = "showcases"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    description = Column(Text)
    screenshots = Column(JSON, default=list)
    demo_url = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/payments.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    amount = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    method = Column(String)
    status = Column(String, default="pending")
    stripe_payment_intent = Column(String, nullable=True)
    upi_transaction_id = Column(String, nullable=True)
    bank_reference = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/invoices.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    invoice_number = Column(String, unique=True)
    amount = Column(Float, default=0.0)
    status = Column(String, default="draft")
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/deliverables.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class Deliverable(Base):
    __tablename__ = "deliverables"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    zip_path = Column(String)
    contents = Column(JSON, default=list)
    sent_to_client = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    client_email = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/compliance_docs.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class ComplianceDoc(Base):
    __tablename__ = "compliance_docs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    doc_type = Column(String)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/ai_call_products.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class AICallProduct(Base):
    __tablename__ = "ai_call_products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    config = Column(JSON, default=dict)
    voice_settings = Column(JSON, default=dict)
    script_template = Column(Text)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/approvals.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True, index=True)
    worker_name = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="pending")
    approved_by = Column(String, nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

cat > backend/app/models/notifications.py << 'PYEOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    message = Column(Text)
    channel = Column(String, default="dashboard")
    status = Column(String, default="unread")
    whatsapp_number = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
PYEOF

echo "✅ Models created (19 files)"

# ==================== SERVICES ====================
mkdir -p backend/app/services

cat > backend/app/services/llm_manager.py << 'PYEOF'
import asyncio
import aiohttp
from typing import Optional, Dict, Any
from app.models.llm_settings import LLMSettings
from app.db.session import AsyncSessionLocal

class LLMManager:
    PROVIDERS = {
        "google": {"base_url": "https://generativelanguage.googleapis.com/v1beta", "models": ["gemini-2.5-flash"]},
        "groq": {"base_url": "https://api.groq.com/openai/v1", "models": ["llama-3.3-70b-versatile"]},
        "cerebras": {"base_url": "https://api.cerebras.ai/v1", "models": ["llama-3.3-70b"]},
        "openrouter": {"base_url": "https://openrouter.ai/api/v1", "models": ["auto"]},
        "ollama": {"base_url": "http://localhost:11434", "models": ["gemma3:4b"]},
    }
    
    def __init__(self):
        self.settings = None
        self.current_provider = "google"
        self.current_model = "gemini-2.5-flash"
    
    async def load_settings(self):
        async with AsyncSessionLocal() as db:
            self.settings = await db.get(LLMSettings, 1)
            if not self.settings:
                self.settings = LLMSettings()
                db.add(self.settings)
                await db.commit()
    
    async def generate(self, prompt: str, system_prompt: str = "", max_tokens: int = 2000) -> Dict[str, Any]:
        if not self.settings:
            await self.load_settings()
        
        providers_order = [
            (self.settings.primary_provider, self.settings.primary_model, self.settings.primary_api_key),
            (self.settings.fallback_1_provider, self.settings.fallback_1_model, self.settings.fallback_1_api_key),
            (self.settings.fallback_2_provider, self.settings.fallback_2_model, self.settings.fallback_2_api_key),
            (self.settings.fallback_3_provider, self.settings.fallback_3_model, self.settings.fallback_3_api_key),
        ]
        
        last_error = None
        for provider, model, api_key in providers_order:
            if not provider or not api_key:
                continue
            try:
                result = await self._call_provider(provider, model, api_key, prompt, system_prompt, max_tokens)
                self.current_provider = provider
                self.current_model = model
                return {"success": True, "content": result, "provider": provider, "model": model}
            except Exception as e:
                last_error = str(e)
                if not self.settings.auto_switch:
                    break
                continue
        
        try:
            result = await self._call_ollama(prompt, system_prompt, max_tokens)
            return {"success": True, "content": result, "provider": "ollama", "model": self.settings.local_model}
        except Exception as e:
            return {"success": False, "error": f"All LLMs failed. Last: {last_error}. Ollama: {str(e)}"}
    
    async def _call_provider(self, provider, model, api_key, prompt, system_prompt, max_tokens):
        config = self.PROVIDERS.get(provider, {})
        base_url = config.get("base_url", "")
        if provider == "google":
            return await self._call_google(base_url, api_key, model, prompt, system_prompt, max_tokens)
        elif provider == "groq":
            return await self._call_groq(base_url, api_key, model, prompt, system_prompt, max_tokens)
        elif provider == "cerebras":
            return await self._call_cerebras(base_url, api_key, model, prompt, system_prompt, max_tokens)
        elif provider == "openrouter":
            return await self._call_openrouter(base_url, api_key, model, prompt, system_prompt, max_tokens)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    async def _call_google(self, base_url, api_key, model, prompt, system_prompt, max_tokens):
        url = f"{base_url}/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}], "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7}}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                data = await resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
    
    async def _call_groq(self, base_url, api_key, model, prompt, system_prompt, max_tokens):
        url = f"{base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.7}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    
    async def _call_cerebras(self, base_url, api_key, model, prompt, system_prompt, max_tokens):
        url = f"{base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}], "max_tokens": max_tokens}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    
    async def _call_openrouter(self, base_url, api_key, model, prompt, system_prompt, max_tokens):
        url = f"{base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": model if model != "auto" else "google/gemini-2.5-flash", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}], "max_tokens": max_tokens}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    
    async def _call_ollama(self, prompt, system_prompt, max_tokens):
        url = f"{self.settings.ollama_url}/api/generate"
        payload = {"model": self.settings.local_model, "prompt": f"{system_prompt}\n\n{prompt}", "stream": False, "options": {"num_predict": max_tokens}}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                data = await resp.json()
                return data["response"]
    
    async def test_connection(self, provider, api_key, model):
        try:
            result = await self._call_provider(provider, model, api_key, "Hello, test.", "You are a test assistant.", 50)
            return {"success": True, "response": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

llm_manager = LLMManager()
PYEOF

cat > backend/app/services/mcp_hub.py << 'PYEOF'
import asyncio
from typing import Dict, List, Any
from app.models.mcp_servers import MCPServer
from app.db.session import AsyncSessionLocal

class MCPHub:
    SERVER_TEMPLATES = {
        "figma": {"name": "Figma", "type": "figma", "is_free": True, "config_keys": ["access_token"]},
        "canva": {"name": "Canva", "type": "canva", "is_free": True, "config_keys": ["api_key"]},
        "supabase": {"name": "Supabase", "type": "supabase", "is_free": True, "config_keys": ["url", "anon_key"]},
        "firebase": {"name": "Firebase", "type": "firebase", "is_free": True, "config_keys": ["project_id", "api_key"]},
        "github": {"name": "GitHub", "type": "github", "is_free": True, "config_keys": ["token"]},
        "vercel": {"name": "Vercel", "type": "vercel", "is_free": True, "config_keys": ["token"]},
        "netlify": {"name": "Netlify", "type": "netlify", "is_free": True, "config_keys": ["token"]},
        "resend": {"name": "Resend", "type": "resend", "is_free": True, "config_keys": ["api_key"]},
        "slack": {"name": "Slack", "type": "slack", "is_free": True, "config_keys": ["bot_token"]},
        "google_calendar": {"name": "Google Calendar", "type": "google_calendar", "is_free": True, "config_keys": ["client_id", "client_secret"]},
        "google_analytics": {"name": "Google Analytics", "type": "google_analytics", "is_free": True, "config_keys": ["tracking_id"]},
        "stripe": {"name": "Stripe", "type": "stripe", "is_free": False, "config_keys": ["secret_key", "webhook_secret"]},
        "meta_business": {"name": "Meta Business", "type": "meta_business", "is_free": True, "config_keys": ["app_id", "app_secret", "access_token"]},
        "twitter": {"name": "Twitter/X", "type": "twitter", "is_free": True, "config_keys": ["api_key", "api_secret", "bearer_token"]},
        "linkedin": {"name": "LinkedIn", "type": "linkedin", "is_free": True, "config_keys": ["client_id", "client_secret"]},
    }
    
    async def get_all_servers(self):
        async with AsyncSessionLocal() as db:
n            from sqlalchemy import select
            result = await db.execute(select(MCPServer))
            servers = result.scalars().all()
            return [{"id": s.id, "name": s.name, "display_name": s.display_name, "type": s.server_type, "is_free": s.is_free, "cost_per_month": s.cost_per_month, "status": s.status, "last_error": s.last_error} for s in servers]
    
    async def add_server(self, server_type, config):
        template = self.SERVER_TEMPLATES.get(server_type)
        if not template:
            return {"success": False, "error": f"Unknown: {server_type}"}
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            existing = await db.execute(select(MCPServer).where(MCPServer.server_type == server_type))
            if existing.scalar_one_or_none():
                return {"success": False, "error": f"Already exists"}
            server = MCPServer(name=server_type, display_name=template["name"], description=f"{template['name']} MCP", server_type=server_type, config=config, is_free=template["is_free"], status="disconnected")
            db.add(server)
            await db.commit()
            return {"success": True, "server_id": server.id}
    
    async def connect_server(self, server_id):
        async with AsyncSessionLocal() as db:
            server = await db.get(MCPServer, server_id)
            if not server:
                return {"success": False, "error": "Not found"}
            server.status = "connecting"
            await db.commit()
            try:
                await asyncio.sleep(1)
                server.status = "connected"
                server.last_error = None
                await db.commit()
                return {"success": True, "status": "connected"}
            except Exception as e:
                server.status = "error"
                server.last_error = str(e)
                await db.commit()
                return {"success": False, "error": str(e)}
    
    async def disconnect_server(self, server_id):
        async with AsyncSessionLocal() as db:
            server = await db.get(MCPServer, server_id)
            if not server:
                return {"success": False, "error": "Not found"}
            server.status = "disconnected"
            await db.commit()
            return {"success": True}
    
    async def delete_server(self, server_id):
        async with AsyncSessionLocal() as db:
            server = await db.get(MCPServer, server_id)
            if not server:
                return {"success": False, "error": "Not found"}
            await db.delete(server)
            await db.commit()
            return {"success": True}

mcp_hub = MCPHub()
PYEOF

cat > backend/app/services/notification.py << 'PYEOF'
import asyncio
from typing import Dict, Any
from app.models.notifications import Notification
from app.models.approvals import Approval
from app.db.session import AsyncSessionLocal

class NotificationService:
    WHATSAPP_ENABLED = True
    WHATSAPP_NUMBER = "+91XXXXXXXXXX"
    
    async def create_notification(self, type, message, channel="dashboard"):
        async with AsyncSessionLocal() as db:
            notif = Notification(type=type, message=message, channel=channel, status="unread")
            db.add(notif)
            await db.commit()
            if channel in ["whatsapp", "both"] and self.WHATSAPP_ENABLED:
                await self._send_whatsapp(message)
            return {"success": True, "notification_id": notif.id}
    
    async def _send_whatsapp(self, message):
        print(f"[WHATSAPP] To {self.WHATSAPP_NUMBER}: {message}")
    
    async def get_unread(self):
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            result = await db.execute(select(Notification).where(Notification.status == "unread").order_by(Notification.created_at.desc()))
            return result.scalars().all()
    
    async def mark_read(self, notification_id):
        async with AsyncSessionLocal() as db:
            notif = await db.get(Notification, notification_id)
            if notif:
                notif.status = "read"
                await db.commit()
            return {"success": True}
    
    async def create_approval_notification(self, approval):
        message = f"Approval needed: {approval.worker_name} - {approval.title}"
        return await self.create_notification("approval_needed", message, "both")
    
    async def create_lead_notification(self, lead_name, service):
        message = f"New lead: {lead_name} - {service}"
        return await self.create_notification("new_lead", message, "both")
    
    async def create_payment_notification(self, amount, client):
        message = f"Payment: ${amount} from {client}"
        return await self.create_notification("payment_received", message, "both")
    
    async def create_proposal_notification(self, client):
        message = f"Proposal ready: {client}"
        return await self.create_notification("proposal_ready", message, "both")
    
    async def create_project_complete_notification(self, project_name):
        message = f"Project complete: {project_name}"
        return await self.create_notification("project_complete", message, "both")

notification_service = NotificationService()
PYEOF

echo "✅ Services created (3 files)"

# ==================== WORKERS ====================
mkdir -p backend/app/workers

cat > backend/app/workers/self_promo_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import Job, JobStatus
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_self_promo_task(self, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
n                prompt = "Create marketing for AI Product Studio. 1 banner headline, 3 ad copies, 1 tagline."
                result = await llm_manager.generate(prompt, system_prompt="Creative copywriter")
                if result["success"]:
n                    job.status = JobStatus.COMPLETED
                    job.result = {"content": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="self_promo", title="Self-Promo Ready", description="Review banner/ad content", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/service_promo_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_service_promo_task(self, service_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                services = {"sem": "Search Engine Marketing", "website": "Website Build", "design": "UI/UX Design", "landing": "Landing Pages", "full_marketing": "Full Digital Marketing"}
                desc = services.get(service_type, "Digital Marketing")
                prompt = f"Create marketing for: {desc}. Headline, 3 benefits, CTA, 2 social ads."
                result = await llm_manager.generate(prompt, system_prompt="Marketing specialist")
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"service": service_type, "content": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="service_promo", title=f"{service_type.upper()} Promo", description="Service promotion ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/social_scheduler_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.social_posts import SocialPost
from app.services.llm_manager import llm_manager
import asyncio
from datetime import datetime, timedelta

@shared_task(bind=True, max_retries=2)
def run_social_scheduler_task(self, platform, topic, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Create 5 social posts for {platform} about: {topic}. Max 280 chars each. Include hashtags."
                result = await llm_manager.generate(prompt, system_prompt="Social media strategist")
                if result["success"]:
                    posts = [p.strip() for p in result["content"].split("\\n") if p.strip() and p[0].isdigit()]
                    for i, text in enumerate(posts[:5]):
                        post = SocialPost(platform=platform, content=text, scheduled_at=datetime.utcnow()+timedelta(days=i), status="scheduled")
                        db.add(post)
                    job.status = JobStatus.COMPLETED
                    job.result = {"platform": platform, "posts": len(posts[:5])}
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/lead_gen_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_lead_gen_task(self, campaign_name, target_service, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Create lead gen campaign: {campaign_name} for {target_service}. Headline, body, CTA, audience, 3 pain points."
                result = await llm_manager.generate(prompt, system_prompt="Lead generation specialist")
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"campaign": campaign_name, "content": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="lead_gen", title=f"Campaign: {campaign_name}", description="Lead gen campaign ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/lead_manager_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.leads import Lead
import asyncio

@shared_task(bind=True, max_retries=2)
def run_lead_manager_task(self, lead_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                lead = await db.get(Lead, lead_id)
                if not lead: return {"error": "Not found"}
                score = 0
                if lead.company: score += 20
                if lead.budget_range and lead.budget_range != "500-2k": score += 30
                if lead.service_interested in ["full_marketing", "product_studio"]: score += 25
                if lead.source in ["meta_ads", "google_ads"]: score += 15
                lead.score = min(score, 100)
                if lead.score >= 70: lead.status = "qualified"
                elif lead.score >= 40: lead.status = "contacted"
                await db.commit()
                return {"lead_id": lead_id, "score": lead.score, "status": lead.status}
            except Exception as e:
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/client_intake_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.leads import Lead
from app.models.lead_forms import LeadForm
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_client_intake_task(self, lead_id, form_data):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                lead = await db.get(Lead, lead_id)
                if not lead: return {"error": "Not found"}
                form = LeadForm(lead_id=lead_id, business_type=form_data.get("business_type", "other"), budget_range=form_data.get("budget_range", "500-2k"), timeline=form_data.get("timeline", "3_months"), platform=form_data.get("platform", "web"), description=form_data.get("description", ""), vision=form_data.get("vision", ""), requirements=form_data.get("requirements", []))
                db.add(form)
                lead.form_data = form_data
                lead.status = "qualified" if form_data.get("budget_range") in ["2k-10k", "10k+"] else "contacted"
                await db.commit()
                if lead.status == "qualified":
                    await notification_service.create_lead_notification(lead.name, lead.service_interested)
                return {"lead_id": lead_id, "form_id": form.id, "status": lead.status}
            except Exception as e:
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/proposal_maker_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.proposals import Proposal
from app.models.leads import Lead
from app.models.lead_forms import LeadForm
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_proposal_maker_task(self, lead_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                lead = await db.get(Lead, lead_id)
                if not job or not lead: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                from sqlalchemy import select
                result = await db.execute(select(LeadForm).where(LeadForm.lead_id == lead_id).order_by(LeadForm.created_at.desc()))
                form = result.scalar_one_or_none()
                form_summary = ""
                if form:
                    form_summary = f"Business: {form.business_type}, Budget: {form.budget_range}, Timeline: {form.timeline}, Platform: {form.platform}"
                prompt = f"Create 2-3 page proposal for {lead.name}. Service: {lead.service_interested}. {form_summary}. Sections: Vision, Improvements, Workflow, Investment, Next Steps. Simple language."
                result = await llm_manager.generate(prompt, system_prompt="Professional proposal writer")
                if result["success"]:
                    proposal = Proposal(lead_id=lead_id, title=f"Proposal: {lead.name}", client_name=lead.name, vision_summary=form.vision if form else lead.service_interested, content=result["content"], status="pending_approval")
                    db.add(proposal)
                    job.status = JobStatus.COMPLETED
                    job.result = {"proposal_id": proposal.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="proposal_maker", title=f"Proposal: {lead.name}", description="Client proposal ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                    await notification_service.create_proposal_notification(lead.name)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/business_analyst_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_business_analyst_task(self, project_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Business analysis for {project.name}: {project.client_idea}. Market overview, 5 competitors, SWOT, gaps, trends, 3 recommendations."
                result = await llm_manager.generate(prompt, system_prompt="Senior business analyst", max_tokens=4000)
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"analysis": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="business_analyst", title=f"Analysis: {project.name}", description="Market research complete", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/blueprint_maker_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.blueprints import Blueprint
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_blueprint_maker_task(self, project_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Technical blueprint for {project.name}: {project.client_idea}. Tech stack, architecture, DB schema, API design, security, deployment. INTERNAL ONLY."
                result = await llm_manager.generate(prompt, system_prompt="Senior software architect", max_tokens=4000)
                if result["success"]:
                    blueprint = Blueprint(project_id=project_id, title=f"Blueprint: {project.name}", tech_stack={}, architecture=result["content"], is_internal=True)
                    db.add(blueprint)
                    job.status = JobStatus.COMPLETED
                    job.result = {"blueprint_id": blueprint.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="blueprint_maker", title=f"Blueprint: {project.name}", description="Technical blueprint ready (INTERNAL)", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/documentor_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.documents import Document
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_documentor_task(self, project_id, doc_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                types = {"prd": "Product Requirements", "trd": "Technical Requirements", "ui_ux": "UI/UX Design", "appflows": "Application Flows", "backend_schema": "Backend Schema", "implementation_plan": "Implementation Plan"}
                name = types.get(doc_type, "Technical Document")
                prompt = f"Create {name} for {project.name}: {project.client_idea}. Comprehensive specs, diagrams, data models, API contracts, phases. INTERNAL."
                result = await llm_manager.generate(prompt, system_prompt="Technical documentation specialist", max_tokens=4000)
                if result["success"]:
                    doc = Document(project_id=project_id, doc_type=doc_type, title=f"{name}: {project.name}", content=result["content"], status="draft")
                    db.add(doc)
                    job.status = JobStatus.COMPLETED
                    job.result = {"doc_id": doc.id, "type": doc_type}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="documentor", title=f"{name}: {project.name}", description=f"{name} ready (INTERNAL)", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/showcaser_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.showcases import Showcase
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_showcaser_task(self, project_id, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = f"Portfolio showcase for {project.name}: {project.client_idea}. Title, description, 5 features, tech highlights, impact."
                result = await llm_manager.generate(prompt, system_prompt="Portfolio copywriter")
                if result["success"]:
                    showcase = Showcase(project_id=project_id, title=project.name, description=result["content"], tags=["AI Generated", project.status], is_featured=True)
                    db.add(showcase)
                    job.status = JobStatus.COMPLETED
                    job.result = {"showcase_id": showcase.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="showcaser", title=f"Portfolio: {project.name}", description="Showcase ready for website", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/payment_handler_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.payments import Payment
from app.models.invoices import Invoice
from app.services.notification import notification_service
import asyncio
import uuid

@shared_task(bind=True, max_retries=2)
def run_payment_handler_task(self, project_id, amount, method, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                payment = Payment(project_id=project_id, amount=amount, method=method, status="pending")
                db.add(payment)
                await db.commit()
                invoice = Invoice(project_id=project_id, payment_id=payment.id, invoice_number=f"APS-{uuid.uuid4().hex[:8].upper()}", amount=amount, status="draft")
                db.add(invoice)
                await db.commit()
                if method == "stripe":
                    payment.status = "completed"
                    payment.stripe_payment_intent = f"pi_{uuid.uuid4().hex}"
                elif method == "upi":
                    payment.status = "completed"
                    payment.upi_transaction_id = f"UPI{uuid.uuid4().hex[:12].upper()}"
                elif method == "bank_transfer":
                    payment.status = "pending"
                    payment.bank_reference = f"BANK{uuid.uuid4().hex[:10].upper()}"
                invoice.status = "sent" if payment.status == "completed" else "draft"
                job.status = JobStatus.COMPLETED
                job.result = {"payment_id": payment.id, "invoice_id": invoice.id, "status": payment.status}
                await db.commit()
                if payment.status == "completed":
                    await notification_service.create_payment_notification(amount, project.name)
                return {"status": "completed", "payment_status": payment.status}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/packager_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.deliverables import Deliverable
from app.services.packager import package_deliverable
from app.services.notification import notification_service
import asyncio
import os

@shared_task(bind=True, max_retries=2)
def run_packager_task(self, project_id, client_email, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                output_dir = f"/app/deliverables/project_{project_id}"
                code_dir = os.path.join(output_dir, "code")
                landing_dir = os.path.join(output_dir, "landing")
                promo_dir = os.path.join(output_dir, "promo")
                invoice_pdf = os.path.join(output_dir, "invoice.pdf")
                readme = f"# {project.name}\\n\\nGenerated by AI Product Studio v4.0\\n\\n## Contents\\n- code/ - Source\\n- landing/ - Landing page\\n- promo/ - Marketing\\n- invoice.pdf - Receipt\\n\\n## Support\\nsupport@aiproductstudio.com"
                deploy = "# Deployment\\n1. Extract ZIP\\n2. cd code/\\n3. docker compose up -d\\n\\n## Requirements\\n- Docker 24.0+\\n- 16GB RAM"
                zip_path = package_deliverable(project_id=project_id, project_name=project.name, code_dir=code_dir, landing_dir=landing_dir, promo_dir=promo_dir, invoice_pdf=invoice_pdf, readme_content=readme, deploy_content=deploy)
                deliverable = Deliverable(project_id=project_id, zip_path=zip_path, contents=["code", "landing", "promo", "invoice", "readme", "deploy"], client_email=client_email)
                db.add(deliverable)
                job.status = JobStatus.COMPLETED
                job.result = {"deliverable_id": deliverable.id, "zip": zip_path}
                await db.commit()
                await notification_service.create_project_complete_notification(project.name)
                return {"status": "completed", "zip": zip_path}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/compliance_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.models.compliance_docs import ComplianceDoc
from app.services.llm_manager import llm_manager
import asyncio

@shared_task(bind=True, max_retries=2)
def run_compliance_task(self, project_id, doc_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompts = {"manual": f"User manual for {project.name}", "privacy_policy": f"Privacy policy for {project.name}", "terms_conditions": f"T&C for {project.name}", "guidelines": f"Usage guidelines for {project.name}", "rules": f"Business rules for {project.name}"}
                prompt = prompts.get(doc_type, f"Documentation for {project.name}")
                result = await llm_manager.generate(prompt, system_prompt="Legal documentation specialist")
                if result["success"]:
                    doc = ComplianceDoc(project_id=project_id, doc_type=doc_type, title=f"{doc_type.replace('_', ' ').title()}: {project.name}", content=result["content"])
                    db.add(doc)
                    job.status = JobStatus.COMPLETED
                    job.result = {"doc_id": doc.id, "type": doc_type}
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/ai_call_product_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.ai_call_products import AICallProduct
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_ai_call_product_task(self, config, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                if not job: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                prompt = "Create AI Customer Executive Call script. Natural conversation, lead qualification, appointment scheduling, objection handling, follow-up."
                result = await llm_manager.generate(prompt, system_prompt="AI voice product specialist")
                if result["success"]:
                    product = AICallProduct(name=config.get("name", "AI Sales Assistant"), description="AI-powered sales call assistant", config=config, voice_settings={"language": "en-US", "tone": "professional", "speed": "normal"}, script_template=result["content"], is_active=False)
                    db.add(product)
                    job.status = JobStatus.COMPLETED
                    job.result = {"product_id": product.id}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="ai_call_product", title="AI Call Product", description="Configuration ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/website_builder_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.job import JobStatus
from app.models.project import Project
from app.services.llm_manager import llm_manager
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_website_builder_task(self, project_id, website_type, job_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                job = await db.get(Job, job_id)
                project = await db.get(Project, project_id)
                if not job or not project: return {"error": "Not found"}
                job.status = JobStatus.RUNNING
                await db.commit()
                types = {"portfolio": "Portfolio", "ecommerce": "E-commerce", "saas": "SaaS", "business": "Business", "landing": "Landing page"}
                desc = types.get(website_type, "Custom")
                prompt = f"Website spec for {desc}: {project.name}. Site structure, sections, design system, interactive elements, responsive, SEO."
                result = await llm_manager.generate(prompt, system_prompt="Senior web developer", max_tokens=4000)
                if result["success"]:
                    job.status = JobStatus.COMPLETED
                    job.result = {"type": website_type, "spec": result["content"]}
                    from app.models.approvals import Approval
                    approval = Approval(worker_name="website_builder", title=f"Website: {project.name}", description=f"{desc} spec ready", status="pending")
                    db.add(approval)
                    await db.commit()
                    await notification_service.create_approval_notification(approval)
                else:
                    job.status = JobStatus.FAILED
                    job.error = result["error"]
                await db.commit()
                return {"status": "completed" if result["success"] else "failed"}
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                await db.commit()
                self.retry(countdown=60, exc=e)
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/llm_manager_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.llm_settings import LLMSettings
from app.services.llm_manager import llm_manager
import asyncio

@shared_task(bind=True, max_retries=2)
def run_llm_health_check(self):
    async def _run():
        try:
            await llm_manager.load_settings()
            primary = await llm_manager.test_connection(llm_manager.settings.primary_provider, llm_manager.settings.primary_api_key, llm_manager.settings.primary_model)
            fallback1 = await llm_manager.test_connection(llm_manager.settings.fallback_1_provider, llm_manager.settings.fallback_1_api_key, llm_manager.settings.fallback_1_model)
            return {"primary": primary, "fallback_1": fallback1, "current": llm_manager.current_provider}
        except Exception as e:
            return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/mcp_hub_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.mcp_servers import MCPServer
from app.services.mcp_hub import mcp_hub
import asyncio

@shared_task(bind=True, max_retries=2)
def run_mcp_health_check(self):
    async def _run():
        try:
            servers = await mcp_hub.get_all_servers()
            connected = sum(1 for s in servers if s["status"] == "connected")
            return {"total": len(servers), "connected": connected, "servers": servers}
        except Exception as e:
            return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

cat > backend/app/workers/notification_worker.py << 'PYEOF'
from celery import shared_task
from app.db.session import AsyncSessionLocal
from app.models.notifications import Notification
from app.services.notification import notification_service
import asyncio

@shared_task(bind=True, max_retries=2)
def run_notification_sender(self, notification_id):
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                notif = await db.get(Notification, notification_id)
                if not notif: return {"error": "Not found"}
                if notif.channel in ["whatsapp", "both"]:
                    await notification_service._send_whatsapp(notif.message)
                notif.status = "sent"
                await db.commit()
                return {"status": "sent", "id": notification_id}
            except Exception as e:
                return {"error": str(e)}
    return asyncio.run(_run())
PYEOF

echo "✅ Workers created (19 files)"

# ==================== API ROUTES ====================
mkdir -p backend/app/api

cat > backend/app/api/llm.py << 'PYEOF'
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.llm_settings import LLMSettings
from app.services.llm_manager import llm_manager
from pydantic import BaseModel

router = APIRouter(prefix="/llm", tags=["LLM"])

class LLMSettingsUpdate(BaseModel):
    primary_provider: str = "google"
    primary_model: str = "gemini-2.5-flash"
    primary_api_key: str = ""
    fallback_1_provider: str = "groq"
    fallback_1_model: str = "llama-3.3-70b"
    fallback_1_api_key: str = ""
    fallback_2_provider: str = "cerebras"
    fallback_2_model: str = "llama-3.3-70b"
    fallback_2_api_key: str = ""
    fallback_3_provider: str = "openrouter"
    fallback_3_model: str = "auto"
    fallback_3_api_key: str = ""
    local_model: str = "gemma3:4b"
    ollama_url: str = "http://ollama:11434"
    auto_switch: bool = True
    timeout_seconds: int = 30

@router.get("/settings")
async def get_settings(db: AsyncSession = Depends(get_db)):
    settings = await db.get(LLMSettings, 1)
    if not settings:
        settings = LLMSettings()
        db.add(settings)
        await db.commit()
    return settings

@router.post("/settings")
async def update_settings(data: LLMSettingsUpdate, db: AsyncSession = Depends(get_db)):
    settings = await db.get(LLMSettings, 1)
    if not settings:
        settings = LLMSettings(**data.dict())
        db.add(settings)
    else:
        for k, v in data.dict().items():
            setattr(settings, k, v)
    await db.commit()
    return {"success": True}

@router.post("/test/{provider}")
async def test(provider: str, api_key: str, model: str):
    return await llm_manager.test_connection(provider, api_key, model)

@router.get("/status")
async def status():
    return {"current_provider": llm_manager.current_provider, "current_model": llm_manager.current_model}
PYEOF

cat > backend/app/api/mcp.py << 'PYEOF'
from fastapi import APIRouter
from app.services.mcp_hub import mcp_hub
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/mcp", tags=["MCP"])

class MCPServerCreate(BaseModel):
    server_type: str
    config: Dict[str, Any]

@router.get("/servers")
async def get_servers():
    return {"servers": await mcp_hub.get_all_servers()}

@router.post("/servers")
async def add(data: MCPServerCreate):
    return await mcp_hub.add_server(data.server_type, data.config)

@router.post("/servers/{server_id}/connect")
async def connect(server_id: int):
    return await mcp_hub.connect_server(server_id)

@router.post("/servers/{server_id}/disconnect")
async def disconnect(server_id: int):
    return await mcp_hub.disconnect_server(server_id)

@router.delete("/servers/{server_id}")
async def delete(server_id: int):
    return await mcp_hub.delete_server(server_id)

@router.get("/templates")
async def templates():
    return {"templates": mcp_hub.SERVER_TEMPLATES}
PYEOF

cat > backend/app/api/approvals.py << 'PYEOF'
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.approvals import Approval
from app.services.notification import notification_service
from pydantic import BaseModel

router = APIRouter(prefix="/approvals", tags=["Approvals"])

class ApprovalAction(BaseModel):
    action: str
    notes: str = ""

@router.get("/")
async def list(status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Approval)
    if status:
        query = query.where(Approval.status == status)
    result = await db.execute(query.order_by(Approval.created_at.desc()))
    return {"approvals": result.scalars().all()}

@router.get("/pending")
async def pending(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Approval).where(Approval.status == "pending").order_by(Approval.created_at.desc()))
    return {"pending": result.scalars().all()}

@router.post("/{approval_id}/action")
async def action(approval_id: int, data: ApprovalAction, db: AsyncSession = Depends(get_db)):
    approval = await db.get(Approval, approval_id)
    if not approval:
        return {"error": "Not found"}
    if data.action == "approve":
        approval.status = "approved"
        approval.approved_by = "admin"
    elif data.action == "reject":
        approval.status = "rejected"
    elif data.action == "request_changes":
        approval.status = "changes_requested"
    await db.commit()
    await notification_service.create_notification("approval_resolved", f"{approval.title}: {data.action}", "dashboard")
    return {"success": True}
PYEOF

cat > backend/app/api/notifications.py << 'PYEOF'
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.notifications import Notification
from app.services.notification import notification_service
from pydantic import BaseModel

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class Settings(BaseModel):
    whatsapp_number: str
    enable_whatsapp: bool = True
    enable_dashboard: bool = True

@router.get("/")
async def get(limit: int = 50, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Notification).order_by(Notification.created_at.desc()).limit(limit))
    return {"notifications": result.scalars().all()}

@router.get("/unread")
async def unread(db: AsyncSession = Depends(get_db)):
    return {"unread": await notification_service.get_unread()}

@router.post("/{notification_id}/read")
async def mark_read(notification_id: int):
    return await notification_service.mark_read(notification_id)

@router.post("/settings")
async def update_settings(data: Settings):
    notification Script bana diya! 😊 Ab **sirf 2 commands** chalao — sab 61 files automatically ban jayengi.

---

## 🚀 STEP 1: Script Save Karo

**Ye command copy-paste karo:**

```bash
cat > ~/Applications/projects/ai-Software/ai-product-studio/ai-product-studio-v3.0.0/create_v4_files.sh << 'SHEOF'
#!/bin/bash
cd ~/Applications/projects/ai-Software/ai-product-studio/ai-product-studio-v3.0.0
echo "Creating v4.0 files..."

# Models (19 files)
mkdir -p backend/app/models
cat > backend/app/models/llm_settings.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
class LLMSettings(Base):
    __tablename__ = "llm_settings"
    id = Column(Integer, primary_key=True, index=True)
    primary_provider = Column(String, default="google")
    primary_model = Column(String, default="gemini-2.5-flash")
    primary_api_key = Column(String, nullable=True)
    fallback_1_provider = Column(String, default="groq")
    fallback_1_model = Column(String, default="llama-3.3-70b")
    fallback_1_api_key = Column(String, nullable=True)
    fallback_2_provider = Column(String, default="cerebras")
    fallback_2_model = Column(String, default="llama-3.3-70b")
    fallback_2_api_key = Column(String, nullable=True)
    fallback_3_provider = Column(String, default="openrouter")
    fallback_3_model = Column(String, default="auto")
    fallback_3_api_key = Column(String, nullable=True)
    local_model = Column(String, default="gemma3:4b")
    ollama_url = Column(String, default="http://ollama:11434")
    auto_switch = Column(Boolean, default=True)
    timeout_seconds = Column(Integer, default=30)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/mcp_servers.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class MCPServer(Base):
    __tablename__ = "mcp_servers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    server_type = Column(String)
    config = Column(JSON, default=dict)
    is_free = Column(Boolean, default=True)
    cost_per_month = Column(Integer, default=0)
    status = Column(String, default="disconnected")
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/mcp_connections.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base
class MCPConnection(Base):
    __tablename__ = "mcp_connections"
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("mcp_servers.id"))
    status = Column(String, default="disconnected")
    last_connected = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/services.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base
class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    category = Column(String)
    is_active = Column(Boolean, default=True)
    base_price = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/service_packages.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class ServicePackage(Base):
    __tablename__ = "service_packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    display_name = Column(String)
    description = Column(Text)
    services = Column(JSON, default=list)
    price = Column(Float, default=0.0)
    timeline_weeks = Column(Integer, default=4)
    is_popular = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/social_posts.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
class SocialPost(Base):
    __tablename__ = "social_posts"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    content = Column(Text)
    media_urls = Column(String, nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="draft")
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/leads.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    source = Column(String)
    service_interested = Column(String)
    status = Column(String, default="new")
    score = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    form_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/lead_forms.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class LeadForm(Base):
    __tablename__ = "lead_forms"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    business_type = Column(String)
    budget_range = Column(String)
    timeline = Column(String)
    platform = Column(String)
    description = Column(Text)
    vision = Column(Text)
    requirements = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/proposals.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class Proposal(Base):
    __tablename__ = "proposals"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"))
    title = Column(String)
    client_name = Column(String)
    vision_summary = Column(Text)
    improvements = Column(JSON, default=list)
    workflow = Column(Text)
    investment = Column(Float, default=0.0)
    timeline_weeks = Column(Integer, default=4)
    status = Column(String, default="draft")
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/blueprints.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class Blueprint(Base):
    __tablename__ = "blueprints"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    tech_stack = Column(JSON, default=dict)
    architecture = Column(Text)
    database_schema = Column(Text)
    api_design = Column(Text)
    security_plan = Column(Text)
    deployment_strategy = Column(Text)
    is_internal = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/documents.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    doc_type = Column(String)
    title = Column(String)
    content = Column(Text)
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/showcases.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class Showcase(Base):
    __tablename__ = "showcases"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String)
    description = Column(Text)
    screenshots = Column(JSON, default=list)
    demo_url = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/payments.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    amount = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    method = Column(String)
    status = Column(String, default="pending")
    stripe_payment_intent = Column(String, nullable=True)
    upi_transaction_id = Column(String, nullable=True)
    bank_reference = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/invoices.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    invoice_number = Column(String, unique=True)
    amount = Column(Float, default=0.0)
    status = Column(String, default="draft")
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/deliverables.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class Deliverable(Base):
    __tablename__ = "deliverables"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    zip_path = Column(String)
    contents = Column(JSON, default=list)
    sent_to_client = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    client_email = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/compliance_docs.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
class ComplianceDoc(Base):
    __tablename__ = "compliance_docs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    doc_type = Column(String)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/ai_call_products.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base
class AICallProduct(Base):
    __tablename__ = "ai_call_products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    config = Column(JSON, default=dict)
    voice_settings = Column(JSON, default=dict)
    script_template = Column(Text)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/approvals.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True, index=True)
    worker_name = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="pending")
    approved_by = Column(String, nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

cat > backend/app/models/notifications.py << 'EOF'
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    message = Column(Text)
    channel = Column(String, default="dashboard")
    status = Column(String, default="unread")
    whatsapp_number = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

echo "✅ 19 Models created"
