# src/classifier.py

"""
Classifier Module
=================

This module provides functions to classify documents based on their textual content.
It extracts text from various file types and uses pattern matching to determine the type of document.
The classifier does not rely on filenames, making it effective even for poorly named files.
"""

import re
import logging
from werkzeug.datastructures import FileStorage
from .extractors import (
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_docx,
    # extract_text_from_excel,  # Uncomment if handling Excel files
)

def classify_text(text: str) -> str:
    """
    Classify the text content of a document by matching it against predefined regular expression patterns
    for various document types. It calculates scores based on the number of pattern matches for each type
    and selects the one with the highest score.

    Parameters:
        text (str): The extracted text from the document.

    Returns:
        str: The classification of the document. Possible values include:
            - 'drivers_license'
            - 'passport'
            - 'bank_statement'
            - 'invoice'
            - 'tax_report'
            - 'resume'
            - 'contract'
            - 'medical_report'
            - 'unknown' (if no patterns match)
            - 'ambiguous' (if there's a tie between multiple types)
    """
    # Normalize text to lowercase
    text = text.lower()

    # Define regular expression patterns for each document type
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

    # Initialize scores for each document type
    scores = {key: 0 for key in patterns.keys()}

    # Compute scores based on pattern matches
    for doc_type, doc_patterns in patterns.items():
        for pattern in doc_patterns:
            matches = re.findall(pattern, text)
            scores[doc_type] += len(matches)

    # Determine the document type with the highest score
    max_score = max(scores.values())
    if max_score == 0:
        return 'unknown'

    # Check for ties among document types with the highest score
    top_classes = [doc_type for doc_type, score in scores.items() if score == max_score]
    if len(top_classes) == 1:
        return top_classes[0]
    else:
        return 'ambiguous'

def classify_text2(text: str) -> str:
    """
    An alternative, simplified function for classifying text content based on direct keyword searches.

    Parameters:
        text (str): The extracted text from the document.

    Returns:
        str: The classification of the document.
    """
    # Normalize text to lowercase
    text = text.lower()

    # Direct keyword matching
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

    Parameters:
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
