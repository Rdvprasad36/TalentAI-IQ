"""
Central configuration for the Redrob AI Hiring Challenge ranker.

Design goals:
  - Multi-JD: swap ranking profiles without code changes
  - Skill ontology: alias → canonical → parent hierarchy for robust matching
  - Company / education tiers: differentiated hiring signals
  - Performance knobs: streaming batches + heap-based top-K selection
"""

from __future__ import annotations

from typing import Final, TypedDict


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


class JDProfile(TypedDict):
    """Per-job-description scoring profile. Component weights must sum to 1.0."""

    title_weight: float
    skill_weight: float
    behavior_weight: float
    experience_weight: float
    location_weight: float
    education_weight: float
    min_years_experience: float
    max_years_experience: float
    ideal_years_experience: float
    preferred_locations: tuple[str, ...]
    target_skills: tuple[str, ...]


# ---------------------------------------------------------------------------
# Active JD selection
# ---------------------------------------------------------------------------

DEFAULT_JD: Final[str] = "AI_ENGINEER"

JD_CONFIG: Final[dict[str, JDProfile]] = {
    "AI_ENGINEER": {
        # Original weights rescaled to make room for education (5%).
        "title_weight": 0.285,
        "skill_weight": 0.24,
        "behavior_weight": 0.19,
        "experience_weight": 0.14,
        "location_weight": 0.095,
        "education_weight": 0.05,
        "min_years_experience": 5.0,
        "max_years_experience": 9.0,
        "ideal_years_experience": 7.0,
        "preferred_locations": (
            "Pune",
            "Noida",
            "Bangalore",
            "Hyderabad",
            "Delhi NCR",
            "Mumbai",
        ),
        "target_skills": (
            "Python",
            "Machine Learning",
            "Deep Learning",
            "LLMs",
            "Transformers",
            "PyTorch",
            "TensorFlow",
            "Scikit-learn",
            "LangGraph",
            "LangChain",
            "RAG",
            "Vector Databases",
            "FAISS",
            "Qdrant",
            "Milvus",
            "Pinecone",
            "Embeddings",
            "Ranking",
            "Retrieval",
            "FastAPI",
            "Docker",
            "Kubernetes",
            "AWS",
            "Azure",
            "GCP",
            "Git",
        ),
    },
    # Placeholder for future JDs — copy AI_ENGINEER and tune weights/skills.
    # "DATA_ENGINEER": { ... },
}


def get_jd_config(jd_key: str = DEFAULT_JD) -> JDProfile:
    """Return the scoring profile for a job description key."""
    if jd_key not in JD_CONFIG:
        known = ", ".join(sorted(JD_CONFIG))
        raise KeyError(f"Unknown JD key {jd_key!r}. Available: {known}")
    return JD_CONFIG[jd_key]


# Active config shortcut used by the ranker pipeline.
config: JDProfile = get_jd_config(DEFAULT_JD)

# Backward-compatible weight exports (derived from active JD).
TITLE_WEIGHT: Final[float] = config["title_weight"]
SKILL_WEIGHT: Final[float] = config["skill_weight"]
BEHAVIOR_WEIGHT: Final[float] = config["behavior_weight"]
EXPERIENCE_WEIGHT: Final[float] = config["experience_weight"]
LOCATION_WEIGHT: Final[float] = config["location_weight"]
EDUCATION_WEIGHT: Final[float] = config["education_weight"]

RANKING_WEIGHTS: Final[dict[str, float]] = {
    "title": TITLE_WEIGHT,
    "skill": SKILL_WEIGHT,
    "behavior": BEHAVIOR_WEIGHT,
    "experience": EXPERIENCE_WEIGHT,
    "location": LOCATION_WEIGHT,
    "education": EDUCATION_WEIGHT,
}

# ---------------------------------------------------------------------------
# Global constants
# ---------------------------------------------------------------------------

# heapq maintains the top-N candidates during streaming scoring.
HEAP_SIZE: Final[int] = 100
TOP_K: Final[int] = HEAP_SIZE  # alias — challenge spec requires exactly 100 rows

PREFERRED_NOTICE_PERIOD_DAYS: Final[int] = 30
ACCEPTABLE_NOTICE_PERIOD_DAYS: Final[int] = 60
MIN_TRUSTED_SKILL_DURATION_MONTHS: Final[int] = 12
KEYWORD_STUFFING_SKILL_COUNT_THRESHOLD: Final[int] = 15
KEYWORD_STUFFING_ENDORSEMENT_RATIO_THRESHOLD: Final[float] = 0.15

