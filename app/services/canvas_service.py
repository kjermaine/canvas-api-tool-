from app.providers.canvas_client import CanvasClient
from app.repositories.canvas_alias_repository import CanvasAliasRepository, normalize_alias
from app.services.canvas_reference_resolver import CanvasReferenceResolver
from app.services.export_service import ExportService


class CanvasService:
    def __init__(
        self,
        canvas_client: CanvasClient,
        alias_repository: CanvasAliasRepository,
        reference_resolver: CanvasReferenceResolver,
        export_service: ExportService,
    ):
        self.canvas_client = canvas_client
        self.alias_repository = alias_repository
        self.reference_resolver = reference_resolver
        self.export_service = export_service

    def get_courses(self):
        courses = self.canvas_client.get_courses()

        return [
            {
                "id": course.get("id"),
                "name": course.get("name"),
                "course_code": course.get("course_code"),
                "workflow_state": course.get("workflow_state"),
            }
            for course in courses
        ]

    def sync_aliases(self):
        courses = self.get_courses()
        created = []

        for course in courses:
            if not course.get("id") or not course.get("name"):
                continue

            aliases = {
                normalize_alias(course["name"]),
            }

            if course.get("course_code"):
                aliases.add(normalize_alias(course["course_code"]))

            first_word = normalize_alias(course["name"]).split("_")[0]
            if first_word:
                aliases.add(first_word)

            for alias in aliases:
                self.alias_repository.save_alias(
                    alias_key=alias,
                    entity_type="course",
                    canvas_id=course["id"],
                    display_name=course["name"],
                    source="system",
                )
                created.append(
                    {
                        "alias": alias,
                        "entity_type": "course",
                        "canvas_id": course["id"],
                        "display_name": course["name"],
                    }
                )

        return {
            "status": "synced",
            "created_aliases": created,
        }

    def get_aliases(self):
        return self.alias_repository.list_aliases()

    def save_alias(self, alias: str, entity_type: str, canvas_id: int, display_name: str):
        self.alias_repository.save_alias(
            alias_key=alias,
            entity_type=entity_type,
            canvas_id=canvas_id,
            display_name=display_name,
            source="user",
        )

        return {
            "status": "saved",
            "alias": normalize_alias(alias),
            "entity_type": entity_type,
            "canvas_id": canvas_id,
        }

    def get_modules(self, course_ref: str):
        course_id = self.reference_resolver.resolve_course_ref(course_ref)
        return self.canvas_client.get_modules(course_id)

    def get_assignments(self, course_ref: str):
        course_id = self.reference_resolver.resolve_course_ref(course_ref)
        assignments = self.canvas_client.get_assignments(course_id)

        return [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "due_at": item.get("due_at"),
                "html_url": item.get("html_url"),
                "points_possible": item.get("points_possible"),
                "published": item.get("published"),
            }
            for item in assignments
        ]

    def get_calendar(self, course_ref: str):
        course_id = self.reference_resolver.resolve_course_ref(course_ref)
        events = self.canvas_client.get_calendar_events(course_id)

        return [
            {
                "id": event.get("id"),
                "title": event.get("title"),
                "start_at": event.get("start_at"),
                "end_at": event.get("end_at"),
                "html_url": event.get("html_url"),
            }
            for event in events
        ]

    def get_modules_markdown(self, course_ref: str):
        modules = self.get_modules(course_ref)
        return self.export_service.modules_to_markdown(course_ref, modules)