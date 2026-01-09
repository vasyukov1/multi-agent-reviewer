def weak_label_from_rules(ad, rule_result):
    """
    Convert rule-based auditor output into pseudo-labels.
    Docstring for weak_label_from_rules
    
    :param ad: Description
    :param rule_result: Description
    """

    risk_score = rule_result["risk_score"]

    labels = {
        "scam": 0,
        "spam": 0,
        "illegal": 0,
        "low_info": 0,
    }

    for issue in rule_result["issues"]:
        if issue["code"] == "BANNED_WORD":
            labels["scam"] = 1
        if issue["code"] == "DESCRIPTION_TOO_SHORT":
            labels["low_info"] = 1
    
    return risk_score, list(labels.values())
