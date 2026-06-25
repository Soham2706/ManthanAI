import json

from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------
# Candidate Text Builder
# ---------------------------

def build_candidate_text(candidate):

    profile = candidate["profile"]

    headline = profile.get("headline", "")
    summary = profile.get("summary", "")

    skills = " ".join(
        skill["name"]
        for skill in candidate["skills"]
    )

    career = " ".join(
        job.get("description", "")
        for job in candidate["career_history"]
    )

    return f"""
    {headline}
    {summary}
    {skills}
    {career}
    """


# ---------------------------
# Load JD
# ---------------------------

doc = Document("../data/job_description.docx")

jd_text = "\n".join(
    p.text for p in doc.paragraphs
)

# ---------------------------
# Embedding Model
# ---------------------------

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

jd_embedding = model.encode(
    [jd_text]
)

# ---------------------------
# Career Keywords
# ---------------------------

CAREER_KEYWORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "recommender",
    "search",
    "semantic search",
    "matching",
    "candidate matching",
    "embeddings",
    "vector",
    "vector database",
    "milvus",
    "pinecone",
    "weaviate",
    "qdrant",
    "faiss",
    "evaluation",
    "ndcg",
    "mrr",
    "map",
    "ab testing",
    "production",
    "deployed",
    "real users",
    "recommendation system",
    "marketplace",
    "information retrieval"
]


def career_score(candidate):

    text = ""

    for job in candidate["career_history"]:
        text += " "
        text += job.get(
            "description",
            ""
        ).lower()

    score = 0

    for keyword in CAREER_KEYWORDS:

        if keyword in text:
            score += 5

    return min(score, 100)


# ---------------------------
# Behavior Score
# ---------------------------

def behavior_score(candidate):

    signals = candidate["redrob_signals"]

    github = signals.get(
        "github_activity_score",
        0
    )

    response = (
        signals.get(
            "recruiter_response_rate",
            0
        ) * 100
    )

    interview = (
        signals.get(
            "interview_completion_rate",
            0
        ) * 100
    )

    saved = (
        signals.get(
            "saved_by_recruiters_30d",
            0
        ) * 5
    )

    score = (
        github * 0.3
        + response * 0.3
        + interview * 0.3
        + saved * 0.1
    )

    return min(score, 100)


# ---------------------------
# Title Penalty
# ---------------------------

BAD_TITLES = [
    "marketing",
    "hr",
    "designer",
    "writer",
    "sales"
]

GOOD_TITLES = [
    "ai engineer",
    "ml engineer",
    "machine learning engineer",
    "data scientist",
    "search engineer",
    "nlp engineer",
    "recommendation engineer",
    "retrieval engineer"
]

def title_penalty(candidate):

    title = candidate["profile"].get(
        "current_title",
        ""
    ).lower()

    for bad in BAD_TITLES:

        if bad in title:
            return -40

    return 0

def title_bonus(candidate):

    title = candidate["profile"].get(
        "current_title",
        ""
    ).lower()

    for good in GOOD_TITLES:

        if good in title:
            return 15

    return 0

# ---------------------------
# Experience Score
# ---------------------------

def experience_score(candidate):

    years = candidate["profile"].get(
        "years_of_experience",
        0
    )

    # JD wants roughly 5-9 years

    if 5 <= years <= 9:
        return 100

    if 4 <= years < 5:
        return 80

    if 9 < years <= 12:
        return 80

    return 50


# ---------------------------
# Semantic Score
# ---------------------------

def semantic_score(candidate):

    text = build_candidate_text(
        candidate
    )

    candidate_embedding = model.encode(
        [text]
    )

    similarity = cosine_similarity(
        jd_embedding,
        candidate_embedding
    )[0][0]

    return similarity * 100


# ---------------------------
# Final Score
# ---------------------------

def final_score(candidate):

    semantic = semantic_score(candidate)

    career = career_score(candidate)

    experience = experience_score(candidate)

    behavior = behavior_score(candidate)

    penalty = title_penalty(candidate)

    fit_score = (
        semantic * 0.45
        + career * 0.35
        + experience * 0.20
    )

    behavior_multiplier = (
        0.80 + (behavior / 500)
    )

    final = (
        fit_score * behavior_multiplier
        + penalty
    )

    return round(final, 4)

# ---------------------------
# Test Candidate
# ---------------------------

with open(
    "../data/sample_candidates.json",
    "r",
    encoding="utf-8"
) as f:

    candidates = json.load(f)

candidate = candidates[0]

print(
    "Candidate:",
    candidate["candidate_id"]
)

print(
    "Final Score:",
    final_score(candidate)
)