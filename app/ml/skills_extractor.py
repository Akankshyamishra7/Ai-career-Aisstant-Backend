import re
from typing import List, Dict, Set
from app.ml.taxonomy import SKILL_ALIASES, SKILL_CATEGORIES, JOB_ROLES_TAXONOMY

# Compile regex patterns for special tokens to prevent erroneous word-boundary misses
SPECIAL_SKILLS = {
    "c++": "C++",
    "c#": "C#",
    ".net": ".NET",
    "node.js": "Node.js",
    "next.js": "Next.js",
    "vue.js": "Vue.js",
    "ci/cd": "CI/CD",
}

class SkillsExtractor:
    def __init__(self):
        # Build comprehensive map of canonical names + aliases
        full_map = dict(SKILL_ALIASES)
        
        # Add every canonical skill from taxonomy and categories
        for category_skill in SKILL_CATEGORIES.keys():
            full_map[category_skill.lower()] = category_skill

        for role_meta in JOB_ROLES_TAXONOMY.values():
            for s in role_meta.get("core_skills", []) + role_meta.get("recommended_skills", []):
                full_map[s.lower()] = s

        # Sort by length descending (longest phrases first, e.g. "machine learning" before "learning")
        self.alias_map = dict(sorted(full_map.items(), key=lambda item: len(item[0]), reverse=True))

    def extract_skills_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extracts matched technical and domain skills from raw resume or user text.
        Returns a list of dicts with 'name' and 'category'.
        """
        if not text:
            return []

        found_canonical_skills: Set[str] = set()
        clean_text = text.lower()

        # 1. Match special punctuation skills first
        for key, canonical in SPECIAL_SKILLS.items():
            pattern = re.escape(key)
            if re.search(pattern, clean_text):
                found_canonical_skills.add(canonical)

        # 2. Match standard alias keywords with word boundaries
        for alias, canonical in self.alias_map.items():
            if alias in SPECIAL_SKILLS:
                continue

            # Handle words like 'R' or 'C' or multi-word like 'power bi' or 'machine learning'
            if len(alias) <= 2:
                # Single or two letter tokens: require strict word boundary
                pattern = rf"(?:\b|\s){re.escape(alias)}(?:\b|\s|[,\.;:\)])"
            else:
                pattern = rf"\b{re.escape(alias)}\b"

            if re.search(pattern, clean_text):
                found_canonical_skills.add(canonical)

        # 3. Format result with categories
        result = []
        for skill in sorted(found_canonical_skills):
            category = SKILL_CATEGORIES.get(skill, "Technical Skill")
            result.append({
                "name": skill,
                "category": category
            })

        return result

    def get_skill_names(self, text: str) -> List[str]:
        extracted = self.extract_skills_from_text(text)
        return [s["name"] for s in extracted]

skills_extractor = SkillsExtractor()
