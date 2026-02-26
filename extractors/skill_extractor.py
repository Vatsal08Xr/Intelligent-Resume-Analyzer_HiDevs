import re


def _section(text, header):
    pattern = rf"{header}(.*?)(soft skills|education|experience|projects|certifications|$)"
    m = re.search(pattern, text.lower(), re.S)
    return m.group(1) if m else ""

def _clean_tokens(section_text):
    tokens = re.split(r"[,\n]", section_text)
    return [t.strip() for t in tokens if t.strip()]


def classify_skill(skill):
    """
    Smart rule-based classifier (NO hardcoding limits)
    """

    s = skill.lower()

    # technical patterns
    tech_keywords = [
        "sql", "js", "html", "css", "python", "java", "react", "node",
        "aws", "docker", "kubernetes", "linux", "git", "api", "flask",
        "django", "c++", "c#", "tensorflow", "pytorch"
    ]

    # soft patterns
    soft_keywords = [
        "communication", "team", "leadership", "management",
        "problem", "collaboration", "support", "presentation",
        "time", "adaptability"
    ]

    if any(k in s for k in tech_keywords):
        return "technical"

    if any(k in s for k in soft_keywords):
        return "soft"

    # fallback rule:
    # short words → technical (tools)
    # long phrases → soft
    if len(s.split()) <= 2:
        return "technical"

    return "soft"


def extract_skills(text):

    tech = []
    soft = []

    skill_text = _section(text, "skills")
    soft_text = _section(text, "soft skills")

    all_skills = _clean_tokens(skill_text) + _clean_tokens(soft_text)

    for skill in all_skills:
        category = classify_skill(skill)

        if category == "technical":
            tech.append(skill)

        else:
            soft.append(skill)

    return {
        "technical": sorted(set(tech)),
        "soft": sorted(set(soft))
    }