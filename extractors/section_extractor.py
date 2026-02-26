import re
import spacy

nlp = spacy.load("en_core_web_sm")


def find_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else ""


def find_phone(text):
    match = re.search(r'\+?\d[\d\s-]{8,}', text)
    return match.group(0) if match else ""


def find_name(text):
    doc = nlp(text)

    # spaCy detects people names automatically
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Unknown"