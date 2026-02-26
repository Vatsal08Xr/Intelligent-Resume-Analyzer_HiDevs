import docx


def parse_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)