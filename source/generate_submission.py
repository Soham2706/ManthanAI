import json
import pickle
import numpy as np
import pandas as pd

from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# LOAD JOB DESCRIPTION
# =====================================================

print("Loading Job Description...")

doc = Document("../data/job_description.docx")
jd_text = "\n".join(p.text for p in doc.paragraphs)

# =====================================================
# LOAD MODEL
# =====================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

jd_embedding = model.encode([jd_text])

# =====================================================
# LOAD PRECOMPUTED EMBEDDINGS
# =====================================================

print("Loading embeddings...")

with open("../models/embeddings.pkl", "rb") as f:
    candidate_ids, embeddings = pickle.load(f)

candidate_index = {cid: idx for idx, cid in enumerate(candidate_ids)}

print("Embeddings loaded:", len(candidate_ids))

# =====================================================
# SEMANTIC RETRIEVAL
# =====================================================

print("Running semantic retrieval...")

similarities = cosine_similarity(jd_embedding, embeddings)[0]

TOP_K = min(5000, len(candidate_ids))
top_indices = np.argsort(similarities)[::-1][:TOP_K]

top_candidate_ids = set(candidate_ids[i] for i in top_indices)

print("Retrieved candidates:", len(top_candidate_ids))

# =====================================================
# KEYWORDS
# =====================================================

CAREER_KEYWORDS = [
    "retrieval", "ranking", "recommendation", "recommender",
    "search", "semantic search", "matching", "vector",
    "embedding", "milvus", "pinecone", "weaviate", "qdrant",
    "faiss", "evaluation", "ndcg", "mrr", "map",
    "ab testing", "production", "deployed",
    "real users", "marketplace", "information retrieval"
]

GOOD_TITLES = [
    "ai engineer", "machine learning engineer", "ml engineer",
    "nlp engineer", "search engineer", "retrieval engineer",
    "recommendation engineer", "applied scientist",
    "data scientist", "research engineer", "llm engineer"
]

BAD_TITLES = [
    "marketing", "hr", "designer", "writer", "sales"
]

# =====================================================
# SCORING FUNCTIONS
# =====================================================

def career_score(candidate):
    text = " ".join(j.get("description", "").lower()
                    for j in candidate["career_history"])
    return min(sum(5 for k in CAREER_KEYWORDS if k in text), 100)


def behavior_score(candidate):
    s = candidate["redrob_signals"]

    github = s.get("github_activity_score", 0)
    response = s.get("recruiter_response_rate", 0) * 100
    interview = s.get("interview_completion_rate", 0) * 100
    saved = s.get("saved_by_recruiters_30d", 0) * 5

    return min(
        github * 0.3 +
        response * 0.3 +
        interview * 0.3 +
        saved * 0.1,
        100
    )


def experience_score(candidate):
    y = candidate["profile"].get("years_of_experience", 0)

    if 5 <= y <= 9:
        return 100
    elif 4 <= y < 5:
        return 70
    elif 9 < y <= 12:
        return 60
    else:
        return 10


def title_adjustment(candidate):
    title = candidate["profile"].get("current_title", "").lower()

    for b in BAD_TITLES:
        if b in title:
            return -40

    for g in GOOD_TITLES:
        if g in title:
            return 15

    return 0


def role_rejection(candidate):
    title = candidate["profile"].get("current_title", "").lower()

    bad_roles = [
        "civil", "mechanical", "electrical", "operations",
        "marketing", "sales", "hr", "designer", "writer",
        "content", "accountant", "project manager",
        "business analyst", "customer support",
        "technical support", "call center"
    ]

    for r in bad_roles:
        if r in title:
            return -100

    return 0


def role_fit_bonus(candidate):
    text = candidate["profile"].get("current_title", "").lower() + " " + \
           " ".join(j.get("description", "").lower()
                    for j in candidate["career_history"])

    return min(sum(6 for k in CAREER_KEYWORDS if k in text), 60)


def retrieval_bonus(candidate):
    text = " ".join(j.get("description", "").lower()
                    for j in candidate["career_history"])

    keywords = [
        "retrieval", "ranking", "recommendation",
        "search", "matching", "vector",
        "embedding", "semantic search"
    ]

    return sum(10 for k in keywords if k in text)


def jd_alignment_bonus(candidate):
    text = " ".join(j.get("description", "").lower()
                    for j in candidate["career_history"])

    terms = [
        "retrieval", "ranking", "recommendation",
        "search", "matching", "vector",
        "embedding", "evaluation",
        "ndcg", "mrr", "semantic search"
    ]

    return sum(10 for t in terms if t in text)


# =====================================================
# RANKING PIPELINE
# =====================================================

print("Scoring candidates...")

results = []

with open("../data/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:
        candidate = json.loads(line)
        cid = candidate["candidate_id"]

        if cid not in top_candidate_ids:
            continue

        semantic = similarities[candidate_index[cid]] * 100

        career = career_score(candidate)
        behavior = behavior_score(candidate)
        experience = experience_score(candidate)

        adjustment = title_adjustment(candidate) + role_rejection(candidate)
        role_bonus = role_fit_bonus(candidate)
        retrieval = retrieval_bonus(candidate)
        alignment = jd_alignment_bonus(candidate)

        fit_score = (
            semantic * 0.45 +
            career * 0.35 +
            experience * 0.20
        )

        final_score = (
            fit_score * (0.8 + behavior / 500)
        ) + adjustment + role_bonus + retrieval + alignment

        title = candidate["profile"].get("current_title", "Unknown")
        years = candidate["profile"].get("years_of_experience", 0)

        reasoning = (
            f"{title} with {years:.1f} yrs experience; "
            f"semantic {semantic:.1f}; "
            f"career {career}; "
            f"behavior {behavior:.1f}; "
            f"JD alignment {alignment}"
        )

        results.append([cid, final_score, reasoning])

# =====================================================
# SORT RESULTS
# =====================================================

results.sort(key=lambda x: (-x[1], x[0]))

all_scores = [r[1] for r in results]
min_score, max_score = min(all_scores), max(all_scores)

# =====================================================
# BUILD SUBMISSION
# =====================================================

submission_rows = []

for rank, (cid, score, reasoning) in enumerate(results, start=1):

    if max_score == min_score:
        normalized = 1.0
    else:
        normalized = (score - min_score) / (max_score - min_score)

    submission_rows.append({
        "rank": rank,
        "candidate_id": cid,
        "score": round(normalized, 6),
        "reasoning": reasoning
    })

submission_df = pd.DataFrame(submission_rows)

# =====================================================
# SAVE FILE
# =====================================================

output_path = "../outputs/generate_submission.csv"
submission_df.to_csv(output_path, index=False)

print("\n✅ Submission created successfully!")
print("📁 Path:", output_path)
print("📊 Total candidates:", len(submission_df))

# =====================================================
# PREVIEW TOP 10
# =====================================================

print("\n🔥 TOP 10 CANDIDATES:\n")
print(submission_df.head(10))