from __future__ import annotations

from dataclasses import dataclass

# -----------------------------
# Semantic Knowledge Base
# -----------------------------

SEMANTIC_GROUPS = {
    "llm": {
        "llm",
        "llms",
        "large language models",
        "transformers",
        "lora",
        "peft",
        "fine-tuning llms",
        "prompt engineering",
        "langchain",
        "langgraph",
        "rag",
    },

    "vector_database": {
        "vector database",
        "vector databases",
        "milvus",
        "pinecone",
        "faiss",
        "qdrant",
        "chromadb",
        "weaviate",
    },

    "machine_learning": {
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "keras",
        "scikit-learn",
        "xgboost",
        "lightgbm",
    },

    "nlp": {
        "nlp",
        "bert",
        "spacy",
        "huggingface",
        "speech recognition",
        "text classification",
    },

    "computer_vision": {
        "computer vision",
        "opencv",
        "image classification",
        "object detection",
        "yolo",
        "segment anything",
    },

    "cloud": {
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
    },
}


@dataclass(slots=True)
class SemanticResult:
    semantic_score: float = 0.0
    matched_groups: int = 0
    total_groups: int = 0
    coverage: float = 0.0
    matched_concepts: list[str] | None = None


class SemanticMatcher:

    def analyze(self, skills):

        result = SemanticResult()

        result.total_groups = len(SEMANTIC_GROUPS)

        result.matched_concepts = []

        candidate_skills = set()

        for skill in skills:
            candidate_skills.add(
                skill.get("name", "").lower()
            )

        matched = 0

        for group, values in SEMANTIC_GROUPS.items():

            if candidate_skills.intersection(values):

                matched += 1

                result.matched_concepts.append(group)

        result.matched_groups = matched
        result.coverage = matched / result.total_groups
        result.semantic_score = min(result.semantic_score, 100)

        return result