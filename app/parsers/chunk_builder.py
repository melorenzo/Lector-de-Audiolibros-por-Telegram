import logging

logger = logging.getLogger(__name__)

CHARS_PER_CHUNK = 20000


def build_chunks_from_text(text, chars_per_chunk=CHARS_PER_CHUNK):

    chunks = []

    for i in range(0, len(text), chars_per_chunk):

        chunk = text[i:i + chars_per_chunk]

        chunks.append({
            "index": len(chunks) + 1,
            "content": chunk
        })

    logger.info(
        f"🎧 Chunks generados (fijo) | cantidad={len(chunks)}"
    )

    return chunks


def build_chunks_from_chapters(text, boundaries):

    if not boundaries:
        return build_chunks_from_text(text)

    chunks = []

    for i, boundary in enumerate(boundaries):

        start = boundary["char_position"]

        next_start = (
            boundaries[i + 1]["char_position"]
            if i + 1 < len(boundaries)
            else len(text)
        )

        chapter_title = boundary["title"]

        chapter_text = text[start:next_start].strip()

        if len(chapter_text) <= CHARS_PER_CHUNK:

            chunks.append({
                "index": len(chunks) + 1,
                "content": chapter_text,
                "chapter": chapter_title
            })

        else:

            sub_chunks = _split_long_chapter(
                chapter_text,
                chapter_title,
                len(chunks) + 1
            )

            chunks.extend(sub_chunks)

    if not chunks:
        return build_chunks_from_text(text)

    logger.info(
        f"🎧 Chunks generados (capítulos) | "
        f"capítulos={len(boundaries)}, "
        f"chunks={len(chunks)}"
    )

    return chunks


def _split_long_chapter(text, chapter_title, start_index):

    chunks = []

    for i in range(0, len(text), CHARS_PER_CHUNK):

        sub_text = text[i:i + CHARS_PER_CHUNK]

        suffixed = (
            f"{chapter_title} (parte {i // CHARS_PER_CHUNK + 1})"
            if len(text) > CHARS_PER_CHUNK
            else chapter_title
        )

        chunks.append({
            "index": start_index + len(chunks),
            "content": sub_text,
            "chapter": suffixed
        })

    return chunks
