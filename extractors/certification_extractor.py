def extract_certifications(text):
    lines = text.split("\n")

    capture = False
    certs = []

    for line in lines:
        clean = line.strip()

        if clean.lower() == "certifications":
            capture = True
            continue

        if capture:
            if not clean or clean.isupper():  # stop at next section
                break
            certs.append(clean)

    return certs