"""
Honeypot / AI Confidence Detector

Detects suspicious or weak candidate profiles and
computes an AI confidence score.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HoneypotResult:

    suspicious: bool = False

    confidence_score: float = 100

    reasons: list[str] | None = None


class HoneypotDetector:

    def analyze(
        self,
        candidate,
        features,
        career,
        skill,
        behavior,
    ):

        result = HoneypotResult(
            reasons=[],
        )

        score = 100

        # ------------------------------------------------
        # Too many AI skills but weak evidence
        # ------------------------------------------------

        if (
            features.ai_skill_count >= 10
            and skill.average_endorsements < 3
        ):

            score -= 20

            result.reasons.append(
                "Many AI skills but very low endorsements."
            )

        # ------------------------------------------------
        # AI skills but no AI roles
        # ------------------------------------------------

        if (
            features.ai_skill_count >= 8
            and career.ai_roles == 0
        ):

            score -= 15

            result.reasons.append(
                "Strong AI claims without AI job titles."
            )

        # ------------------------------------------------
        # Consulting only
        # ------------------------------------------------

        if career.consulting_only:

            score -= 15

            result.reasons.append(
                "Consulting-only career."
            )

        # ------------------------------------------------
        # Very low GitHub
        # ------------------------------------------------

        if (
            behavior.github_score < 2
            and skill.llm_skills >= 2
        ):

            score -= 10

            result.reasons.append(
                "LLM expertise with very low GitHub activity."
            )

        # ------------------------------------------------
        # Very short AI experience
        # ------------------------------------------------

        if (
            features.years_experience < 2
            and skill.llm_skills >= 3
        ):

            score -= 10

            result.reasons.append(
                "Claims advanced AI with little experience."
            )

        # ------------------------------------------------
        # Notice period
        # ------------------------------------------------

        if behavior.notice_period > 90:

            score -= 5

            result.reasons.append(
                "Very long notice period."
            )

        score = max(score, 0)

        result.confidence_score = score

        result.suspicious = score < 60

        return result
    