import json
import pickle

from tqdm import tqdm
from sentence_transformers import SentenceTransformer


def build_candidate_text(candidate):

    profile = candidate["profile"]

    headline = profile.get("headline", "")
    summary = profile.get("summary", "")

    skills = " ".join(
        s["name"]
        for s in candidate["skills"]
    )

    career = " ".join(
        j.get("description", "")
        for j in candidate["career_history"]
    )

    return f"{headline} {summary} {skills} {career}"


print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

texts = []
candidate_ids = []

with open(
    "../data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in tqdm(f):

        candidate = json.loads(line)

        texts.append(
            build_candidate_text(candidate)
        )

        candidate_ids.append(
            candidate["candidate_id"]
        )

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True
)

with open(
    "../models/embeddings.pkl",
    "wb"
) as f:

    pickle.dump(
        (
            candidate_ids,
            embeddings
        ),
        f
    )

print("Done.")