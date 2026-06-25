def get_behavior_score(candidate):

    signals = candidate["redrob_signals"]

    github = signals.get(
        "github_activity_score",
        0
    )

    response_rate = (
        signals.get(
            "recruiter_response_rate",
            0
        ) * 100
    )

    interview_rate = (
        signals.get(
            "interview_completion_rate",
            0
        ) * 100
    )

    recruiter_interest = (
        signals.get(
            "saved_by_recruiters_30d",
            0
        ) * 5
    )

    score = (
        0.30 * github +
        0.30 * response_rate +
        0.25 * interview_rate +
        0.15 * recruiter_interest
    )

    return score