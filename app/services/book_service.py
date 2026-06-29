import os
import logging

from parsers.pdf_parser import extract_text as extract_pdf_text
from parsers.epub_parser import extract_text as extract_epub_text
from parsers.chunk_builder import (
    build_chunks_from_text,
    build_chunks_from_chapters
)
from parsers.chapter_parser import detect_chapters

from services.job_manager import create_job

logger = logging.getLogger(__name__)

CHARS_PER_CHUNK = 20000


def _chunk_from_epub_chapters(epub_chapters):

    chunks = []

    for chap in epub_chapters:

        text = chap["content"]

        for i in range(0, len(text), CHARS_PER_CHUNK):

            sub = text[i:i + CHARS_PER_CHUNK]

            chapter_label = chap["name"].replace(
                "Text/", ""
            ).replace(".xhtml", "")

            if len(text) > CHARS_PER_CHUNK:

                part = i // CHARS_PER_CHUNK + 1
                chapter_label = f"{chapter_label} (parte {part})"

            chunks.append({
                "index": len(chunks) + 1,
                "content": sub,
                "chapter": chapter_label
            })

    return chunks


async def save_book(document, chat_id):

    filename = document.file_name

    if not filename.lower().endswith((".pdf", ".epub")):

        return False, "❌ Solo acepto PDF o EPUB."

    os.makedirs(
        "app/storage/books",
        exist_ok=True
    )

    telegram_file = await document.get_file()

    destination = f"app/storage/books/{filename}"

    await telegram_file.download_to_drive(
        destination
    )

    logger.info(
        f"📚 Libro guardado | nombre={filename}"
    )

    pages = 0

    chapter_info = ""

    if filename.lower().endswith(".pdf"):

        pdf_data = extract_pdf_text(destination)

        text = pdf_data["text"]
        pages = pdf_data["pages"]

        boundaries = detect_chapters(text)

        if boundaries:

            chapter_info = f"📖 Capítulos: {len(boundaries)}"

            chunks = build_chunks_from_chapters(
                text, boundaries
            )

        else:

            chapter_info = "📖 Capítulos: sin detectar"

            chunks = build_chunks_from_text(text)

        text_length = len(text)

    else:

        epub_data = extract_epub_text(destination)

        epub_chapters = epub_data["chapters"]
        pages = epub_data["pages"]

        chapter_info = f"📖 Capítulos: {len(epub_chapters)}"

        chunks = _chunk_from_epub_chapters(epub_chapters)

        text_length = sum(
            len(c["content"]) for c in epub_chapters
        )

    logger.info(
        f"🎧 Chunks generados | cantidad={len(chunks)}"
    )

    book_name = os.path.splitext(filename)[0]

    job = create_job(
        filename,
        chunks,
        chat_id,
        book_name
    )

    return True, {
        "filename": filename,
        "pages": pages,
        "text_length": text_length,
        "chunks": len(chunks),
        "chapters": chapter_info,
        "job": job
    }