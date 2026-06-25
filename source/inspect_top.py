# inspect_top.py

import json

target_ids = [
    "CAND_0008425",
    "CAND_0055905",
    "CAND_0033861"
]

with open(
    "../data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        if candidate["candidate_id"] in target_ids:

            print("\n")
            print("=" * 100)
            print(candidate["candidate_id"])
            print(candidate["profile"]["current_title"])
            print(candidate["profile"]["years_of_experience"])
            print(candidate["profile"]["headline"])

            print("\nSkills:")

            for skill in candidate["skills"][:20]:

                print(
                    skill["name"]
                )