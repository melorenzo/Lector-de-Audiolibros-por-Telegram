import fitz
import logging

logger = logging.getLogger(__name__)


def extract_text(pdf_path):

    text = ""

    pdf = fitz.open(pdf_path)

    page_count = len(pdf)

    logger.info(
        f"📄 Páginas detectadas: {page_count}"
    )

    for page in pdf:
        text += page.get_text()

    pdf.close()

    logger.info(
        f"📝 Caracteres extraídos: {len(text)}"
    )

    return {
        "text": text,
        "pages": page_count
    }