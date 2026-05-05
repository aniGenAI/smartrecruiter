from pypdf import PdfReader


def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []

    for page in reader.pages:
        text.append(page.extract_text() or "")

    return "\n".join(text)