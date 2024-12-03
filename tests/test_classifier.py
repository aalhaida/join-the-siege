# tests/test_classifier.py

import unittest
from unittest.mock import MagicMock, patch
from werkzeug.datastructures import FileStorage
from io import BytesIO
from src import classifier
from src.classifier import classify_text, classify_file
from src.extractors import (
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_docx,
)

class TestClassifier(unittest.TestCase):

    def test_classify_text_drivers_license(self):
        text = "This is a sample driver's license text with DL number and driver ID."
        result = classify_text(text)
        self.assertEqual(result, 'drivers_license')

    def test_classify_text_passport(self):
        text = "Passport Number: X12345678 Nationality: United States of America"
        result = classify_text(text)
        self.assertEqual(result, 'passport')

    def test_classify_text_bank_statement(self):
        text = "Your bank statement is now available. Account Summary: Transactions and Available Balance."
        result = classify_text(text)
        self.assertEqual(result, 'bank_statement')

    def test_classify_text_invoice(self):
        text = "Invoice Number: 12345. Amount Due: $500. Please pay by the due date."
        result = classify_text(text)
        self.assertEqual(result, 'invoice')

    def test_classify_text_tax_report(self):
        text = "This is your Tax Report for the year 2021. Form 1040 from the Internal Revenue Service."
        result = classify_text(text)
        self.assertEqual(result, 'tax_report')

    def test_classify_text_resume(self):
        text = "Curriculum Vitae. Education and Experience. Skills include programming and data analysis."
        result = classify_text(text)
        self.assertEqual(result, 'resume')

    def test_classify_text_contract(self):
        text = "This contract is an agreement between the parties. Terms and conditions apply."
        result = classify_text(text)
        self.assertEqual(result, 'contract')

    def test_classify_text_medical_report(self):
        text = "Patient Diagnosis: The medical report indicates treatment is necessary."
        result = classify_text(text)
        self.assertEqual(result, 'medical_report')

    def test_classify_text_unknown(self):
        text = "This is some random text that doesn't match any document type."
        result = classify_text(text)
        self.assertEqual(result, 'unknown')

    def test_classify_text_ambiguous(self):
        text = "This document contains a driver's license and bank statement information."
        result = classify_text(text)
        self.assertEqual(result, 'ambiguous')

    @patch('src.classifier.extract_text_from_pdf')
    def test_classify_file_pdf(self, mock_extract_text):
        # Mock the text extraction
        mock_extract_text.return_value = "Driver's License Number: 123456"

        # Create a mock PDF file
        file_content = b'%PDF-1.4...'
        file = FileStorage(
            stream=BytesIO(file_content),
            filename='sample.pdf',
            content_type='application/pdf'
        )

        result = classify_file(file)
        self.assertEqual(result, 'drivers_license')

    @patch('src.classifier.extract_text_from_image')
    def test_classify_file_image(self, mock_extract_text):
        # Mock the text extraction
        mock_extract_text.return_value = "Bank Statement for account number 123456789"

        # Create a mock image file
        file_content = b'\x89PNG\r\n\x1a\n...'
        file = FileStorage(
            stream=BytesIO(file_content),
            filename='statement.png',
            content_type='image/png'
        )

        result = classify_file(file)
        self.assertEqual(result, 'bank_statement')

    @patch('src.classifier.extract_text_from_docx')
    def test_classify_file_docx(self, mock_extract_text):
        # Mock the text extraction
        mock_extract_text.return_value = "This is your Invoice. Amount Due: $1000"

        # Create a mock DOCX file
        file_content = b'PK\x03\x04...'
        file = FileStorage(
            stream=BytesIO(file_content),
            filename='invoice.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

        result = classify_file(file)
        self.assertEqual(result, 'invoice')

    def test_classify_file_unsupported_type(self):
        # Create a mock unsupported file
        file_content = b'...'
        file = FileStorage(
            stream=BytesIO(file_content),
            filename='unknown.txt',
            content_type='text/plain'
        )

        result = classify_file(file)
        self.assertEqual(result, 'unsupported file type')

    @patch('src.classifier.extract_text_from_pdf')
    def test_classify_file_error_processing(self, mock_extract_text):
        # Simulate an exception during text extraction
        mock_extract_text.side_effect = Exception("Extraction error")

        # Create a mock PDF file
        file_content = b'%PDF-1.4...'
        file = FileStorage(
            stream=BytesIO(file_content),
            filename='error.pdf',
            content_type='application/pdf'
        )

        result = classify_file(file)
        self.assertEqual(result, 'error processing file')

if __name__ == '__main__':
    unittest.main()
