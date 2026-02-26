import re
import json
import sys
import calendar
from datetime import datetime


# ==============================
# Helpers
# ==============================

MONTHS = {
    "jan":1,"january":1,
    "feb":2,"february":2,
    "mar":3,"march":3,
    "apr":4,"april":4,
    "may":5,
    "jun":6,"june":6,
    "jul":7,"july":7,
    "aug":8,"august":8,
    "sep":9,"september":9,
    "oct":10,"october":10,
    "nov":11,"november":11,
    "dec":12,"december":12
}


def clean_text(text):
    """Normalize weird characters like \u2013"""
    return (
        text.replace("\u2013", "-")
            .replace("–", "-")
            .replace("—", "-")
    )


def get_section(text, header):
    """
    Returns text between HEADER and next ALL-CAPS header.
    Safe for multi-line sections like certifications.
    """

    lines = text.splitlines()
    capture = False
    buffer = []

    for line in lines:
        stripped = line.strip()

        # start capturing
        if stripped.upper() == header.upper():
            capture = True
            continue

        if capture:
            # stop at next header (all caps words like EXPERIENCE, SKILLS, etc)
            if stripped.isupper() and len(stripped.split()) <= 3:
                break

            buffer.append(line)

    return "\n".join(buffer)


# ==============================
# Basic fields
# ==============================

def extract_name(text):
    return text.splitlines()[0].strip()


def extract_email(text):
    m = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return m.group(0) if m else None


def extract_phone(text):
    m = re.search(r'\+?\d[\d\s]{8,}', text)
    return m.group(0).strip() if m else None

def extract_location(text):
    lines = text.splitlines()
    return lines[1].strip() if len(lines) > 1 else None


# ==============================
# Education
# ==============================

def extract_education(text):
    sec = get_section(text, "EDUCATION")
    return [l.strip() for l in sec.splitlines() if l.strip()]


# ==============================
# Roles / Experience titles
# ==============================

def extract_roles(text):
    sec = get_section(text, "EXPERIENCE")
    roles = []

    for line in sec.splitlines():
        line = line.strip()

        # Only capture Title - Company lines
        if "-" in line and not line.startswith("-") and not re.search(r'\d{4}', line):
            roles.append(line)

    return roles

# ==============================
# Certifications
# ==============================

def extract_certifications(text):
    sec = get_section(text, "CERTIFICATIONS")

    return [
        line.strip()
        for line in sec.splitlines()
        if line.strip()
    ]


# ==============================
# Skills
# ==============================

def extract_skills(text):
    tech_sec = get_section(text, "SKILLS")
    soft_sec = get_section(text, "SOFT SKILLS")

    tech = []
    soft = []

    if tech_sec:
        tech = [s.strip().lower() for s in re.split(r'[,\n]', tech_sec) if s.strip()]

    if soft_sec:
        soft = [s.strip().lower() for s in re.split(r'[,\n]', soft_sec) if s.strip()]

    return {
        "technical": sorted(set(tech)),
        "soft": sorted(set(soft))
    }


# ==============================
# Experience calculation (FIXED)
# ==============================

month_map = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12
}

def parse_date(month_str, year_str, end=False):
    month = month_map[month_str.lower()]
    year = int(year_str)

    if end:
        last_day = calendar.monthrange(year, month)[1]
        return datetime(year, month, last_day)
    else:
        return datetime(year, month, 1)


def extract_experience_years(text):
    pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\s+(\d{4})\s*[-–]\s*(Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\s+\d{4})"

    matches = re.findall(pattern, text, re.I)

    total_days = 0
    now = datetime.now()

    for start_m, start_y, end_str in matches:

        start = parse_date(start_m, start_y, end=False)

        # SAFE handling
        if end_str.lower() == "present":
            end_date = now
        else:
            parts = end_str.split()
            if len(parts) == 2:
                end_m, end_y = parts
                end_date = parse_date(end_m, end_y, end=True)
            else:
                continue

        total_days += (end_date - start).days

    return round(total_days / 365.25, 2)
# ==============================
# Quality assessment
# ==============================

def quality_check(data):
    missing = []

    for key in ["name", "email", "skills"]:
        if not data.get(key):
            missing.append(key)

    score = 1.0 - (len(missing) * 0.1)
    score = max(0, round(score, 2))

    return {
        "completeness_score": score,
        "ambiguity_flags": [],
        "missing_sections": missing,
        "data_quality_issues": []
    }


# ==============================
# MAIN
# ==============================

def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py resume.txt")
        return

    path = sys.argv[1]

    with open(path, encoding="utf-8") as f:
        text = clean_text(f.read())

    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
        "education": extract_education(text),
        "roles": extract_roles(text),
        "certifications": extract_certifications(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience_years(text)
    }

    data["quality_assessment"] = quality_check(data)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ results.json created")


if __name__ == "__main__":
    main()