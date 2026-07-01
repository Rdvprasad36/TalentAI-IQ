"""
Reason Generation Module

Generates human-readable explanations for why
a candidate ranked highly.
"""

from __future__ import annotations


class ReasonGenerator:

    def generate(
        self,
        features,
        career,
        skill,
        behavior,
        semantic,
        confidence,
    ):

        reasons = []

        # Experience

        if features.years_experience >= 7:
            reasons.append(
                f"{features.years_experience:.1f} years of experience"
            )

        # Product Company

        if career.product_company_count > 0:
            reasons.append(
                "Product company experience"
            )

        # AI Roles

        if career.ai_roles > 0:
            reasons.append(
                "AI-focused career"
            )

        # LLM

        if skill.llm_skills > 0:
            reasons.append(
                "LLM expertise"
            )

        # Vector DB

        if skill.vector_db_skills > 0:
            reasons.append(
                "Vector Database experience"
            )

        # ML

        if skill.ml_skills > 0:
            reasons.append(
                "Strong ML background"
            )

        # GitHub

        if behavior.github_score >= 7:
            reasons.append(
                "High GitHub activity"
            )

        # Recruiter Interest

        if behavior.saved_by_recruiters >= 5:
            reasons.append(
                "Frequently shortlisted"
            )

        # Hiring Readiness

        if behavior.notice_period <= 30:
            reasons.append(
                "Immediate availability"
            )

        # Confidence

        if confidence.confidence_score >= 90:

            reasons.append(
                "High confidence profile"
            )

        elif confidence.confidence_score >= 75:

            reasons.append(
                "Reliable profile"
            )

        return ", ".join(reasons)
    