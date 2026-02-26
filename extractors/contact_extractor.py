import re


def find_email(text):
    m = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return m.group(0) if m else ""


def find_phone(text):
    m = re.search(r'(\+?\d[\d\-\s]{8,}\d)', text)
    return m.group(0).strip() if m else ""


def find_name(text):
    first_line = text.strip().split("\n")[0]
    return first_line.strip()