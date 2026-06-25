import json


def parse_candidate(candidate):

    profile = candidate["profile"]

    skills = [
        skill["name"].lower()
        for skill in candidate["skills"]
    ]

    career_text = " ".join(
        job["description"]
        for job in candidate["career_history"]
    )

    skill_text = " ".join(skills)

    full_text = " ".join([
        profile["headline"],
        profile["summary"],
        career_text,
        skill_text
    ])

    return {
        "candidate_id": candidate["candidate_id"],

        "experience_years":
            profile["years_of_experience"],

        "current_title":
            profile["current_title"],

        "skills":
            skills,

        "text":
            full_text,

        "github_score":
            candidate["redrob_signals"]
            ["github_activity_score"],

        "response_rate":
            candidate["redrob_signals"]
            ["recruiter_response_rate"],

        "saved_by_recruiters":
            candidate["redrob_signals"]
            ["saved_by_recruiters_30d"],

        "interview_rate":
            candidate["redrob_signals"]
            ["interview_completion_rate"]
    }


with open(
    "../data/sample_candidates.json",
    "r",
    encoding="utf-8"
) as f:

    candidates = json.load(f)

parsed = parse_candidate(candidates[0])

for k, v in parsed.items():
    print("\n")
    print(k)
    print(v)