from heapq import heappush
from heapq import heappushpop
from src.preprocess import Preprocessor
from src.semantic_match import SemanticMatcher

import pandas as pd

from src.loader import CandidateLoader

from src.feature_engineering import FeatureEngineer

from src.career_analyzer import CareerAnalyzer

from src.skill_matcher import SkillMatcher

from src.behavioral_score import BehavioralScorer

from src.honeypot_detector import HoneypotDetector

from src.reasoning import ReasonGenerator

from src.scorer import Scorer

preprocessor = Preprocessor()
semantic_matcher = SemanticMatcher()

TOP_K = 100


loader = CandidateLoader(
    "data/candidates.jsonl"
)

feature_engineer = FeatureEngineer()

career_analyzer = CareerAnalyzer()

skill_matcher = SkillMatcher()

behavior_scorer = BehavioralScorer()

honeypot = HoneypotDetector()

reasoning = ReasonGenerator()

scorer = Scorer()

heap = []


for candidate in loader.stream_candidates():

    candidate = preprocessor.process(candidate)

    features = feature_engineer.extract(candidate)

    career = career_analyzer.analyze(
        candidate["career_history"]
    )

    skill = skill_matcher.analyze(
        candidate["skills"]
    )

    behavior = behavior_scorer.analyze(
        candidate["redrob_signals"]
    )

    semantic = semantic_matcher.analyze(
        candidate["skills"]
    )

    confidence = honeypot.analyze(
        candidate,
        features,
        career,
        skill,
        behavior,
    )

    score = scorer.score(
        features,
        career,
        skill,
        behavior,
        semantic,
    )

    reason = reasoning.generate(
        features,
        career,
        skill,
        behavior,
        semantic,
        confidence,
    )

    item = (
        score,
        candidate["candidate_id"],
        reason,
    )

    if len(heap) < TOP_K:

        heappush(
            heap,
            item,
        )

    else:

        heappushpop(
            heap,
            item,
        )


heap.sort(reverse=True)

rows = []

for rank, item in enumerate(
    heap,
    1,
):

    score, cid, reason = item

    rows.append(
    {
        "candidate_id": cid,
        "rank": rank,
        "score": round(score, 2),
        "reasoning": reason,
    }
)


df = pd.DataFrame(rows)

df.to_csv(
    "submission.csv",
    index=False,
)

print()

print("=" * 50)

print("Top 100 generated.")

print("submission.csv saved.")

print("=" * 50)
