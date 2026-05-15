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
