TARGET_SKILLS = [
    "milvus",
    "pinecone",
    "weaviate",
    "qdrant",
    "faiss",
    "elasticsearch",
    "opensearch",
    "python",
    "llm",
    "fine-tuning",
    "lora",
    "embeddings",
    "ranking",
    "retrieval"
]
def get_skill_score(candidate):

    skills = [
        s["name"].lower()
        for s in candidate["skills"]
    ]

    score = 0

    for target in TARGET_SKILLS:

        if any(
            target in skill
            for skill in skills
        ):
            score += 7

    return min(score, 100)