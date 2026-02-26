DEGREES = ["bachelor", "master", "b.tech", "m.tech", "phd", "bsc", "msc"]


def extract_education(text):
    lines = text.split("\n")
    edu = []

    for line in lines:
        if any(d in line.lower() for d in DEGREES):
            edu.append(line.strip())

    return edu