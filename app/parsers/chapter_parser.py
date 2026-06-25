import re
import logging

logger = logging.getLogger(__name__)

CHAPTER_PATTERNS = [
    # Spanish: Capítulo 1, Capítulo I, CAPÍTULO PRIMERO
    r"(?i)^(?:cap[íi]tulo|lecci[óo]n|secci[óo]n|tema|unidad)\s+.+",
    # English: Chapter 1, Chapter One
    r"(?i)^(?:chapter|lesson|section|topic|unit)\s+.+",
    # Part / Parte (at start of line)
    r"(?i)^part(?:e|)\s+(?:\d+|[ivxlcdm]+|\w+).*",
    # Front/back matter
    r"(?i)^(?:pr[óo]logo|ep[íi]logo|introducci[óo]n|ap[eé]ndice)$",
    r"(?i)^(?:prologue|epilogue|introduction|appendix)$",
]

MAX_LINE_LENGTH = 120

MIN_CHAPTERS_TO_CONFIRM = 3


def extract_chapters(text):

    lines = text.split("\n")

    boundaries = []

    for i, line in enumerate(lines):

        stripped = line.strip()

        if not stripped:
            continue

        if len(stripped) > MAX_LINE_LENGTH:
            continue

        for pattern in CHAPTER_PATTERNS:

            if re.search(pattern, stripped):

                boundaries.append({
                    "title": stripped,
                    "line_index": i,
                    "char_position": sum(
                        len(l) + 1 for l in lines[:i]
                    )
                })

                break

    return boundaries


def detect_chapters(text):

    boundaries = extract_chapters(text)

    if len(boundaries) >= MIN_CHAPTERS_TO_CONFIRM:

        logger.info(
            f"📖 Capítulos detectados: {len(boundaries)}"
        )

        return boundaries

    logger.info(
        f"📖 Sin capítulos detectados "
        f"({len(boundaries)} encontrados, "
        f"mínimo {MIN_CHAPTERS_TO_CONFIRM})"
    )

    return []
