from typing import List, Dict, Any, Tuple
import numpy as np
from app.ml.train import get_or_load_model
from app.ml.taxonomy import JOB_ROLES_TAXONOMY

class JobRolePredictor:
    def __init__(self):
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            self._pipeline = get_or_load_model()
        return self._pipeline

    def predict_roles(self, resume_text: str, extracted_skill_names: List[str]) -> Dict[str, Any]:
        """
        Uses trained ML pipeline + skill taxonomy overlap to predict top job roles,
        calculate match percentages, identify missing skills, and compute readiness.
        """
        # Formulate query text combining raw text preview + highlighted skills
        query_text = f"{' '.join(extracted_skill_names)} {resume_text[:2000]}"
        
        # ML Probabilities
        classes = self.pipeline.classes_
        probabilities = self.pipeline.predict_proba([query_text])[0]
        
        # User skill set lowercase lookup
        user_skills_lower = {s.lower() for s in extracted_skill_names}

        role_evaluations: List[Dict[str, Any]] = []

        for idx, role in enumerate(classes):
            prob = float(probabilities[idx])
            role_meta = JOB_ROLES_TAXONOMY.get(role, {
                "description": f"Role focusing on {role} responsibilities.",
                "core_skills": [],
                "recommended_skills": [],
                "salary_range": "$80k - $130k",
                "market_demand": "High"
            })

            core_skills = role_meta["core_skills"]
            recommended_skills = role_meta["recommended_skills"]
            all_target_skills = core_skills + recommended_skills

            # Identify matched and missing
            matched = []
            missing = []
            
            for cs in core_skills:
                if cs.lower() in user_skills_lower:
                    matched.append(cs)
                else:
                    missing.append(cs)

            for rs in recommended_skills:
                if rs.lower() in user_skills_lower:
                    if rs not in matched:
                        matched.append(rs)
                else:
                    if rs not in missing:
                        missing.append(rs)

            # Skill coverage computation
            core_overlap_ratio = len([s for s in core_skills if s.lower() in user_skills_lower]) / max(len(core_skills), 1)
            total_overlap_ratio = len(matched) / max(len(all_target_skills), 1)

            # Blended match score: 40% ML semantic confidence + 60% direct core skill coverage
            # Calibrate so candidates with strong matching skills get realistic 70%-95% scores
            raw_match = (prob * 45.0) + (core_overlap_ratio * 45.0) + (total_overlap_ratio * 10.0)
            
            # If user has good skills for the role, boost appropriately
            if core_overlap_ratio >= 0.5:
                raw_match = max(raw_match, core_overlap_ratio * 88.0)
            
            match_percentage = int(min(max(raw_match, 15.0), 98.0))

            role_evaluations.append({
                "role": role,
                "confidence": round(prob, 4),
                "match_percentage": match_percentage,
                "description": role_meta["description"],
                "matched_skills": matched,
                "missing_skills": missing[:6], # top missing skills
                "all_missing_skills": missing,
                "market_demand": role_meta.get("market_demand", "High"),
                "avg_salary_range": role_meta.get("salary_range", "$85k - $130k"),
                "core_overlap_ratio": core_overlap_ratio
            })

        # Sort by match percentage descending, then ML confidence
        role_evaluations.sort(key=lambda x: (x["match_percentage"], x["confidence"]), reverse=True)

        top_role = role_evaluations[0]
        
        # Calculate career readiness score (taking into account total skills + top match)
        readiness_score = int(min(max(top_role["match_percentage"] * 0.9 + min(len(extracted_skill_names) * 1.5, 15), 20), 99))

        return {
            "top_predicted_role": top_role["role"],
            "top_match_percentage": top_role["match_percentage"],
            "readiness_score": readiness_score,
            "predictions": role_evaluations[:5], # Return top 5 matched roles
            "missing_skills": top_role["missing_skills"],
            "recommended_skills": top_role["all_missing_skills"][:8],
            "role_meta": top_role
        }

job_predictor = JobRolePredictor()
