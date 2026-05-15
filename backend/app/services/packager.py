import os
import zipfile
import json
from typing import Optional

from app.config import settings
from cryptography.fernet import Fernet


def get_fernet() -> Fernet:
    key = settings.ENCRYPTION_KEY.encode() if isinstance(settings.ENCRYPTION_KEY, str) else settings.ENCRYPTION_KEY
    return Fernet(key)


def encrypt_sensitive_data(data: str) -> str:
    f = get_fernet()
    return f.encrypt(data.encode()).decode()


def decrypt_sensitive_data(token: str) -> str:
    f = get_fernet()
    return f.decrypt(token.encode()).decode()


def package_deliverable(
    project_id: int,
    project_name: str,
    code_dir: str,
    landing_dir: str,
    promo_dir: str,
    invoice_pdf: Optional[str],
    readme_content: str,
    deploy_content: str,
) -> str:
    project_dir = f"/app/deliverables/project_{project_id}"
    os.makedirs(project_dir, exist_ok=True)

    zip_path = os.path.join(project_dir, "deliverable.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if os.path.exists(code_dir):
            for root, dirs, files in os.walk(code_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=project_dir)
                    zf.write(file_path, arcname)

        if os.path.exists(landing_dir):
            for root, dirs, files in os.walk(landing_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=project_dir)
                    zf.write(file_path, arcname)

        if os.path.exists(promo_dir):
            for root, dirs, files in os.walk(promo_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=project_dir)
                    zf.write(file_path, arcname)

        if invoice_pdf and os.path.exists(invoice_pdf):
            zf.write(invoice_pdf, "invoice.pdf")

        zf.writestr("README.md", readme_content)
        zf.writestr("DEPLOY.md", deploy_content)

        manifest = {
            "project_id": project_id,
            "project_name": project_name,
            "contents": {
                "code": os.path.exists(code_dir),
                "landing": os.path.exists(landing_dir),
                "promo": os.path.exists(promo_dir),
                "invoice": invoice_pdf is not None,
            },
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))

    return zip_path
