# src/extractors.py

from pdfminer.high_level import extract_text
from PIL import Image
import pytesseract
import docx
from werkzeug.datastructures import FileStorage
from pdfminer.high_level import extract_text
from io import BytesIO

def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.

    Args:
        file (FileStorage): The PDF file uploaded by the user.

    Returns:
        str: The extracted text from the PDF.
    """
    file.seek(0)
    file_bytes = file.read()
    file_stream = BytesIO(file_bytes)
    text = extract_text(file_stream)
    return text

def extract_text_from_image(file: FileStorage) -> str:
    """Extract text from an image file."""
    file.seek(0)
    image = Image.open(file.stream)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_docx(file: FileStorage) -> str:
    """Extract text from a Word document."""
    file.seek(0)
    doc = docx.Document(file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text
