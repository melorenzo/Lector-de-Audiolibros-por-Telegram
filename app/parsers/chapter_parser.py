import re


def extract_chapters(text):

    pattern = r"(?i)cap[ií]tulo\s+\d+"

    matches = list(
        re.finditer(pattern, text)
    )

    return matches