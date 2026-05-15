import os
import hmac
import hashlib
import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.config import settings

router = APIRouter(prefix="/download", tags=["download"])


def _generate_token(project_id: int, expiry: int) -> str:
    msg = f"{project_id}:{expiry}".encode()
    sig = hmac.new(settings.DELIVERY_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    return f"{project_id}:{expiry}:{sig}"


def _verify_token(token: str) -> int:
    try:
        project_id_str, expiry_str, sig = token.split(":")
        project_id = int(project_id_str)
        expiry = int(expiry_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token format")

    if time.time() > expiry:
        raise HTTPException(status_code=410, detail="Token expired")

    expected = _generate_token(project_id, expiry)
    if not hmac.compare_digest(expected, token):
        raise HTTPException(status_code=403, detail="Invalid token")

    return project_id


@router.get("/{token}")
async def download_deliverable(token: str):
    project_id = _verify_token(token)

    zip_path = f"/app/deliverables/project_{project_id}/deliverable.zip"
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Deliverable not found")

    return FileResponse(
        path=zip_path,
        filename=f"project_{project_id}_deliverable.zip",
        media_type="application/zip",
    )


@router.get("/token/{project_id}")
async def get_download_token(project_id: int):
    expiry = int(time.time()) + 3600
    token = _generate_token(project_id, expiry)
    return {"token": token, "expires_at": expiry}
