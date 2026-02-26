def assess_quality(c):
    total = 7
    present = 0
    missing = []

    checks = {
        "name": c.name,
        "email": c.email,
        "skills": c.skills["technical"],
        "education": c.education,
        "roles": c.roles,
        "location": c.location != "Unknown",
        "experience": c.experience_years > 0
    }

    for k, v in checks.items():
        if v:
            present += 1
        else:
            missing.append(k)

    return {
        "completeness_score": round(present / total, 2),
        "ambiguity_flags": [],
        "missing_sections": missing,
        "data_quality_issues": []
    }