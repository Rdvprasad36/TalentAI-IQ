"""
Final Scoring Engine

Combines all engineered features into one final
candidate score.
"""

from __future__ import annotations

from src.config import (
    TITLE_WEIGHT,
    SKILL_WEIGHT,
    EXPERIENCE_WEIGHT,
    BEHAVIOR_WEIGHT,
    LOCATION_WEIGHT,
)


class Scorer:

 def score(
    self,
    features,
    career,
    skill,
    behavior,
    semantic,
):

    score = 0.0

    # -------------------------
    # Title Score
    # -------------------------

    title = features.current_title.lower()

    if "ai engineer" in title:
        title_score = 100

    elif "machine learning" in title:
        title_score = 95

    elif "ml engineer" in title:
        title_score = 92

    elif "data scientist" in title:
        title_score = 88

    elif "backend" in title:
        title_score = 70

    elif "software engineer" in title:
        title_score = 60

    else:
        title_score = 35

    score += title_score * TITLE_WEIGHT

    # -------------------------
    # Skill Score
    # -------------------------

    score += min(skill.skill_score, 100) * SKILL_WEIGHT

    # -------------------------
    # Semantic Understanding
    # -------------------------

    score += min(semantic.semantic_score, 100) * 0.10

    # -------------------------
    # Career
    # -------------------------

    score += min(career.career_score, 100) * EXPERIENCE_WEIGHT

    # -------------------------
    # Behaviour
    # -------------------------

    score += min(behavior.behavioral_score, 100) * BEHAVIOR_WEIGHT

    # -------------------------
    # Location
    # -------------------------

    location = features.location.lower()

    if any(city in location for city in
           ["bangalore", "bengaluru"]):

        location_score = 100

    elif any(city in location for city in
             ["hyderabad"]):

        location_score = 95

    elif any(city in location for city in
             ["pune", "noida"]):

        location_score = 90

    else:
        location_score = 70

    score += location_score * LOCATION_WEIGHT

    # =====================================================
    # Recruiter Intelligence Bonuses
    # =====================================================

    # LLM + Vector DB Engineer

    if (
        "llm" in semantic.matched_concepts and
        "vector_database" in semantic.matched_concepts
    ):
        score += 8

    # Broad AI profile

    if semantic.matched_groups >= 4:
        score += 6

    # Product company experience

    if career.product_company_count > 0:
        score += 7

    # Multiple AI roles

    if career.ai_roles >= 2:
        score += 5

    # Strong GitHub

    if behavior.github_score >= 8:
        score += 4

    # Recruiter interest

    if behavior.saved_by_recruiters >= 5:
        score += 3

    # =====================================================
    # Penalties
    # =====================================================

    if career.consulting_only:
        score -= 8

    if skill.keyword_stuffing:
        score -= 10

    if features.years_experience < 2:
        score -= 5

    score = min(score, 100)
    return round(score, 2)