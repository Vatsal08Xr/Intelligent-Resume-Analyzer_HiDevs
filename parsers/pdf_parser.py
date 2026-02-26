from pdfminer.high_level import extract_text


def parse_pdf(path):
    return extract_text(path)