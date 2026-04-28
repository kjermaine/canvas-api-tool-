from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from app.api.dependencies import get_canvas_service
from app.repositories.canvas_token_repository import CanvasTokenRepository
from app.services.canvas_service import CanvasService


router = APIRouter(prefix="/canvas", tags=["canvas"])


class CanvasTokenConfigRequest(BaseModel):
    canvas_base_url: str
    access_token: str
    profile_key: str = "default"


class CanvasAliasRequest(BaseModel):
    alias: str
    entity_type: str = "course"
    canvas_id: int
    display_name: str


@router.post("/config")
def save_canvas_config(payload: CanvasTokenConfigRequest):
    repo = CanvasTokenRepository()
    repo.save_token(
        profile_key=payload.profile_key,
        canvas_base_url=payload.canvas_base_url,
        access_token=payload.access_token,
    )

    return {
        "status": "saved",
        "profile_key": payload.profile_key,
    }


@router.get("/courses")
def get_courses(service: CanvasService = Depends(get_canvas_service)):
    return service.get_courses()


@router.post("/sync-aliases")
def sync_aliases(service: CanvasService = Depends(get_canvas_service)):
    return service.sync_aliases()


@router.get("/aliases")
def get_aliases(service: CanvasService = Depends(get_canvas_service)):
    return service.get_aliases()


@router.post("/aliases")
def save_alias(
    payload: CanvasAliasRequest,
    service: CanvasService = Depends(get_canvas_service),
):
    return service.save_alias(
        alias=payload.alias,
        entity_type=payload.entity_type,
        canvas_id=payload.canvas_id,
        display_name=payload.display_name,
    )


@router.get("/courses/{course_ref}/modules")
def get_modules(
    course_ref: str,
    service: CanvasService = Depends(get_canvas_service),
):
    return service.get_modules(course_ref)


@router.get("/courses/{course_ref}/assignments")
def get_assignments(
    course_ref: str,
    service: CanvasService = Depends(get_canvas_service),
):
    return service.get_assignments(course_ref)


@router.get("/courses/{course_ref}/calendar")
def get_calendar(
    course_ref: str,
    service: CanvasService = Depends(get_canvas_service),
):
    return service.get_calendar(course_ref)


@router.get("/courses/{course_ref}/modules/markdown", response_class=PlainTextResponse)
def get_modules_markdown(
    course_ref: str,
    service: CanvasService = Depends(get_canvas_service),
):
    return service.get_modules_markdown(course_ref)