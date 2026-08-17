RISK_LEVELS = {
    "low": 0,
    "medium": 1,
    "high": 2,
}


MAX_AUTO_RISK = 1


def requires_approval(tool):

    risk = tool.get(
        "risk",
        "high",
    )

    return (
        RISK_LEVELS[risk]
        > MAX_AUTO_RISK
    )