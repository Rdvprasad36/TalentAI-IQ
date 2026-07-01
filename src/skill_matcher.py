"""
Skill Matcher
-------------

Analyzes candidate skills and computes an intelligent
skill matching score for AI/ML job roles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.config import AI_SKILLS_NORMALIZED

Candidate = dict[str, Any]


@dataclass(slots=True)
class SkillFeatures:

    total_skills: int = 0

    ai_skills: int = 0

    advanced_ai_skills: int = 0

    llm_skills: int = 0

    vector_db_skills: int = 0

    ml_skills: int = 0

    cloud_skills: int = 0

    average_endorsements: float = 0

    average_duration: float = 0

    skill_score: float = 0
    keyword_stuffing: bool = False


class SkillMatcher:

    def analyze(self, skills):

        result = SkillFeatures()

        if not skills:
            return result

        llm_keywords = {
            "llms",
            "fine-tuning llms",
            "transformers",
            "langchain",
            "langgraph",
            "rag",
            "lora",
        }

        vector_keywords = {
            "milvus",
            "pinecone",
            "faiss",
            "qdrant",
            "vector databases",
        }

        ml_keywords = {
            "machine learning",
            "deep learning",
            "nlp",
            "computer vision",
            "speech recognition",
            "gans",
            "classification",
        }

        cloud_keywords = {
            "aws",
            "azure",
            "gcp",
        }

        total_endorsements = 0
        total_duration = 0

        for skill in skills:

            name = skill.get("name", "").lower()

            duration = skill.get("duration_months", 0)

            endorsements = skill.get("endorsements", 0)

            proficiency = skill.get("proficiency", "").lower()

            result.total_skills += 1

            total_endorsements += endorsements

            total_duration += duration

            if name in AI_SKILLS_NORMALIZED:
                result.ai_skills += 1

            if proficiency == "advanced":
                result.advanced_ai_skills += 1

            if any(word in name for word in llm_keywords):
                result.llm_skills += 1

            if any(word in name for word in vector_keywords):
                result.vector_db_skills += 1

            if any(word in name for word in ml_keywords):
                result.ml_skills += 1

            if any(word in name for word in cloud_keywords):
                result.cloud_skills += 1

        result.average_endorsements = (
            total_endorsements / max(result.total_skills, 1)
        )

        result.average_duration = (
            total_duration / max(result.total_skills, 1)
        )

        score = 0

        score += result.ai_skills * 2
        score += result.advanced_ai_skills * 2
        score += result.llm_skills * 4
        score += result.vector_db_skills * 3
        score += result.ml_skills * 2
        score += result.cloud_skills * 1
        score += result.average_endorsements * 0.10
        score += result.average_duration * 0.05

        result.skill_score = min(score, 100)

        return result