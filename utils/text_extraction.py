import pdfplumber
import docx
import pytesseract
from PIL import Image


def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


def extract_text_from_docx(file):

    doc = docx.Document(file)

    text = "\n".join([p.text for p in doc.paragraphs])

    return text


def extract_text_from_image(file):

    image = Image.open(file)

    text = pytesseract.image_to_string(image)

    return text


def extract_text(file, filename):

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)

    elif filename.endswith(".jpg") or filename.endswith(".png"):
        return extract_text_from_image(file)

    else:
        return ""