# src/classifier.py

import re
import logging
# A slightly more diverse code that allows for deeper classification
def classify_text(text: str) -> str:
    text = text.lower()

    # Updated patterns without word boundaries
    patterns = {
        'drivers_license': [
            r'driver\'?s?\s+license',
            r'dl\s+number',
            r'driver\s+id',
        ],
        'passport': [
            r'passport',
            r'passport\s+number',
            r'nationality',
            r'issued\s+by.*department\s+of\s+state',
        ],
        'bank_statement': [
            r'bank\s+statement',
            r'account\s+summary',
            r'transaction\s+history',
            r'available\s+balance',
        ],
        'invoice': [
            r'invoice',
            r'invoice\s+number',
            r'bill\s+to',
            r'amount\s+due',
        ],
        'tax_report': [
            r'tax\s+report',
            r'tax\s+return',
            r'form\s+1040',
            r'internal\s+revenue\s+service',
        ],
        'resume': [
            r'resume',
            r'curriculum\s+vitae',
            r'\bcv\b',
            r'education',
            r'skills',
            r'experience',
        ],
        'contract': [
            r'contract',
            r'agreement',
            r'terms\s+and\s+conditions',
            r'party.*hereby',
        ],
        'medical_report': [
            r'medical\s+report',
            r'diagnosis',
            r'patient',
            r'treatment',
        ],
    }

    # Initialize scores
    scores = {key: 0 for key in patterns.keys()}

    # Compute scores
    for doc_type, doc_patterns in patterns.items():
        for pattern in doc_patterns:
            matches = re.findall(pattern, text)
            scores[doc_type] += len(matches)

    # Determine the document type with the highest score
    max_score = max(scores.values())
    if max_score == 0:
        return 'unknown'

    # Check for ties
    top_classes = [doc_type for doc_type, score in scores.items() if score == max_score]
    if len(top_classes) == 1:
        return top_classes[0]
    else:
        return 'ambiguous'


# src/classifier.py

from werkzeug.datastructures import FileStorage
from .extractors import (
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_docx,
    # extract_text_from_excel,  # Uncomment if handling Excel files
)
import logging

def classify_text2(text: str) -> str:
    """
    Classify the text content of a document.

    Args:
        text (str): The extracted text from the document.

    Returns:
        str: The classification of the document.
    """
    text = text.lower()
    if 'driver\'s license' in text or 'driver license' in text:
        return 'drivers_license'
    elif 'bank statement' in text:
        return 'bank_statement'
    elif 'invoice' in text:
        return 'invoice'
    elif 'passport' in text:
        return 'passport'
    elif 'tax report' in text:
        return 'tax_report'
    elif 'resume' in text or 'curriculum vitae' in text:
        return 'resume'
    elif 'contract' in text:
        return 'contract'
    else:
        return 'unknown'

def classify_file(file: FileStorage) -> str:
    """
    Classify a file based on its content by extracting text and analyzing it.

    Args:
        file (FileStorage): The file uploaded by the user.

    Returns:
        str: The classification of the document.
    """
    filename = file.filename.lower()
    file_extension = filename.rsplit('.', 1)[1]

    try:
        # Extract text based on file extension
        if file_extension == 'pdf':
            text = extract_text_from_pdf(file)
        elif file_extension in ['png', 'jpg', 'jpeg']:
            text = extract_text_from_image(file)
        elif file_extension == 'docx':
            text = extract_text_from_docx(file)
        # Uncomment the following if handling Excel files
        # elif file_extension == 'xlsx':
        #     text = extract_text_from_excel(file)
        else:
            return 'unsupported file type'

        # Classify the extracted text
        file_class = classify_text(text)
        return file_class

    except Exception as e:
        # Log the error for debugging purposes
        logging.error(f"Error processing file {filename}: {e}")
        return 'error processing file'



