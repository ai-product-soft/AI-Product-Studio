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
