import json
from tqdm import tqdm


def load_candidates(path):

    candidates = []

    with open(path, "r", encoding="utf-8") as f:

        for line in tqdm(f):

            candidates.append(json.loads(line))

    return candidates


if __name__ == "__main__":

    candidates = load_candidates(
        "../data/candidates.jsonl"
    )

    print("Candidates Loaded:", len(candidates))

    print(candidates[0]["candidate_id"])