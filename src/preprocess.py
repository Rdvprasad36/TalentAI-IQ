"""
Data Preprocessing Module
-------------------------

Cleans and normalizes candidate records before feature extraction.
"""

from __future__ import annotations

from copy import deepcopy

from src.config import (
    AI_SKILL_ALIASES,
    COMPANY_ALIASES,
    LOCATION_ALIASES,
)


class Preprocessor:

    def process(self, candidate: dict) -> dict:
        """
        Return a cleaned copy of the candidate.
        """

        candidate = deepcopy(candidate)

        self._normalize_profile(candidate)
        self._normalize_skills(candidate)
        self._normalize_career(candidate)
        self._fill_missing(candidate)

        return candidate

    # --------------------------------------------------

    def _normalize_profile(self, candidate):

        profile = candidate.get("profile", {})

        profile["current_title"] = (
            profile.get("current_title", "")
            .strip()
        )

        profile["headline"] = (
            profile.get("headline", "")
            .strip()
        )

        profile["summary"] = (
            profile.get("summary", "")
            .strip()
        )

        location = profile.get("location", "").strip()

        if location.lower() in LOCATION_ALIASES:
            location = LOCATION_ALIASES[location.lower()]

        profile["location"] = location

    # --------------------------------------------------

    def _normalize_skills(self, candidate):

        skills = candidate.get("skills", [])

        for skill in skills:

            name = skill.get("name", "").strip()

            key = name.lower()

            if key in AI_SKILL_ALIASES:
                name = AI_SKILL_ALIASES[key]

            skill["name"] = name

            skill["proficiency"] = (
                skill.get("proficiency", "")
                .strip()
                .lower()
            )

            skill["duration_months"] = skill.get(
                "duration_months",
                0,
            )

            skill["endorsements"] = skill.get(
                "endorsements",
                0,
            )

    # --------------------------------------------------

    def _normalize_career(self, candidate):

        history = candidate.get(
            "career_history",
            [],
        )

        for job in history:

            company = job.get(
                "company",
                "",
            ).strip()

            key = company.lower()

            if key in COMPANY_ALIASES:
                company = COMPANY_ALIASES[key]

            job["company"] = company

            job["title"] = (
                job.get("title", "")
                .strip()
            )

            job["industry"] = (
                job.get("industry", "")
                .strip()
            )

    # --------------------------------------------------

    def _fill_missing(self, candidate):

        profile = candidate.setdefault(
            "profile",
            {},
        )

        profile.setdefault(
            "years_of_experience",
            0,
        )

        profile.setdefault(
            "location",
            "",
        )

        candidate.setdefault(
            "skills",
            [],
        )

        candidate.setdefault(
            "career_history",
            [],
        )

        candidate.setdefault(
            "education",
            [],
        )

        candidate.setdefault(
            "redrob_signals",
            {},
        )
      