MIN_SCORE: Final[float] = 0.0
MAX_SCORE: Final[float] = 1.0

DEFAULT_CANDIDATES_PATH: Final[str] = "data/candidates.jsonl"
DEFAULT_OUTPUT_PATH: Final[str] = "submission.csv"

# ---------------------------------------------------------------------------
# Embedding model (used by semantic_match.py)
# ---------------------------------------------------------------------------

MODEL_NAME: Final[str] = "all-MiniLM-L6-v2"
EMBEDDING_BATCH_SIZE: Final[int] = 256

# ---------------------------------------------------------------------------
# Performance / memory
# ---------------------------------------------------------------------------

BATCH_SIZE: Final[int] = 5000
STREAMING: Final[bool] = True
MAX_MEMORY_MB: Final[int] = 512

# ---------------------------------------------------------------------------
# Skill ontology
# ---------------------------------------------------------------------------
# Canonical skill → surface-form aliases (all lowercase).
# Matchers normalize input, look up alias → canonical, then walk SKILL_HIERARCHY
# upward for partial-credit scoring (e.g. "ml" → Machine Learning → AI).

SKILL_ONTOLOGY: Final[dict[str, tuple[str, ...]]] = {
    "Artificial Intelligence": (
        "artificial intelligence",
        "ai engineering",
        "ai/ml",
    ),
    "AI": (
        "ai",
        "applied ai",
        "ai systems",
    ),
    "Machine Learning": (
        "machine learning",
        "ml",
        "supervised learning",
        "unsupervised learning",
        "classical ml",
    ),
    "Deep Learning": (
        "deep learning",
        "dl",
        "neural networks",
        "neural network",
        "cnn",
        "rnn",
    ),
    "Python": (
        "python",
        "python3",
        "py",
        "python 3",
    ),
    "LLMs": (
        "llms",
        "llm",
        "large language models",
        "large language model",
        "generative ai",
        "gen ai",
    ),
    "Transformers": (
        "transformers",
        "transformer models",
        "attention mechanism",
        "bert",
        "gpt",
    ),
    "PyTorch": (
        "pytorch",
        "py torch",
        "torch",
    ),
    "TensorFlow": (
        "tensorflow",
        "tensor flow",
        "tf",
        "keras",
    ),
    "Scikit-learn": (
        "scikit-learn",
        "scikit learn",
        "sklearn",
        "sk learn",
    ),
    "LangGraph": (
        "langgraph",
        "lang graph",
    ),
    "LangChain": (
        "langchain",
        "lang chain",
    ),
    "RAG": (
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
    ),
    "Vector Databases": (
        "vector databases",
        "vector database",
        "vector db",
        "vector store",
        "vector search",
    ),
    "FAISS": ("faiss",),
    "Qdrant": ("qdrant",),
    "Milvus": ("milvus",),
    "Pinecone": ("pinecone",),
    "Embeddings": (
        "embeddings",
        "embedding models",
        "sentence embeddings",
        "dense retrieval",
    ),
    "Ranking": (
        "ranking",
        "learning to rank",
        "ltr",
        "re-ranking",
        "reranking",
    ),
    "Retrieval": (
        "retrieval",
        "information retrieval",
        "ir",
        "hybrid search",
        "semantic search",
    ),
    "FastAPI": (
        "fastapi",
        "fast api",
    ),
    "Docker": (
        "docker",
        "containerization",
        "containers",
    ),
    "Kubernetes": (
        "kubernetes",
        "k8s",
        "kube",
    ),
    "AWS": (
        "aws",
        "amazon web services",
        "amazon aws",
        "ec2",
        "s3",
    ),
    "Azure": (
        "azure",
        "microsoft azure",
        "azure ml",
    ),
    "GCP": (
        "gcp",
        "google cloud",
        "google cloud platform",
        "google cloud platform gcp",
    ),
    "Git": (
        "git",
        "github",
        "gitlab",
        "version control",
    ),
    "NLP": (
        "nlp",
        "natural language processing",
        "text mining",
    ),
}

