from fastapi import HTTPException

from app.repositories.canvas_alias_repository import CanvasAliasRepository, normalize_alias


class CanvasReferenceResolver:
    def __init__(self, alias_repository: CanvasAliasRepository):
        self.alias_repository = alias_repository

    def resolve_course_ref(self, course_ref: str | int) -> int:
        course_ref = str(course_ref)

        if course_ref.isdigit():
            return int(course_ref)

        alias = self.alias_repository.resolve(
            entity_type="course",
            alias_key=normalize_alias(course_ref),
        )

        if not alias:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown course reference '{course_ref}'. Use a Canvas course ID or run /canvas/sync-aliases first.",
            )

        return int(alias["canvas_id"])