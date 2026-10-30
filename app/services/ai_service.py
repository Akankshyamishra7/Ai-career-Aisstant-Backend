import json
import os
from typing import List, Dict, Any, Optional
import httpx

from app.config import settings
from app.models.schemas import (
    RoadmapMilestone,
    CareerRoadmapResponse,
    InterviewQuestion,
    InterviewQuestionsResponse,
    ChatResponse
)

class AIService:
    def __init__(self):
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_key = settings.OPENAI_API_KEY

    async def _call_gemini(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.gemini_key:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"System Instructions: {system_instruction}\n\nTask: {prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 2048,
            }
        }
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                else:
                    print(f"[AIService] Gemini API error: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"[AIService] Gemini API exception: {e}")
        return None

    async def _call_openai(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.openai_key:
            return None
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5
        }
        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(url, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"[AIService] OpenAI API error: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"[AIService] OpenAI API exception: {e}")
        return None

    async def generate_career_roadmap(
        self,
        target_role: str,
        current_skills: List[str],
        missing_skills: List[str],
        experience_level: str = "Beginner to Intermediate",
        timeline_weeks: int = 12
    ) -> CareerRoadmapResponse:
        """
        Generates a tailored learning roadmap targeting the missing skills
        for the given job role.
        """
        # Try external LLM first if configured
        system_prompt = (
            "You are an expert tech career coach and curriculum architect. "
            "Return valid JSON adhering strictly to this schema: "
            '{"target_role": str, "estimated_timeline": str, "overview": str, "milestones": [{"week_or_month": str, "title": str, "description": str, "skills_to_learn": [str], "recommended_resources": [{"title": str, "url": str, "type": str}], "practice_project": str}], "key_certifications": [str], "interview_readiness_tips": [str]}'
        )
        user_prompt = (
            f"Generate a practical {timeline_weeks}-week roadmap for a candidate aspiring to be a '{target_role}'.\n"
            f"Current Skills: {', '.join(current_skills) if current_skills else 'None specified'}\n"
            f"Missing Skills to master: {', '.join(missing_skills) if missing_skills else 'Advanced patterns'}\n"
            f"Experience level: {experience_level}.\n"
            "Format response as strict raw JSON without backticks."
        )

        llm_reply = None
        if self.gemini_key:
            llm_reply = await self._call_gemini(user_prompt, system_prompt)
        elif self.openai_key:
            llm_reply = await self._call_openai(user_prompt, system_prompt)

        if llm_reply:
            try:
                # Clean potential markdown fences
                clean_json = llm_reply.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                if clean_json.startswith("```"):
                    clean_json = clean_json[3:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                clean_json = clean_json.strip()
                data = json.loads(clean_json)
                return CareerRoadmapResponse(**data)
            except Exception as e:
                print(f"[AIService] Failed to parse LLM roadmap JSON: {e}, using heuristic generator.")

        # Authoritative Heuristic Engine Fallback
        return self._generate_heuristic_roadmap(target_role, current_skills, missing_skills, timeline_weeks)

    def _generate_heuristic_roadmap(
        self,
        target_role: str,
        current_skills: List[str],
        missing_skills: List[str],
        timeline_weeks: int = 12
    ) -> CareerRoadmapResponse:
        skills_pool = missing_skills if missing_skills else ["Core Architecture", "Production Deployment", "Advanced Patterns"]
        
        milestones = []
        # Chunk skills across 4 phases
        step_skills = []
        n_chunks = 4
        chunk_size = max(1, (len(skills_pool) + n_chunks - 1) // n_chunks)
        for i in range(0, len(skills_pool), chunk_size):
            step_skills.append(skills_pool[i:i + chunk_size])

        # Ensure 4 stages
        while len(step_skills) < 4:
            step_skills.append([f"Advanced {target_role} Specialization"])

        milestones.append(RoadmapMilestone(
            week_or_month="Weeks 1 - 3",
            title=f"Foundation & Bridging Core Gaps: {', '.join(step_skills[0])}",
            description=f"Establish rigorous theoretical grounding and hands-on syntax for {', '.join(step_skills[0])}. Bridge prerequisite gaps while reinforcing your existing strengths.",
            skills_to_learn=step_skills[0],
            recommended_resources=[
                {"title": f"Official {step_skills[0][0]} Documentation & Quickstart", "url": "https://devdocs.io", "type": "Documentation"},
                {"title": f"Interactive {step_skills[0][0]} Mastery Course", "url": "https://freecodecamp.org", "type": "Interactive Course"}
            ],
            practice_project=f"Build a standalone prototype applying {step_skills[0][0]} with clean error handling and automated test coverage."
        ))

        milestones.append(RoadmapMilestone(
            week_or_month="Weeks 4 - 6",
            title=f"Core Tooling & Modern Workflows: {', '.join(step_skills[1])}",
            description=f"Deep dive into production conventions with {', '.join(step_skills[1])}. Implement realistic data pipelines, state management, or API integrations.",
            skills_to_learn=step_skills[1],
            recommended_resources=[
                {"title": f"Deep Dive into {step_skills[1][0]} Patterns", "url": "https://coursera.org", "type": "Video Course"},
                {"title": "Production Best Practices Guide", "url": "https://roadmap.sh", "type": "Architectural Guide"}
            ],
            practice_project=f"Develop a mini-application that bridges {current_skills[0] if current_skills else 'core fundamentals'} with {step_skills[1][0]}."
        ))

        milestones.append(RoadmapMilestone(
            week_or_month="Weeks 7 - 9",
            title=f"System Architecture & Scalability: {', '.join(step_skills[2])}",
            description=f"Integrate {', '.join(step_skills[2])} with end-to-end performance benchmarking, database design, and cloud containerization.",
            skills_to_learn=step_skills[2],
            recommended_resources=[
                {"title": "System Design & Scalability Principles", "url": "https://github.com/donnemartin/system-design-primer", "type": "Open Source"},
                {"title": f"Real-world {target_role} Case Studies", "url": "https://medium.com", "type": "Engineering Blog"}
            ],
            practice_project=f"Architect a capstone microservice or full-stack dashboard featuring authentication, database persistence, and {step_skills[2][0]}."
        ))

        milestones.append(RoadmapMilestone(
            week_or_month="Weeks 10 - 12",
            title=f"Production Deployment, Portfolio & Interview Prep: {', '.join(step_skills[3])}",
            description=f"Containerize your capstone, set up CI/CD automation, write detailed README documentation, and simulate technical interview rounds for {target_role}.",
            skills_to_learn=step_skills[3],
            recommended_resources=[
                {"title": "LeetCode & HackerRank Interview Practice", "url": "https://leetcode.com", "type": "Interview Practice"},
                {"title": "System Design & Behavioral Mock Interviews", "url": "https://pramp.com", "type": "Mock Interviews"}
            ],
            practice_project=f"Deploy your end-to-end {target_role} capstone to a cloud provider (AWS/Vercel/Render) with live URL and GitHub repository."
        ))

        return CareerRoadmapResponse(
            target_role=target_role,
            estimated_timeline=f"{timeline_weeks} Weeks (10-15 hrs/week recommended)",
            overview=f"This structured roadmap is curated to elevate you from your current profile to a competitive {target_role}. It systematically bridges your missing skills ({', '.join(missing_skills[:4])}) while compounding your established strengths.",
            milestones=milestones,
            key_certifications=[
                f"AWS Certified Solutions Architect or Cloud Practitioner",
                f"Certified {target_role} Professional (Coursera / Google / Meta)",
                f"Official Specialized Credential in {missing_skills[0] if missing_skills else 'Advanced Architecture'}"
            ],
            interview_readiness_tips=[
                "Rehearse the STAR methodology (Situation, Task, Action, Result) for all resume projects.",
                f"Be prepared to explain tradeoffs between {missing_skills[0] if missing_skills else 'tools'} and competing alternatives.",
                "Practice writing clean code and explaining your thinking out loud during live whiteboard sessions.",
                "Publish all projects to GitHub with architecture diagrams, setup instructions, and live demos."
            ]
        )

    async def generate_interview_questions(
        self,
        job_role: str,
        skills: List[str],
        count: int = 6
    ) -> InterviewQuestionsResponse:
        """
        Generates realistic technical and behavioral interview questions tailored to the predicted role.
        """
        system_prompt = (
            "You are a Senior Principal Interviewer at a top tier tech company. "
            "Return valid JSON adhering to: "
            '{"job_role": str, "difficulty": str, "questions": [{"id": int, "type": str, "question": str, "why_asked": str, "key_points_to_cover": [str], "sample_answer_outline": str}]}'
        )
        user_prompt = (
            f"Generate {count} high-signal interview questions for a '{job_role}' role.\n"
            f"Candidate Skills: {', '.join(skills[:8])}.\n"
            "Include 3 Technical questions, 2 Behavioral/Leadership, and 1 System/Scenario question. "
            "Output raw JSON without markdown formatting."
        )

        llm_reply = None
        if self.gemini_key:
            llm_reply = await self._call_gemini(user_prompt, system_prompt)
        elif self.openai_key:
            llm_reply = await self._call_openai(user_prompt, system_prompt)

        if llm_reply:
            try:
                clean_json = llm_reply.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                if clean_json.startswith("```"):
                    clean_json = clean_json[3:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                clean_json = clean_json.strip()
                data = json.loads(clean_json)
                return InterviewQuestionsResponse(**data)
            except Exception as e:
                print(f"[AIService] Failed to parse LLM interview JSON: {e}")

        # Heuristic Generator Fallback
        return self._generate_heuristic_interview_questions(job_role, skills)

    def _generate_heuristic_interview_questions(self, job_role: str, skills: List[str]) -> InterviewQuestionsResponse:
        primary_skill = skills[0] if skills else "System Architecture"
        secondary_skill = skills[1] if len(skills) > 1 else "Database Optimization"
        tertiary_skill = skills[2] if len(skills) > 2 else "API Design"

        questions = [
            InterviewQuestion(
                id=1,
                type="Technical (Deep Dive)",
                question=f"How do you optimize performance and manage resource bottlenecks when scaling applications built with {primary_skill}?",
                why_asked="Tests hands-on production experience, profiling abilities, and deep knowledge of runtime characteristics.",
                key_points_to_cover=[
                    f"Explain memory management, asynchronous execution, or query indexing in {primary_skill}.",
                    "Discuss profiling tools (APM, profilers, latency monitors) used to isolate bottlenecks.",
                    "Highlight caching layers (e.g. Redis), connection pooling, or batching strategies."
                ],
                sample_answer_outline=f"Start by outlining a real scenario where latency degraded. Describe how you profiled {primary_skill} metrics, pinpointed slow operations, implemented caching/indexing, and achieved measurable (e.g. 40%) throughput gains."
            ),
            InterviewQuestion(
                id=2,
                type="Technical (Architecture & Design)",
                question=f"Compare how you handle data consistency, schemas, and transactions when working with {secondary_skill} versus alternative paradigms.",
                why_asked="Evaluates your understanding of data integrity, ACID vs BASE tradeoffs, and schema evolution.",
                key_points_to_cover=[
                    "ACID compliance vs eventual consistency in distributed systems.",
                    "Proper indexing strategies to avoid full table/collection scans.",
                    "Migration strategies for schema changes without application downtime."
                ],
                sample_answer_outline=f"State the business context requirements (e.g. financial transaction vs social feed). Contrast write speed vs query complexity in {secondary_skill}, emphasizing reliability and resilience."
            ),
            InterviewQuestion(
                id=3,
                type="Technical (Practical Implementation)",
                question=f"Walk us through how you would architect a secure, fault-tolerant REST API or data pipeline using {tertiary_skill}.",
                why_asked="Checks whether you implement secure coding standards, input validation, and graceful error handling.",
                key_points_to_cover=[
                    "Authentication & authorization (JWT, OAuth2, RBAC).",
                    "Input validation, sanitize queries against injection, rate limiting.",
                    "Idempotency and retry mechanisms with exponential backoff."
                ],
                sample_answer_outline="Describe the lifecycle of an incoming request from API gateway to database layer. Emphasize observability (structured logs), health checks, and defensive coding."
            ),
            InterviewQuestion(
                id=4,
                type="Behavioral (STAR Method)",
                question=f"Tell me about a time when a critical bug or performance outage occurred in your code. How did you diagnose, resolve, and prevent it?",
                why_asked="Evaluates emotional composure, root cause analysis, accountability, and blameless post-mortem culture.",
                key_points_to_cover=[
                    "Situation: The severity of the incident and impact on users.",
                    "Task: Your immediate responsibility in triage and mitigation.",
                    "Action: How you isolated the root cause systematically without panic.",
                    "Result: Restored service, added regression tests, and updated alerting."
                ],
                sample_answer_outline="Follow STAR cleanly: 'During a release, memory spiked... I rolled back first, analyzed error logs, identified an unclosed connection leak, deployed a hotfix with tests, and wrote a post-mortem to alert on leak thresholds.'"
            ),
            InterviewQuestion(
                id=5,
                type="Situational / Team Collaboration",
                question=f"How do you handle disagreement with a senior engineer or product manager regarding the technical approach for a {job_role} project?",
                why_asked="Measures communication skills, empathy, willingness to listen, and ability to use data to justify technical decisions.",
                key_points_to_cover=[
                    "Seek first to understand the business constraints and product deadlines.",
                    "Create objective prototypes or benchmark data rather than relying on opinions.",
                    "Disagree and commit: Respecting final decisions once aligned."
                ],
                sample_answer_outline="Explain that you separate ego from architecture. Outline how you wrote a lightweight RFC with pros/cons, scheduled a 15-minute sync, converged on an incremental compromise, and delivered on time."
            ),
            InterviewQuestion(
                id=6,
                type="System Design & Scalability",
                question=f"Design an end-to-end analytics and tracking system for 10 million daily active users suitable for a {job_role}.",
                why_asked="Tests high-level systems thinking, horizontal scalability, partitioning, and caching.",
                key_points_to_cover=[
                    "API Gateway, rate limiting, and event ingestion queue (Kafka/RabbitMQ).",
                    "Stream processing or microservice workers writing to partitioned storage.",
                    "Aggregation pipelines and read replica caching for sub-second dashboards."
                ],
                sample_answer_outline="Start by asking clarifying scope questions (read/write ratio, latency requirements). Sketch the architecture into Ingestion -> Processing -> Storage -> Serving layers, discussing failover at each step."
            )
        ]

        return InterviewQuestionsResponse(
            job_role=job_role,
            difficulty="Mid to Senior Level",
            questions=questions
        )

    async def evaluate_candidate_answer(
        self,
        question: str,
        answer: str,
        job_role: str,
        question_type: str = "Technical"
    ) -> Dict[str, Any]:
        """
        Evaluates a candidate's answer for technical depth, clarity, and STAR structure,
        providing an objective score (1-10) and feedback.
        """
        system_prompt = (
            "You are a Senior Technical Interviewer. Evaluate the candidate's interview answer objectively. "
            "Return valid JSON adhering strictly to: "
            '{"score": int, "strengths": [str], "improvements": [str], "model_answer_tip": str}'
        )
        user_prompt = (
            f"Job Role: {job_role}\n"
            f"Question Type: {question_type}\n"
            f"Question: {question}\n\n"
            f"Candidate Answer: {answer}\n\n"
            "Score from 1 to 10. List 2 specific strengths, 2 targeted improvements, and 1 concise model answer tip."
        )

        llm_reply = None
        if self.gemini_key:
            llm_reply = await self._call_gemini(user_prompt, system_prompt)
        elif self.openai_key:
            llm_reply = await self._call_openai(user_prompt, system_prompt)

        if llm_reply:
            try:
                clean_json = llm_reply.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                if clean_json.startswith("```"):
                    clean_json = clean_json[3:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                clean_json = clean_json.strip()
                return json.loads(clean_json)
            except Exception as e:
                print(f"[AIService] Failed to parse evaluation JSON: {e}")

        # Intelligent rubric fallback calculation
        words = len(answer.strip().split()) if answer else 0
        if words < 10:
            return {
                "score": 3,
                "strengths": ["Attempted to answer"],
                "improvements": ["Answer is too brief. Elaborate with specific technical details, architecture choices, or concrete numbers.", "Use structured phrasing (e.g. STAR method for behavioral or Tradeoffs for technical)."],
                "model_answer_tip": "Aim for a structured response covering context, technical reasoning, tradeoffs made, and measurable outcomes."
            }
        
        # Calculate dynamic score based on depth and keywords
        has_metrics = bool(any(char.isdigit() or sym in answer for char in answer for sym in ["%", "$", "ms", "x"]))
        has_structure = bool(any(k in answer.lower() for k in ["because", "first", "tradeoff", "result", "situation", "scale", "performance"]))
        
        score = 6
        if words >= 40:
            score += 1
        if has_metrics:
            score += 1
        if has_structure:
            score += 1
        score = min(max(score, 4), 9)

        return {
            "score": score,
            "strengths": [
                "Clear understanding of the underlying domain problem.",
                "Addressed the core question directly with relevant technical context." if words >= 30 else "Good foundational terminology."
            ],
            "improvements": [
                "Quantify business impact or performance metrics (e.g., 'reduced latency by 35%', 'processed 2M records').",
                "Explicitly address tradeoffs or alternative solutions considered."
            ],
            "model_answer_tip": f"For {job_role} interviews, highlight how your approach balances latency, maintainability, and scalability."
        }

    async def chat(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Any]] = None
    ) -> ChatResponse:
        """
        Conversational career advisor answering questions about resume, jobs, learning resources, and interview tactics.
        """
        role_ctx = context.get("top_predicted_role", "Software Engineer") if context else "Software Engineer"
        skills_ctx = context.get("extracted_skills", []) if context else []
        missing_ctx = context.get("missing_skills", []) if context else []
        skills_str = ", ".join([s["name"] if isinstance(s, dict) else str(s) for s in skills_ctx])

        system_prompt = (
            f"You are the AI Career Assistant Coach. You are advising a candidate who is targeting or best-matched for: '{role_ctx}'. "
            f"Their identified current skills: {skills_str or 'General Tech'}. "
            f"Their missing/recommended skills to learn: {', '.join(missing_ctx) or 'None specified'}. "
            "Be encouraging, highly actionable, concise, and structured. Include bullet points and practical next steps."
        )

        llm_reply = None
        if self.gemini_key:
            prompt_with_history = f"History: {chat_history[-3:] if chat_history else ''}\nUser asks: {user_message}"
            llm_reply = await self._call_gemini(prompt_with_history, system_prompt)
        elif self.openai_key:
            prompt_with_history = f"History: {chat_history[-3:] if chat_history else ''}\nUser asks: {user_message}"
            llm_reply = await self._call_openai(prompt_with_history, system_prompt)

        if llm_reply:
            return ChatResponse(
                reply=llm_reply.strip(),
                suggestions=[
                    f"What projects should I build to learn {missing_ctx[0] if missing_ctx else 'new skills'}?",
                    f"How do I present my experience for a {role_ctx} role?",
                    "Can you generate mock interview questions for me?"
                ]
            )

        # Smart Heuristic Assistant Response
        msg_lower = user_message.lower()
        if "missing" in msg_lower or "learn" in msg_lower or "roadmap" in msg_lower:
            reply = (
                f"### High-Impact Next Steps for **{role_ctx}**\n\n"
                f"Based on your profile, the top skills that will boost your market value are: **{', '.join(missing_ctx[:4]) if missing_ctx else 'Advanced Cloud & Architecture'}**.\n\n"
                f"**Recommended Action Plan:**\n"
                f"1. **Phase 1 (Fundamentals):** Dedicate 10-15 days to master core syntax and concepts of {missing_ctx[0] if missing_ctx else 'key tools'}.\n"
                f"2. **Phase 2 (Project Integration):** Connect {missing_ctx[0] if missing_ctx else 'your new skill'} with your existing strengths ({skills_str.split(',')[0] if skills_str else 'Python/JavaScript'}).\n"
                f"3. **Phase 3 (Portfolio Proof):** Build and deploy a public GitHub project showcasing real-world performance benchmarks.\n\n"
                f"Would you like a step-by-step 12-week roadmap or suggested open-source repositories to study?"
            )
        elif "interview" in msg_lower or "question" in msg_lower or "salary" in msg_lower:
            reply = (
                f"### Interview Preparation for **{role_ctx}**\n\n"
                f"Candidates in this domain are evaluated on three major pillars:\n\n"
                f"- **Core Technical Depth:** Expect deep questions on {skills_str.split(',')[0] if skills_str else 'core language/framework'} internals and memory/execution models.\n"
                f"- **System Design & Tradeoffs:** Be prepared to discuss how you structure data models and scale services under load.\n"
                f"- **Behavioral Impact:** Prepare 3-4 STAR stories focusing on overcoming technical blockers and delivering measurable business impact.\n\n"
                f"Check out the **Interview Generator** tab to practice questions tailored directly to your profile!"
            )
        else:
            reply = (
                f"Great question! As an aspiring or progressing **{role_ctx}**, balancing your core technical mastery ({skills_str or 'foundational tools'}) "
                f"with in-demand market additions ({', '.join(missing_ctx[:3]) if missing_ctx else 'system architecture'}) is the fastest path to landing top offers.\n\n"
                f"**Key Recommendations:**\n"
                f"- **Showcase depth over breadth:** Having 2 polished portfolio projects with live URLs beats 10 unfinished tutorials.\n"
                f"- **Quantify resume bullets:** Replace 'Worked on APIs' with 'Engineered REST API endpoints reducing response latency by 35%'.\n"
                f"- **Stay consistent:** Commit 1 hour daily to deliberate practice on missing concepts.\n\n"
                f"What specific topic or challenge would you like to explore next?"
            )

        return ChatResponse(
            reply=reply,
            suggestions=[
                f"How should I organize my resume for {role_ctx}?",
                f"What is the best way to master {missing_ctx[0] if missing_ctx else 'SQL/Cloud'}?",
                "Give me 3 capstone project ideas to build for my portfolio."
            ]
        )

ai_service = AIService()
