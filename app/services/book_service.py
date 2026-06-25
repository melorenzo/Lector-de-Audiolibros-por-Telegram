import os
import logging

from parsers.pdf_parser import extract_text as extract_pdf_text
from parsers.epub_parser import extract_text as extract_epub_text
from parsers.chunk_builder import build_chunks_from_text

from services.job_manager import create_job

logger = logging.getLogger(__name__)


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

    text = ""
    pages = 0

    if filename.lower().endswith(".pdf"):

        pdf_data = extract_pdf_text(destination)

        text = pdf_data["text"]
        pages = pdf_data["pages"]

    elif filename.lower().endswith(".epub"):

        epub_data = extract_epub_text(destination)

        text = epub_data["text"]
        pages = epub_data["pages"]

    logger.info(
        f"📖 Texto extraído | paginas={pages}"
    )

    chunks = build_chunks_from_text(text)

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
        "text_length": len(text),
        "chunks": len(chunks),
        "job": job
    }