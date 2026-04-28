import requests


class CanvasClient:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

    def _get(self, path: str, params: dict | None = None):
        response = requests.get(
            f"{self.base_url}{path}",
            headers=self._headers(),
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def get_courses(self):
        return self._get("/api/v1/courses", params={"enrollment_state": "active"})

    def get_modules(self, course_id: int):
        return self._get(
            f"/api/v1/courses/{course_id}/modules",
            params={"include[]": "items"},
        )

    def get_assignments(self, course_id: int):
        return self._get(f"/api/v1/courses/{course_id}/assignments")

    def get_calendar_events(self, course_id: int):
        return self._get(
            "/api/v1/calendar_events",
            params={
                "context_codes[]": f"course_{course_id}",
                "type": "event",
                "all_events": "true",
            },
        )