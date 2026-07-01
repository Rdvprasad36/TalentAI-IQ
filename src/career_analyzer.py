"""
Career Analyzer
---------------

Analyzes candidate career history to understand
career quality, progression and relevance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.config import (
    PRODUCT_COMPANIES_NORMALIZED,
    CONSULTING_COMPANIES_NORMALIZED,
)

Candidate = dict[str, Any]


@dataclass(slots=True)
class CareerFeatures:

    total_jobs: int = 0

    avg_duration: float = 0

    product_company_count: int = 0

    consulting_company_count: int = 0

    ai_roles: int = 0

    backend_roles: int = 0

    data_roles: int = 0

    leadership_roles: int = 0

    stable_career: bool = False

    consulting_only: bool = False

    career_score: float = 0


class CareerAnalyzer:

    def analyze(self, history):

        result = CareerFeatures()

        if not history:
            return result

        result.total_jobs = len(history)

        total_duration = 0

        for job in history:

            title = job.get("title", "").lower()

            company = job.get("company", "").lower()

            duration = job.get("duration_months", 0)

            total_duration += duration

            if company in PRODUCT_COMPANIES_NORMALIZED:
                result.product_company_count += 1

            if company in CONSULTING_COMPANIES_NORMALIZED:
                result.consulting_company_count += 1

            if "ai" in title or "ml" in title:
                result.ai_roles += 1

            if "backend" in title:
                result.backend_roles += 1

            if "data" in title:
                result.data_roles += 1

            if (
                "lead" in title
                or "manager" in title
                or "architect" in title
                or "principal" in title
            ):
                result.leadership_roles += 1

        result.avg_duration = total_duration / max(1, result.total_jobs)

        result.stable_career = result.avg_duration >= 18

        result.consulting_only = (
            result.consulting_company_count > 0
            and result.product_company_count == 0
        )

        score = 0

        score += result.product_company_count * 10

        score += result.ai_roles * 12

        score += result.leadership_roles * 6

        if result.stable_career:
            score += 10

        if result.consulting_only:
            score += 8

        result.career_score = min(score, 100)

        return result
    
    