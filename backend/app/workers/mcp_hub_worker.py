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
