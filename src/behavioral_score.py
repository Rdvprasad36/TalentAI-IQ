"""
Behavioral Scoring Module
-------------------------

Scores candidate availability, recruiter engagement,
platform activity and hiring readiness.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BehavioralFeatures:

    github_score: float = 0
    recruiter_response_rate: float = 0
    interview_completion_rate: float = 0
    profile_completeness: float = 0
    profile_views: int = 0
    search_appearance: int = 0
    saved_by_recruiters: int = 0
    offer_acceptance_rate: float = 0
    notice_period: int = 90
    open_to_work: bool = False
    relocation: bool = False
    behavioral_score: float = 0


class BehavioralScorer:

    def analyze(self, signals):

        result = BehavioralFeatures()

        if not signals:
            return result

        result.github_score = signals.get(
            "github_activity_score",
            0,
        )

        result.recruiter_response_rate = signals.get(
            "recruiter_response_rate",
            0,
        )

        result.interview_completion_rate = signals.get(
            "interview_completion_rate",
            0,
        )

        result.profile_completeness = signals.get(
            "profile_completeness_score",
            0,
        )

        result.profile_views = signals.get(
            "profile_views_received_30d",
            0,
        )

        result.search_appearance = signals.get(
            "search_appearance_30d",
            0,
        )

        result.saved_by_recruiters = signals.get(
            "saved_by_recruiters_30d",
            0,
        )

        result.offer_acceptance_rate = signals.get(
            "offer_acceptance_rate",
            0,
        )

        result.notice_period = signals.get(
            "notice_period_days",
            90,
        )

        result.open_to_work = signals.get(
            "open_to_work_flag",
            False,
        )

        result.relocation = signals.get(
            "willing_to_relocate",
            False,
        )

        score = 0

        score += result.github_score * 0.5

        score += result.recruiter_response_rate * 10

        score += result.interview_completion_rate * 10

        score += result.profile_completeness * 0.2

        score += result.saved_by_recruiters * 1

        score += result.search_appearance * 0.02

        score += result.offer_acceptance_rate * 10

        if result.open_to_work:
            score += 8

        if result.relocation:
            score += 5

        if result.notice_period <= 30:
            score += 8

        elif result.notice_period <= 60:
            score += 4

        result.behavioral_score = min(score, 100)

        return result
    