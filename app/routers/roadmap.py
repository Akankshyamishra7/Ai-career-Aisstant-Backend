from fastapi import APIRouter
from app.models.schemas import CareerRoadmapRequest, CareerRoadmapResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api", tags=["Career Roadmap"])

@router.post("/roadmap", response_model=CareerRoadmapResponse)
async def generate_roadmap(payload: CareerRoadmapRequest):
    """
    Generates an AI personalized step-by-step career learning roadmap based on
    target job role and missing skills.
    """
    return await ai_service.generate_career_roadmap(
        target_role=payload.target_role,
        current_skills=payload.current_skills,
        missing_skills=payload.missing_skills,
        experience_level=payload.experience_level or "Beginner to Intermediate",
        timeline_weeks=payload.timeline_weeks or 12
    )
