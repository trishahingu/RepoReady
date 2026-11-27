
def calculate_health_score(scan_results: dict) -> dict:
    """
    Calculate repository health score out of 100.
    """

    total_checks = len(scan_results)

    if total_checks == 0:
        return {
            "score": 0,
            "grade": "N/A",
            "found": 0,
            "missing": 0,
        }

    found = sum(
        1 for item in scan_results.values()
        if item["exists"]
    )

    missing = total_checks - found
    score = round((found / total_checks) * 100)

    if score >= 90:
        grade = "Excellent"
    elif score >= 75:
        grade = "Good"
    elif score >= 50:
        grade = "Needs Improvement"
    else:
        grade = "Poor"

    return {
        "score": score,
        "grade": grade,
        "found": found,
        "missing": missing,
    }
