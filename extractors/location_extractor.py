import re


def extract_location(text):
    m = re.search(r'([A-Z][a-z]+,\s*[A-Z][a-z]+)', text)
    return m.group(1) if m else "Unknown"