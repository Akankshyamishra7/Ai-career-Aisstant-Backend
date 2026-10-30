from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SkillItem(BaseModel):
    name: str
    category: str = "Technical Skill"

class CandidateDetails(BaseModel):
    name: str = "Candidate"
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    word_count: int = 0

class RolePrediction(BaseModel):
    role: str
    confidence: float
    match_percentage: int
    description: str
    missing_skills: List[str]
    matched_skills: List[str]
    market_demand: str = "High"
    avg_salary_range: str = "$85k - $130k"

class ResumeAnalysisResponse(BaseModel):
    id: str
    filename: Optional[str] = "Pasted Resume"
    candidate: Optional[CandidateDetails] = None
    extracted_text_preview: str
    total_skills_found: int
    extracted_skills: List[SkillItem]
    top_predicted_role: str
    match_percentage: int
    readiness_score: int
    predictions: List[RolePrediction]
    missing_skills: List[str]
    recommended_skills: List[str]
    career_summary: str
    created_at: str

class TextAnalyzeRequest(BaseModel):
    text: str
    target_role: Optional[str] = None

class RoadmapMilestone(BaseModel):
    week_or_month: str
    title: str
    description: str
    skills_to_learn: List[str]
    recommended_resources: List[Dict[str, str]]
    practice_project: str

class CareerRoadmapRequest(BaseModel):
    target_role: str
    current_skills: List[str]
    missing_skills: List[str]
    experience_level: Optional[str] = "Beginner to Intermediate"
    timeline_weeks: Optional[int] = 12

class CareerRoadmapResponse(BaseModel):
    target_role: str
    estimated_timeline: str
    overview: str
    milestones: List[RoadmapMilestone]
    key_certifications: List[str]
    interview_readiness_tips: List[str]

class InterviewQuestion(BaseModel):
    id: int
    type: str  # Technical, System Design, Coding, STAR Behavioral
    question: str
    why_asked: str
    key_points_to_cover: List[str]
    sample_answer_outline: str

class InterviewQuestionsRequest(BaseModel):
    job_role: str
    skills: List[str]
    count: Optional[int] = 6

class InterviewQuestionsResponse(BaseModel):
    job_role: str
    difficulty: str = "Mid-Level"
    questions: List[InterviewQuestion]

class AnswerEvaluationRequest(BaseModel):
    question: str
    answer: str
    job_role: str
    question_type: Optional[str] = "Technical"

class AnswerEvaluationResponse(BaseModel):
    score: int
    strengths: List[str]
    improvements: List[str]
    model_answer_tip: str

class ChatMessage(BaseModel):
    role: str # user or assistant
    content: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    chat_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str
    suggestions: List[str] = []