# Parent links: child canonical → parent canonical (root skills have no entry).
SKILL_HIERARCHY: Final[dict[str, str]] = {
    "Machine Learning": "AI",
    "Deep Learning": "AI",
    "LLMs": "AI",
    "Transformers": "Deep Learning",
    "NLP": "AI",
    "RAG": "Retrieval",
    "Retrieval": "AI",
    "Embeddings": "Retrieval",
    "Ranking": "Retrieval",
    "FAISS": "Vector Databases",
    "Qdrant": "Vector Databases",
    "Milvus": "Vector Databases",
    "Pinecone": "Vector Databases",
    "Vector Databases": "Retrieval",
    "LangChain": "LLMs",
    "LangGraph": "LangChain",
    "PyTorch": "Deep Learning",
    "TensorFlow": "Deep Learning",
    "Scikit-learn": "Machine Learning",
    "AI": "Artificial Intelligence",
}

# Reverse index: normalized alias → canonical skill name.
def _build_skill_alias_index() -> dict[str, str]:
    index = {
        alias: canonical
        for canonical, aliases in SKILL_ONTOLOGY.items()
        for alias in aliases
    }
    for canonical in SKILL_ONTOLOGY:
        index.setdefault(canonical.lower(), canonical)
    index.setdefault("ml", "Machine Learning")
    return index


SKILL_ALIAS_INDEX: Final[dict[str, str]] = _build_skill_alias_index()

AI_SKILLS: Final[tuple[str, ...]] = config["target_skills"]
AI_SKILLS_NORMALIZED: Final[frozenset[str]] = frozenset(
    skill.lower() for skill in AI_SKILLS
)


def resolve_skill(raw: str) -> str | None:
    """Map a raw skill string to its canonical ontology name."""
    normalized = raw.strip().lower()
    if not normalized:
        return None
    return SKILL_ALIAS_INDEX.get(normalized)


def skill_ancestors(canonical: str) -> tuple[str, ...]:
    """Return (canonical, parent, grandparent, …) walking SKILL_HIERARCHY."""
    chain: list[str] = [canonical]
    seen: set[str] = {canonical}
    current = canonical
    while current in SKILL_HIERARCHY:
        parent = SKILL_HIERARCHY[current]
        if parent in seen:
            break
        chain.append(parent)
        seen.add(parent)
        current = parent
    return tuple(chain)


# ---------------------------------------------------------------------------
# Company tiers
# ---------------------------------------------------------------------------
# Google ≠ Swiggy — tier reflects hiring-signal strength, not just "product".

TIER1_PRODUCT: Final[tuple[str, ...]] = (
    "Google",
    "Microsoft",
    "Amazon",
    "OpenAI",
    "Meta",
    "Netflix",
)

TIER2_PRODUCT: Final[tuple[str, ...]] = (
    "Uber",
    "Atlassian",
    "Flipkart",
)

STARTUPS: Final[tuple[str, ...]] = (
    "Swiggy",
    "Zomato",
    "Razorpay",
    "PhonePe",
)

CONSULTING: Final[tuple[str, ...]] = (
    "Accenture",
    "Capgemini",
)

SERVICES: Final[tuple[str, ...]] = (
    "TCS",
    "Infosys",
    "Wipro",
    "Cognizant",
    "HCL",
    "Tech Mahindra",
    "LTIMindtree",
)

MNC: Final[tuple[str, ...]] = (
    # Large multinational employers outside the tier-1 product set.
    "IBM",
    "Oracle",
    "SAP",
    "Salesforce",
    "Adobe",
    "Intel",
    "Samsung",
    "Siemens",
)

COMPANY_TIERS: Final[dict[str, tuple[str, ...]]] = {
    "tier1_product": TIER1_PRODUCT,
    "tier2_product": TIER2_PRODUCT,
    "startups": STARTUPS,
    "consulting": CONSULTING,
    "services": SERVICES,
    "mnc": MNC,
}

# Relative career-quality multiplier per tier (1.0 = strongest signal).
COMPANY_TIER_SCORES: Final[dict[str, float]] = {
    "tier1_product": 1.00,
    "tier2_product": 0.85,
    "startups": 0.80,
    "mnc": 0.75,
    "consulting": 0.55,
    "services": 0.45,
}

COMPANY_ALIASES: Final[dict[str, str]] = {
    "tata consultancy services": "TCS",
    "tcs ltd": "TCS",
    "facebook": "Meta",
    "aws": "Amazon",
    "lti mindtree": "LTIMindtree",
    "lti": "LTIMindtree",
    "mindtree": "LTIMindtree",
    "hcl technologies": "HCL",
    "tech mahindra ltd": "Tech Mahindra",
}

# Legacy flat lists (backward compatible).
PRODUCT_COMPANIES: Final[tuple[str, ...]] = TIER1_PRODUCT + TIER2_PRODUCT + STARTUPS
CONSULTING_COMPANIES: Final[tuple[str, ...]] = CONSULTING + SERVICES

