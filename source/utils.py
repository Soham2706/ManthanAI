def build_candidate_text(candidate):

    profile = candidate["profile"]

    headline = profile.get(
        "headline",
        ""
    )

    summary = profile.get(
        "summary",
        ""
    )

    career = " ".join(
        job.get(
            "description",
            ""
        )
        for job in candidate["career_history"]
    )

    skills = " ".join(
        skill["name"]
        for skill in candidate["skills"]
    )

    return " ".join(
        [
            headline,
            summary,
            career,
            skills
        ]
    )