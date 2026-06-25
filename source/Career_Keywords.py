CAREER_KEYWORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "matching",
    "embeddings",
    "vector",
    "recommender",
    "information retrieval",
    "semantic search",
    "a/b testing",
    "evaluation",
    "ndcg",
    "mrr"
]
def get_career_score(candidate):

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

            score += 10

    return min(score, 100)