_COMPANY_TO_TIER: Final[dict[str, str]] = {
    company.lower(): tier
    for tier, companies in COMPANY_TIERS.items()
    for company in companies
}

PRODUCT_COMPANIES_NORMALIZED: Final[frozenset[str]] = frozenset(
    company.lower() for company in PRODUCT_COMPANIES
)
CONSULTING_COMPANIES_NORMALIZED: Final[frozenset[str]] = frozenset(
    company.lower() for company in CONSULTING_COMPANIES
)


def resolve_company(raw: str) -> str:
    """Normalize employer name via alias table."""
    normalized = raw.strip().lower()
    for alias, canonical in COMPANY_ALIASES.items():
        if alias in normalized:
            return canonical
    return raw.strip()


def get_company_tier(company: str) -> str | None:
    """Return tier key (e.g. 'tier1_product') or None if unknown."""
    canonical = resolve_company(company)
    return _COMPANY_TO_TIER.get(canonical.lower())


# ---------------------------------------------------------------------------
# Education tiers
# ---------------------------------------------------------------------------

EDUCATION_TIER_IIT: Final[tuple[str, ...]] = (
    "Indian Institute of Technology",
    "IIT Bombay",
    "IIT Delhi",
    "IIT Madras",
    "IIT Kanpur",
    "IIT Kharagpur",
    "IIT Roorkee",
    "IIT Guwahati",
    "IIT Hyderabad",
    "IIT Indore",
    "IIT BHU",
    "IIT Ropar",
    "IIT Gandhinagar",
    "IIT Patna",
    "IIT Bhubaneswar",
    "IIT Mandi",
    "IIT Jodhpur",
    "IIT Palakkad",
    "IIT Tirupati",
    "IIT Dhanbad",
    "IIT Goa",
    "IIT Jammu",
    "IIT Dharwad",
)

EDUCATION_TIER_NIT: Final[tuple[str, ...]] = (
    "National Institute of Technology",
    "NIT Trichy",
    "NIT Warangal",
    "NIT Surathkal",
    "NIT Calicut",
    "NIT Rourkela",
    "NIT Allahabad",
    "NIT Kurukshetra",
    "NIT Durgapur",
    "NIT Jaipur",
    "NIT Nagpur",
    "NIT Silchar",
    "NIT Jalandhar",
    "NIT Hamirpur",
    "NIT Meghalaya",
)

EDUCATION_TIER_IIIT: Final[tuple[str, ...]] = (
    "International Institute of Information Technology",
    "IIIT Hyderabad",
    "IIIT Bangalore",
    "IIIT Delhi",
    "IIIT Allahabad",
    "IIIT Pune",
    "IIIT Sri City",
    "IIIT Vadodara",
)

EDUCATION_TIER_BITS: Final[tuple[str, ...]] = (
    "Birla Institute of Technology and Science",
    "BITS Pilani",
    "BITS Goa",
    "BITS Hyderabad",
)

EDUCATION_TIER_TOP_STATE: Final[tuple[str, ...]] = (
    "Delhi Technological University",
    "DTU",
    "NSUT",
    "Netaji Subhas University of Technology",
    "Jadavpur University",
    "COEP",
    "College of Engineering Pune",
    "VIT",
    "Vellore Institute of Technology",
    "Manipal Institute of Technology",
    "PES University",
    "RV College of Engineering",
    "MS Ramaiah Institute of Technology",
    "Anna University",
    "Osmania University",
    "JNTU",
)

EDUCATION_TIERS: Final[dict[str, tuple[str, ...]]] = {
    "iit": EDUCATION_TIER_IIT,
    "nit": EDUCATION_TIER_NIT,
    "iiit": EDUCATION_TIER_IIIT,
    "bits": EDUCATION_TIER_BITS,
    "top_state": EDUCATION_TIER_TOP_STATE,
}

# Score contribution for education tier (used with EDUCATION_WEIGHT).
EDUCATION_TIER_SCORES: Final[dict[str, float]] = {
    "iit": 1.00,
    "nit": 0.85,
    "iiit": 0.90,
    "bits": 0.88,
    "top_state": 0.70,
    "tier_1": 0.95,  # schema tier field fallback
    "tier_2": 0.75,
    "tier_3": 0.55,
    "tier_4": 0.35,
    "unknown": 0.40,
}

