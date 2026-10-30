import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from app.services.resume_parser import resume_parser
from app.ml.skills_extractor import skills_extractor
from app.ml.predictor import job_predictor
from app.db import db_manager
from app.models.schemas import (
    ResumeAnalysisResponse,
    TextAnalyzeRequest,
    SkillItem,
    RolePrediction,
    CandidateDetails
)

router = APIRouter(prefix="/api", tags=["Resume Analysis"])

SAMPLE_RESUMES = {
    "data_analyst": {
        "title": "Data Analyst Profile",
        "description": "SQL, Excel, Tableau, Python, Pandas, Power BI, Statistics",
        "text": """
John Doe - Senior Data Analyst
Email: john.doe@analytics.io | Phone: (555) 234-5678 | LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

SUMMARY
Detail-oriented Data Analyst with 4+ years of experience interpreting complex business datasets, developing automated dashboards in Tableau and Power BI, writing advanced SQL queries, and utilizing Python (Pandas, NumPy) for exploratory data analysis and forecasting.

TECHNICAL SKILLS
- Languages & Databases: SQL, Python, PostgreSQL, MySQL, Excel, Snowflake, BigQuery
- Analytics & Visualization: Pandas, NumPy, Tableau, Power BI, Matplotlib, Data Visualization, ETL
- Methodologies: Statistics, A/B Testing, Data Cleaning, Data Warehousing, Agile, Scrum

EXPERIENCE
Lead Data Analyst | Apex Insights (2022 - Present)
- Engineered automated SQL data pipelines and scheduled Tableau dashboards tracking 25+ business KPIs.
- Performed statistical regression and cohort analysis in Python to evaluate customer churn factors, driving 18% retention lift.
- Partnered with product and marketing teams to formulate data-driven campaign optimizations.
        """
    },
    "frontend_developer": {
        "title": "Frontend Engineer Profile",
        "description": "JavaScript, TypeScript, React, Next.js, HTML5, CSS3, Tailwind CSS, Redux",
        "text": """
Sarah Miller - Senior Frontend Engineer
Email: sarah.m@webcraft.dev | Phone: (555) 456-7890 | LinkedIn: linkedin.com/in/sarahmiller | GitHub: github.com/sarahm

SUMMARY
Creative and performance-focused Frontend Engineer with 4 years of experience building responsive, accessible web applications using React, Next.js, TypeScript, and Tailwind CSS.

TECHNICAL SKILLS
- Core: JavaScript, TypeScript, HTML5, CSS3, Responsive Design, UI/UX Design, Figma
- Frameworks & Libraries: React, Next.js, Redux, Tailwind CSS, Zustand
- Tooling & Practices: REST APIs, GraphQL, Git, Webpack, Vite, Jest, Performance Optimization

EXPERIENCE
Frontend Developer | DevCraft Studio (2021 - Present)
- Architected responsive web dashboards in Next.js and TypeScript serving over 150k active monthly users.
- Implemented modern design systems using Tailwind CSS and headless UI primitives.
- Optimized bundle sizes and image assets, boosting Lighthouse performance scores from 68 to 98.
        """
    },
    "ml_engineer": {
        "title": "Machine Learning Engineer Profile",
        "description": "Python, Scikit-learn, PyTorch, TensorFlow, Pandas, Docker, FastAPI, Git",
        "text": """
Alex Chen - Machine Learning Engineer
Email: alex.chen@ai-core.net | Phone: (555) 890-1234 | LinkedIn: linkedin.com/in/alexchen-ml | GitHub: github.com/alexchen-ai

SUMMARY
Machine Learning Engineer with strong background in predictive modeling, deep learning, PyTorch, Scikit-learn, and productionizing models with FastAPI and Docker containers.

TECHNICAL SKILLS
- Programming & ML: Python, PyTorch, Scikit-learn, TensorFlow, Pandas, NumPy, Machine Learning, Deep Learning
- Engineering & Cloud: Docker, Kubernetes, FastAPI, REST APIs, Git, Linux, MLOps, MLflow, SQL, AWS
- AI & NLP: Feature Engineering, Model Evaluation, NLP, Transformers, Vector Databases

EXPERIENCE
ML Engineer | DataCore Systems (2022 - Present)
- Trained classification and gradient boosting models using Scikit-learn and PyTorch with 94% test accuracy.
- Containerized model inference microservices with Docker and deployed high-throughput FastAPI REST endpoints.
- Built automated model retraining pipelines with validation metrics and drift monitoring.
        """
    },
    "devops_cloud_engineer": {
        "title": "DevOps & Cloud Architect Profile",
        "description": "AWS, Docker, Kubernetes, Terraform, CI/CD, Linux, Python, Bash, Prometheus",
        "text": """
Marcus Vance - DevOps & Cloud Infrastructure Engineer
Email: marcus.vance@cloudops.tech | Phone: (555) 345-6789 | LinkedIn: linkedin.com/in/marcusvance | GitHub: github.com/marcusv-cloud

SUMMARY
DevOps and Cloud Solutions Architect with 5+ years automating multi-region cloud infrastructure on AWS, managing containerized Kubernetes clusters, and architecting zero-downtime CI/CD deployment pipelines.

TECHNICAL SKILLS
- Cloud & Infrastructure: AWS, Cloud Architecture, System Design, Terraform, Linux, Bash
- Containers & Orchestration: Docker, Kubernetes, Helm, Microservices
- CI/CD & Observability: CI/CD, GitHub Actions, Jenkins, Prometheus, Grafana, Git
- Scripting & Networking: Python, Bash, Network Security, SSL/TLS, Cost Optimization

EXPERIENCE
Senior Cloud Engineer | Stratos Cloud (2021 - Present)
- Provisioned enterprise multi-account AWS infrastructure using Terraform modules and GitHub Actions CI/CD.
- Managed Kubernetes (EKS) clusters hosting 40+ microservices with automated horizontal pod autoscaling.
- Implemented Prometheus & Grafana alerting that reduced mean-time-to-resolution (MTTR) by 45%.
        """
    }
}

