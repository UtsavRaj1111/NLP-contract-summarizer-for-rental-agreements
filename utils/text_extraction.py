import pdfplumber
import docx
import pytesseract
from PIL import Image

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------
def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            # Normal text PDF
            if page_text:
                text += page_text + "\n"

            # Image-based PDF → use OCR
            else:
                try:
                    page_image = page.to_image(resolution=300).original
                    ocr_text = pytesseract.image_to_string(page_image)

                    text += ocr_text + "\n"

                except Exception:
                    pass

    return text


# --------------------------------------------------
# DOCX TEXT EXTRACTION
# --------------------------------------------------
def extract_text_from_docx(file):

    doc = docx.Document(file)

    text = "\n".join([p.text for p in doc.paragraphs])

    return text


# --------------------------------------------------
# IMAGE TEXT EXTRACTION (OCR)
# --------------------------------------------------
def extract_text_from_image(file):

    image = Image.open(file)

    text = pytesseract.image_to_string(image)

    return text


# --------------------------------------------------
# MAIN ROUTER
# --------------------------------------------------
def extract_text(file, filename):

    filename = filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)

    elif filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
        return extract_text_from_image(file)

    else:
        return ""