_EDUCATION_ALIAS_INDEX: Final[dict[str, str]] = {
    institution.lower(): tier
    for tier, institutions in EDUCATION_TIERS.items()
    for institution in institutions
}


def get_education_tier(institution: str) -> str | None:
    """Match institution name to education tier key."""
    normalized = institution.strip().lower()
    for alias, tier in _EDUCATION_ALIAS_INDEX.items():
        if alias in normalized:
            return tier
    if normalized.startswith("iit "):
        return "iit"
    if normalized.startswith("nit "):
        return "nit"
    if normalized.startswith("iiit"):
        return "iiit"
    if "bits" in normalized:
        return "bits"
    return None


# ---------------------------------------------------------------------------
# Target locations
# ---------------------------------------------------------------------------

TARGET_LOCATIONS: Final[tuple[str, ...]] = config["preferred_locations"]

LOCATION_ALIASES: Final[dict[str, str]] = {
    "bengaluru": "Bangalore",
    "bangalore urban": "Bangalore",
    "gurugram": "Delhi NCR",
    "gurgaon": "Delhi NCR",
    "delhi": "Delhi NCR",
    "new delhi": "Delhi NCR",
    "ncr": "Delhi NCR",
    "greater noida": "Noida",
    "hyderabad": "Hyderabad",
    "secunderabad": "Hyderabad",
    "bombay": "Mumbai",
    "pune": "Pune",
    "noida": "Noida",
}

TARGET_LOCATIONS_NORMALIZED: Final[frozenset[str]] = frozenset(
    loc.lower() for loc in TARGET_LOCATIONS
)

# ---------------------------------------------------------------------------
# Penalty values
# ---------------------------------------------------------------------------
# Multiplicative score reduction: adjusted = base * (1.0 - penalty).

PENALTY_KEYWORD_STUFFING: Final[float] = 0.45
PENALTY_CONSULTING_ONLY: Final[float] = 0.25
PENALTY_TIMELINE_MISMATCH: Final[float] = 0.50
PENALTY_FAKE_AI_PROFILE: Final[float] = 0.40
PENALTY_DUPLICATE_EXPERIENCE: Final[float] = 0.35

PENALTIES: Final[dict[str, float]] = {
    "keyword_stuffing": PENALTY_KEYWORD_STUFFING,
    "consulting_only": PENALTY_CONSULTING_ONLY,
    "timeline_mismatch": PENALTY_TIMELINE_MISMATCH,
    "fake_ai_profile": PENALTY_FAKE_AI_PROFILE,
    "duplicate_experience": PENALTY_DUPLICATE_EXPERIENCE,
}

# ---------------------------------------------------------------------------
# Validation (import-time sanity checks)
# ---------------------------------------------------------------------------

for _jd_key, _profile in JD_CONFIG.items():
    _fields = (
        "title_weight",
        "skill_weight",
        "behavior_weight",
        "experience_weight",
        "location_weight",
        "education_weight",
    )
    _sum = sum(_profile[field] for field in _fields)
    if abs(_sum - 1.0) > 1e-9:
        raise ValueError(f"JD_CONFIG[{_jd_key!r}] weights must sum to 1.0, got {_sum:.6f}")

for _name, _value in PENALTIES.items():
    if not 0.0 <= _value <= 1.0:
        raise ValueError(f"PENALTIES[{_name!r}] must be in [0, 1], got {_value}")
    
# ============================
# Preprocessor Aliases
# ============================

AI_SKILL_ALIASES = {
    "llm": "LLMs",
    "large language models": "LLMs",
    "lang chain": "LangChain",
    "lang graph": "LangGraph",
    "vector db": "Vector Databases",
    "vector database": "Vector Databases",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "py torch": "PyTorch",
    "tensor flow": "TensorFlow",
    "amazon web services": "AWS",
    "google cloud platform": "GCP",
    "microsoft azure": "Azure",
}

COMPANY_ALIASES = {
    "tata consultancy services": "TCS",
    "facebook": "Meta",
    "aws": "Amazon",
    "mindtree": "LTIMindtree",
    "lti": "LTIMindtree",
    "lti mindtree": "LTIMindtree",
}

LOCATION_ALIASES = {
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "gurgaon": "Delhi NCR",
    "gurugram": "Delhi NCR",
    "delhi": "Delhi NCR",
    "new delhi": "Delhi NCR",
    "greater noida": "Noida",
    "bombay": "Mumbai",
    "secunderabad": "Hyderabad",
}
