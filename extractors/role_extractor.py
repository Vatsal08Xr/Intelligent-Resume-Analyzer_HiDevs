import re


def extract_roles(text):
    roles = []

    for line in text.split("\n"):
        if "–" in line or "-" in line:
            if re.search(r"(engineer|developer|manager|intern|analyst)", line.lower()):
                roles.append(line.strip())

    return roles