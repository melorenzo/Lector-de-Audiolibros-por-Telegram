import logging

logger = logging.getLogger(__name__)


def build_chunks_from_text(text, chars_per_chunk=20000):

    chunks = []

    for i in range(0, len(text), chars_per_chunk):

        chunk = text[i:i + chars_per_chunk]

        chunks.append({
            "index": len(chunks) + 1,
            "content": chunk
        })

    logger.info(
        f"🎧 Chunks generados | cantidad={len(chunks)}"
    )

    return chunks