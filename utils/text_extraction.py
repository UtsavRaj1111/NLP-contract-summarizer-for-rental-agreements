import pdfplumber
import docx
import pytesseract
from PIL import Image
import os
import platform
import logging

# Configure production logging
logger = logging.getLogger(__name__)

# Identify Tesseract path
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "tesseract")

# Auto-detect common Windows installation if not in PATH
if platform.system() == "Windows" and TESSERACT_PATH == "tesseract":
    COMMON_WINDOWS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(COMMON_WINDOWS_PATH):
        TESSERACT_PATH = COMMON_WINDOWS_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------
def extract_text_from_pdf(file_path):
    """
    Extracts text from PDF with intelligent OCR fallback for images.
    CPU-efficient by only triggering OCR on empty pages.
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            logger.info(f"PDF Opened: {file_path}, Pages: {len(pdf.pages)}")
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()

                # Normal text PDF: Fast extraction
                if page_text and len(page_text.strip()) > 10:
                    text += page_text + "\n"
                
                # Image-based PDF page: OCR fallback
                else:
                    try:
                        logger.warning(f"Empty text on page {i+1}, triggering OCR...")
                        # High quality but smaller footprint (300 DPI)
                        page_image = page.to_image(resolution=300).original
                        ocr_text = pytesseract.image_to_string(page_image)
                        
                        if ocr_text:
                            text += ocr_text + "\n"
                    except Exception as e:
                        logger.error(f"OCR failed for page {i+1}: {e}")
    except Exception as e:
        logger.error(f"Fatal PDF Reading Error: {e}")

    return text


# --------------------------------------------------
# DOCX TEXT EXTRACTION
# --------------------------------------------------
def extract_text_from_docx(file):
    """Securely handles DOCX extraction."""
    try:
        doc = docx.Document(file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text
    except Exception as e:
        logger.error(f"DOCX Extraction Error: {e}")
        return ""


# --------------------------------------------------
# IMAGE TEXT EXTRACTION (OCR)
# --------------------------------------------------
def extract_text_from_image(file):
    """Performs OCR on static image files."""
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Image OCR Error: {e}")
        return ""


# --------------------------------------------------
# MAIN ROUTER
# --------------------------------------------------
def extract_text(file, filename):
    """
    Optimized router for all legal document types.
    """
    ext = filename.lower().split('.')[-1]
    
    if ext == "pdf":
        return extract_text_from_pdf(file)
    elif ext == "docx":
        return extract_text_from_docx(file)
    elif ext in ["jpg", "png", "jpeg", "bmp"]:
        return extract_text_from_image(file)
    else:
        logger.warning(f"Unsupported file format: {ext}")
        return ""