def build_analysis_response(raw_text: str, filename: str) -> ResumeAnalysisResponse:
    # 1. Extract candidate details
    candidate_details_dict = resume_parser.extract_candidate_details(raw_text)
    candidate_details = CandidateDetails(**candidate_details_dict)

    # 2. Extract skills
    skills_extracted = skills_extractor.extract_skills_from_text(raw_text)
    skill_names = [s["name"] for s in skills_extracted]

    # 3. ML Prediction & role matching
    prediction_results = job_predictor.predict_roles(raw_text, skill_names)
    
    top_role = prediction_results["top_predicted_role"]
    top_match = prediction_results["top_match_percentage"]
    readiness = prediction_results["readiness_score"]
    predictions = prediction_results["predictions"]
    missing_skills = prediction_results["missing_skills"]
    recommended_skills = prediction_results["recommended_skills"]

    # 4. Create career summary
    summary = (
        f"Profile evaluated for {candidate_details.name} identifying {len(skill_names)} verified technical competencies. "
        f"Strongest alignment is with '{top_role}' at {top_match}% role compatibility. "
        f"Prioritize acquiring {', '.join(missing_skills[:3]) if missing_skills else 'advanced system architecture'} to maximize interview conversion."
    )

    record_id = str(uuid.uuid4())
    record = {
        "id": record_id,
        "filename": filename,
        "candidate": candidate_details.dict(),
        "extracted_text_preview": raw_text[:800] + ("..." if len(raw_text) > 800 else ""),
        "total_skills_found": len(skills_extracted),
        "extracted_skills": skills_extracted,
        "top_predicted_role": top_role,
        "match_percentage": top_match,
        "readiness_score": readiness,
        "predictions": predictions,
        "missing_skills": missing_skills,
        "recommended_skills": recommended_skills,
        "career_summary": summary,
        "created_at": datetime.utcnow().isoformat()
    }

    # Save to MongoDB or local fallback
    db_manager.save_analysis(record)

    return ResumeAnalysisResponse(
        id=record_id,
        filename=filename,
        candidate=candidate_details,
        extracted_text_preview=record["extracted_text_preview"],
        total_skills_found=len(skills_extracted),
        extracted_skills=[SkillItem(**s) for s in skills_extracted],
        top_predicted_role=top_role,
        match_percentage=top_match,
        readiness_score=readiness,
        predictions=[RolePrediction(**p) for p in predictions],
        missing_skills=missing_skills,
        recommended_skills=recommended_skills,
        career_summary=summary,
        created_at=record["created_at"]
    )

@router.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume_pdf(file: UploadFile = File(...)):
    """
    Accepts PDF resume upload, extracts text, identifies skills, runs ML job role prediction,
    and returns comprehensive profile analysis.
    """
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT resume files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if file.filename.lower().endswith(".pdf"):
        try:
            raw_text = resume_parser.extract_text_from_pdf_bytes(content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to process PDF: {str(e)}")
    else:
        try:
            raw_text = content.decode("utf-8", errors="ignore")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to decode text file: {str(e)}")

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in document.")

    return build_analysis_response(raw_text, file.filename)

@router.post("/analyze-text", response_model=ResumeAnalysisResponse)
async def analyze_resume_text(payload: TextAnalyzeRequest):
    """
    Analyzes raw pasted resume text or skill description.
    """
    if not payload.text or len(payload.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Please provide at least 10 characters of resume content.")

    return build_analysis_response(payload.text, "Pasted Resume Content")

@router.get("/sample-resumes")
async def get_sample_resumes():
    """
    Provides curated sample resumes for immediate quick-testing without requiring user to find a PDF.
    """
    return SAMPLE_RESUMES
