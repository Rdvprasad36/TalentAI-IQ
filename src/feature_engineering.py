"""
Feature Engineering Module
--------------------------

Extracts structured features from Redrob candidate profiles.

This module converts raw JSON candidate records into numerical and categorical
features that are later consumed by the scoring engine.

Author: RDV
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.config import (
    AI_SKILLS_NORMALIZED,
    PRODUCT_COMPANIES_NORMALIZED,
    CONSULTING_COMPANIES_NORMALIZED,
)


Candidate = dict[str, Any]


@dataclass(slots=True)
class CandidateFeatures:
    # --------------------
    # Experience
    # --------------------
    years_experience: float = 0
    avg_job_duration: float = 0
    total_jobs: int = 0

    # --------------------
    # Skills
    # --------------------
    ai_skill_count: int = 0
    ai_skill_score: float = 0
    llm_score: float = 0
    vector_db_score: float = 0
    cloud_score: float = 0

    # --------------------
    # Career
    # --------------------
    product_company_count: int = 0
    consulting_company_count: int = 0

    # --------------------
    # Behaviour
    # --------------------
    github_score: float = 0
    recruiter_response_rate: float = 0
    interview_completion_rate: float = 0
    profile_completeness: float = 0
    notice_period: int = 0
    open_to_work: bool = False
    relocation: bool = False

    # --------------------
    # Education
    # --------------------
    education_tier: str = "unknown"

    # --------------------
    # Meta
    # --------------------
    current_title: str = ""
    current_company: str = ""
    location: str = ""

    #create engine
class FeatureEngineer:

    def extract(self, candidate: Candidate) -> CandidateFeatures:

        profile = candidate.get("profile", {})
        history = candidate.get("career_history", [])
        skills = candidate.get("skills", [])
        education = candidate.get("education", [])
        signals = candidate.get("redrob_signals", {})

        features = CandidateFeatures()

        features.years_experience = profile.get(
            "years_of_experience",
            0,
        )

        features.current_title = profile.get(
            "current_title",
            "",
        )

        features.current_company = profile.get(
            "current_company",
            "",
        )

        features.location = profile.get(
            "location",
            "",
        )

        self._career_features(history, features)

        self._skill_features(skills, features)

        self._education_features(education, features)

        self._behavior_features(signals, features)

        return features
    #create features
    def _career_features(self, history, features):

        if not history:
            return

        features.total_jobs = len(history)

        duration = 0

        for job in history:

            duration += job.get("duration_months", 0)

            company = job.get("company", "").lower()

            if company in PRODUCT_COMPANIES_NORMALIZED:
                features.product_company_count += 1

            if company in CONSULTING_COMPANIES_NORMALIZED:
                features.consulting_company_count += 1

        features.avg_job_duration = duration / max(
            1,
            len(history),
        )
    #skill feture
    def _skill_features(self, skills, features):

        if not skills:
            return

        llm_keywords = {
            "llms",
            "fine-tuning llms",
            "langchain",
            "langgraph",
            "rag",
            "transformers",
            "lora",
        }

        vector_keywords = {
            "milvus",
            "faiss",
            "pinecone",
            "qdrant",
            "vector databases",
        }

        cloud_keywords = {
            "aws",
            "azure",
            "gcp",
        }

        total_score = 0

        for skill in skills:

            name = skill.get("name", "").lower()

            duration = skill.get("duration_months", 0)

            endorsements = skill.get("endorsements", 0)

            proficiency = skill.get("proficiency", "").lower()

            score = 0

            if duration >= 12:
                score += 2

            elif duration >= 6:
                score += 1

            score += min(endorsements / 10, 5)

            if proficiency == "advanced":
                score += 3

            elif proficiency == "intermediate":
                score += 2

            else:
                score += 1

            total_score += score

            if name in AI_SKILLS_NORMALIZED:
                features.ai_skill_count += 1

            if any(word in name for word in llm_keywords):
                features.llm_score += score

            if any(word in name for word in vector_keywords):
                features.vector_db_score += score

            if any(word in name for word in cloud_keywords):
                features.cloud_score += score

        features.ai_skill_score = total_score
#behaviroul featuers
    def _behavior_features(self, signals, features):

        features.github_score = signals.get(
            "github_activity_score",
            0,
        )

        features.recruiter_response_rate = signals.get(
            "recruiter_response_rate",
            0,
        )

        features.interview_completion_rate = signals.get(
            "interview_completion_rate",
            0,
        )

        features.profile_completeness = signals.get(
            "profile_completeness_score",
            0,
        )

        features.notice_period = signals.get(
            "notice_period_days",
            90,
        )

        features.open_to_work = signals.get(
            "open_to_work_flag",
            False,
        )

        features.relocation = signals.get(
            "willing_to_relocate",
            False,
        )
#behaviorl featues
    def _behavior_features(self, signals, features):

        features.github_score = signals.get(
            "github_activity_score",
            0,
        )

        features.recruiter_response_rate = signals.get(
            "recruiter_response_rate",
            0,
        )

        features.interview_completion_rate = signals.get(
            "interview_completion_rate",
            0,
        )

        features.profile_completeness = signals.get(
            "profile_completeness_score",
            0,
        )

        features.notice_period = signals.get(
            "notice_period_days",
            90,
        )

        features.open_to_work = signals.get(
            "open_to_work_flag",
            False,
        )

        features.relocation = signals.get(
            "willing_to_relocate",
            False,
        )
   #education features 
    def _education_features(self, education, features):

        if not education:
            return

        best = education[0]

        features.education_tier = best.get(
            "tier",
            "unknown",
        )
    def career_dna(self, history):

        dna = []

        for job in history:

            title = job.get(
                "title",
                "",
            ).lower()

            if "ai" in title or "ml" in title:
                dna.append("AI")

            elif "data" in title:
                dna.append("DATA")

            elif "backend" in title:
                dna.append("BACKEND")

            elif "software" in title:
                dna.append("SOFTWARE")

            else:
                dna.append("OTHER")

        return " → ".join(dna)