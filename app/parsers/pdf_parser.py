import fitz


def extract_text(pdf_path):

    text = ""

    pdf = fitz.open(pdf_path)

    page_count = len(pdf)

    print(f"📄 Páginas detectadas: {page_count}")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    print(f"📝 Caracteres extraídos: {len(text)}")

    return {
        "text": text,
        "pages": page_count
    }