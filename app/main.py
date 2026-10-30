from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import resume, roadmap, interview, chat, history
from app.ml.train import get_or_load_model
from app.db import db_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure ML model is loaded or trained
    print("[Startup] Initializing ML Job Role Model...")
    try:
        get_or_load_model()
        print("[Startup] ML Model successfully loaded and ready.")
    except Exception as e:
        print(f"[Startup] Warning during model initialization: {e}")
    yield
    print("[Shutdown] Cleaning up AI Career Assistant.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent AI Career Assistant API for resume skill extraction, ML job prediction, roadmaps, and interview prep.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(interview.router)
app.include_router(chat.router)
app.include_router(history.router)

@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_manager.get_status()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
