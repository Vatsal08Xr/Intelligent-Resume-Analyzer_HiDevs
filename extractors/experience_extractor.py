import re
from datetime import datetime


def extract_experience_years(text):
    """
    Parse date ranges like:
    2023 – 2024
    2024 – Present
    """

    current_year = datetime.now().year

    total_months = 0

    pattern = r'(\d{4})\s*[–-]\s*(present|\d{4})'

    matches = re.findall(pattern, text.lower())

    for start, end in matches:
        start = int(start)

        if end == "present":
            end = current_year
        else:
            end = int(end)

        months = (end - start) * 12
        total_months += months

    years = total_months / 12

    return round(years, 1)