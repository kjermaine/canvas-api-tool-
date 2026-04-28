import os

from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.services.canvas_service import CanvasService
from app.providers.canvas_client import CanvasClient
from app.repositories.canvas_token_repository import CanvasTokenRepository
from app.repositories.canvas_alias_repository import CanvasAliasRepository
from app.services.canvas_reference_resolver import CanvasReferenceResolver
from app.services.export_service import ExportService


def get_auth_service() -> AuthService:
    return AuthService()


def get_canvas_service() -> CanvasService:
    token_repo = CanvasTokenRepository()
    token_record = token_repo.get_token("default")

    if token_record:
        canvas_base_url = token_record["canvas_base_url"]
        access_token = token_record["access_token"]
    else:
        canvas_base_url = os.getenv("CANVAS_BASE_URL")
        access_token = os.getenv("CANVAS_ACCESS_TOKEN")

    if not canvas_base_url or not access_token:
        raise HTTPException(
            status_code=400,
            detail="Canvas credentials missing. Use POST /canvas/config or set CANVAS_BASE_URL and CANVAS_ACCESS_TOKEN.",
        )

    alias_repo = CanvasAliasRepository()
    resolver = CanvasReferenceResolver(alias_repository=alias_repo)

    client = CanvasClient(
        base_url=canvas_base_url,
        access_token=access_token,
    )

    return CanvasService(
        canvas_client=client,
        alias_repository=alias_repo,
        reference_resolver=resolver,
        export_service=ExportService(),
    )