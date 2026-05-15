import asyncio
from typing import Dict, List, Any
from app.models.mcp_servers import MCPServer
from app.db.session import AsyncSessionLocal

class MCPHub:
    SERVER_TEMPLATES = {
        "figma": {"name": "Figma", "type": "figma", "is_free": True, "config_keys": ["access_token"]},
        "canva": {"name": "Canva", "type": "canva", "is_free": True, "config_keys": ["api_key"]},
        "github": {"name": "GitHub", "type": "github", "is_free": True, "config_keys": ["token"]},
        "stripe": {"name": "Stripe", "type": "stripe", "is_free": False, "config_keys": ["secret_key"]},
    }

    async def get_all_servers(self):
        async with AsyncSessionLocal() as db:
            from sqlalchemy import select
            result = await db.execute(select(MCPServer))
            servers = result.scalars().all()
            return [{"id": s.id, "name": s.name, "display_name": s.display_name, "type": s.server_type, "is_free": s.is_free, "status": s.status} for s in servers]

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
