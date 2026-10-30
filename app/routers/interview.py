from fastapi import APIRouter
from app.models.schemas import (
    InterviewQuestionsRequest,
    InterviewQuestionsResponse,
    AnswerEvaluationRequest,
    AnswerEvaluationResponse
)
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api", tags=["Interview Questions"])

@router.post("/interview-questions", response_model=InterviewQuestionsResponse)
async def generate_interview_questions(payload: InterviewQuestionsRequest):
    """
    Generates tailored technical, behavioral, and architectural interview questions
    with evaluation rubrics and sample outline answers.
    """
    return await ai_service.generate_interview_questions(
        job_role=payload.job_role,
        skills=payload.skills,
        count=payload.count or 6
    )

@router.post("/interview/evaluate", response_model=AnswerEvaluationResponse)
async def evaluate_interview_answer(payload: AnswerEvaluationRequest):
    """
    Evaluates candidate's written or transcribed interview answer, returning an objective score (1-10)
    and structured strengths, improvements, and model answer tips.
    """
    result = await ai_service.evaluate_candidate_answer(
        question=payload.question,
        answer=payload.answer,
        job_role=payload.job_role,
        question_type=payload.question_type or "Technical"
    )
    return AnswerEvaluationResponse(**result)
