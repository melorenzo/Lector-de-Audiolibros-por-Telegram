import os
import logging

from parsers.pdf_parser import extract_text as extract_pdf_text
from parsers.epub_parser import extract_text as extract_epub_text
from parsers.chunk_builder import build_chunks_from_text

logger = logging.getLogger(__name__)


async def save_book(document):

    filename = document.file_name

    if not filename.lower().endswith((".pdf", ".epub")):
        logger.warning(f"Archivo rechazado | nombre={filename}")
        return False, "❌ Solo acepto PDF o EPUB."

    os.makedirs("app/storage/books", exist_ok=True)

    telegram_file = await document.get_file()

    destination = f"app/storage/books/{filename}"

    await telegram_file.download_to_drive(destination)

    logger.info(
        f"📚 Libro guardado | nombre={filename} | ruta={destination}"
    )

    text = ""
    pages = 0

    # 📄 PDF
    if filename.lower().endswith(".pdf"):

        pdf_data = extract_pdf_text(destination)

        text = pdf_data["text"]
        pages = pdf_data["pages"]

    # 📚 EPUB
    elif filename.lower().endswith(".epub"):

        epub_data = extract_epub_text(destination)

        text = epub_data["text"]
        pages = epub_data["pages"]

    logger.info(
        f"📖 Texto extraído | paginas={pages} | caracteres={len(text)}"
    )

    # 🎧 CHUNKS
    chunks = []

    if text:

        chunks = build_chunks_from_text(text)

    logger.info(
        f"🎧 Chunks generados | cantidad={len(chunks)}"
    )

    return True, {
        "filename": filename,
        "pages": pages,
        "text_length": len(text),
        "chunks": len(chunks)
    }