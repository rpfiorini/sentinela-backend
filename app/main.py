from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import auth, people, correspondences, checklist

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(people.router, prefix="/people", tags=["people"])
app.include_router(correspondences.router, prefix="/correspondences", tags=["correspondences"])
app.include_router(checklist.router, prefix="/checklists", tags=["checklists"])

@app.get("/")
def root():
    return {"status": "online", "app": settings.app_name}
