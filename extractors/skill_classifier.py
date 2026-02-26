TECH = ["python", "sql", "docker", "aws", "machine learning"]
SOFT = ["communication", "leadership", "teamwork", "problem solving"]


def classify_skills(all_skills):
    tech = []
    soft = []
    other = []

    for s in all_skills:
        sl = s.lower()

        if sl in TECH:
            tech.append(s)
        elif sl in SOFT:
            soft.append(s)
        else:
            other.append(s)

    return {
        "technical": tech,
        "soft": soft,
        "other": other
    }