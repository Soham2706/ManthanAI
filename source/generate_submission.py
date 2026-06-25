import json
import pickle
import numpy as np
import pandas as pd

from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# LOAD JD
# =====================================================

print("Loading Job Description...")

doc = Document("../data/job_description.docx")

jd_text = "\n".join(
    p.text for p in doc.paragraphs
)

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

jd_embedding = model.encode(
    [jd_text]
)

# =====================================================
# LOAD EMBEDDINGS
# =====================================================

print("Loading embeddings...")

with open(
    "../models/embeddings.pkl",
    "rb"
) as f:

    candidate_ids, embeddings = pickle.load(f)

print(
    "Embeddings loaded:",
    len(candidate_ids)
)

candidate_index = {
    cid: idx
    for idx, cid in enumerate(candidate_ids)
}

# =====================================================
# SEMANTIC RETRIEVAL
# =====================================================

print("Finding top candidates...")

similarities = cosine_similarity(
    jd_embedding,
    embeddings
)[0]

TOP_K = 5000

top_indices = np.argsort(
    similarities
)[::-1][:TOP_K]

top_candidate_ids = set(
    candidate_ids[i]
    for i in top_indices
)

print(
    "Retrieved:",
    len(top_candidate_ids),
    "candidates"
)

# =====================================================
# KEYWORDS
# =====================================================

CAREER_KEYWORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "recommender",
    "search",
    "semantic search",
    "matching",
    "vector",
    "embedding",
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
    "marketplace",
    "information retrieval"
]

GOOD_TITLES = [
    "ai engineer",
    "machine learning engineer",
    "ml engineer",
    "nlp engineer",
    "search engineer",
    "retrieval engineer",
    "recommendation engineer",
    "applied scientist",
    "data scientist",
    "research engineer",
    "applied ai engineer",
    "ranking engineer",
    "llm engineer"
]

BAD_TITLES = [
    "marketing",
    "hr",
    "designer",
    "writer",
    "sales"
]

# =====================================================
# ROLE FIT BONUS
# =====================================================

def role_fit_bonus(candidate):

    text = ""

    title = candidate["profile"].get(
        "current_title",
        ""
    ).lower()

    text += title

    for job in candidate["career_history"]:

        text += " "

        text += job.get(
            "description",
            ""
        ).lower()

    score = 0

    for keyword in CAREER_KEYWORDS:

        if keyword in text:
            score += 6

    return min(score, 60)

# =====================================================
# CAREER SCORE
# =====================================================

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

# =====================================================
# BEHAVIOR SCORE
# =====================================================

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

# =====================================================
# EXPERIENCE SCORE
# =====================================================

def experience_score(candidate):

    years = candidate["profile"].get(
        "years_of_experience",
        0
    )

    if 5 <= years <= 9:
        return 100

    elif 4 <= years < 5:
        return 70

    elif 9 < years <= 12:
        return 60

    elif years > 12:
        return 10

    else:
        return 10

# =====================================================
# TITLE ADJUSTMENT
# =====================================================

def title_adjustment(candidate):

    title = candidate["profile"].get(
        "current_title",
        ""
    ).lower()

    for bad in BAD_TITLES:

        if bad in title:
            return -40

    for good in GOOD_TITLES:

        if good in title:
            return 15

    return 0

# =====================================================
# ROLE REJECTION
# =====================================================

def role_rejection(candidate):

    title = candidate["profile"].get(
        "current_title",
        ""
    ).lower()

    bad_roles = [
        "civil",
        "mechanical",
        "electrical",
        "operations",
        "marketing",
        "sales",
        "hr",
        "designer",
        "writer",
        "content",
        "accountant",
        "project manager",
        "business analyst",
        "customer support",
        "support engineer",
        "customer success",
        "technical support",
        "call center"
    ]

    for role in bad_roles:

        if role in title:
            return -100

    return 0

# =====================================================
# JD ALIGNMENT BONUS
# =====================================================

def jd_alignment_bonus(candidate):

    text = ""
    print(candidate["candidate_id"])
    print(candidate["profile"]["current_title"])
    for job in candidate["career_history"]:
        print(job["description"])
        text += " "
        text += job.get(
            "description",
            ""
        ).lower()

    bonus_terms = [
        "retrieval",
        "ranking",
        "recommendation",
        "recommender",
        "search",
        "matching",
        "vector",
        "embedding",
        "evaluation",
        "ndcg",
        "mrr",
        "hybrid search",
        "semantic search",
        "candidate matching",
        "information retrieval"
    ]
    hits= sum(
        1
        for k in bonus_terms
        if k in text
    )
    return hits*10

    score = 0

    for term in bonus_terms:

        if term in text:
            score += 8

    return min(score, 50)

# =====================================================
# RANKING
# =====================================================

print("Ranking candidates...")
def retrieval_bonus(candidate):

    text = ""

    for job in candidate["career_history"]:

        text += " "

        text += job.get(
            "description",
            ""
        ).lower()

    keywords = [
        "retrieval",
        "ranking",
        "recommendation",
        "recommender",
        "search",
        "matching",
        "vector",
        "embedding",
        "semantic search",
        "information retrieval"
    ]

    hits = 0

    for keyword in keywords:

        if keyword in text:
            hits += 1

    return hits * 10

results = []

with open(
    "../data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        cid = candidate["candidate_id"]

        if cid not in top_candidate_ids:
            continue

        semantic = (
            similarities[
                candidate_index[cid]
            ] * 100
        )

        career = career_score(candidate)

        behavior = behavior_score(candidate)

        experience = experience_score(candidate)

        adjustment = (
            title_adjustment(candidate)
            + role_rejection(candidate)
        )
        retrieval = retrieval_bonus(
            candidate
        )
        alignment = jd_alignment_bonus(candidate)

        role_bonus = role_fit_bonus(candidate)

        fit_score = (
            semantic * 0.45
            + career * 0.35
            + experience * 0.20
        )

        final_score = (
            fit_score *
            (0.8 + behavior / 500)
        ) + adjustment + alignment + role_bonus + retrieval

        title = candidate["profile"].get(
            "current_title",
            "Unknown"
        )

        years = candidate["profile"].get(
            "years_of_experience",
            0
        )

        reasoning = (
            f"{title} with "
            f"{years:.1f} yrs experience; "
            f"semantic match {semantic:.1f}; "
            f"career relevance {career}; "
            f"behavior score {behavior:.1f}; "
            f"JD alignment {alignment}"
        )

        results.append([
            cid,
            final_score,
            reasoning
        ])

# =====================================================
# SORT RESULTS
# =====================================================

results.sort(
    key=lambda x: (-x[1], x[0])
    
)
all_scores = [r[1] for r in results]

min_score = min(all_scores)
max_score = max(all_scores)

# =====================================================
# BUILD SUBMISSION
# =====================================================

submission_rows = []

for rank, row in enumerate(
    results,
    start=1
):

    normalized_score = (
    (row[1] - min_score)
    /
    (max_score - min_score)
)

    submission_rows.append({
        "candidate_id": row[0],
        "rank": rank,
        "score": round(row[1] / 100, 6),
        "reasoning": row[2]
    })

submission = pd.DataFrame(
    submission_rows
)

# =====================================================
# SAVE
# =====================================================

submission.to_csv(
    "../outputs/final_submission.csv",
    index=False
)

print(
    "Saved:",
    len(submission),
    "candidates"
)

# =====================================================
# PREVIEW
# =====================================================

print("\nTOP 20 CANDIDATES\n")

print(
    submission.head(20)
)