from fastapi import FastAPI

from app.api.routes import canvas
from app.api.routes import canvas_auth
from app.api.routes import canvas_routes

app = FastAPI(
    title="Canvas API Utility",
    description="A FastAPI utility layer for Canvas data, aliases, and study-friendly exports.",
    version="0.1.0",
)

app.include_router(canvas.router)
app.include_router(canvas_auth.router)
app.include_router(canvas_routes.router)


@app.get("/")
def root():
    return {"status": "running"}