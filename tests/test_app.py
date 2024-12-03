# tests/test_app.py

from io import BytesIO

import pytest
from src.app import app, allowed_file

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.jpeg", True),
    ("file.docx", True),
    ("file.txt", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No file part in the request"}

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No selected file"}

def test_unsupported_file_type(client):
    data = {'file': (BytesIO(b"dummy content"), 'file.exe')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json() == {"error": "File type not allowed"}

def test_empty_file_upload(client, mocker):
    
    def mock_classify_file(file):
        return 'error processing file' if not file.read() else 'unknown'

    mocker.patch('src.app.classify_file', mock_classify_file)

    data = {'file': (BytesIO(b""), 'empty.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "error processing file"}

def test_corrupted_file_upload(client, mocker):
    def mock_classify_file(file):
        raise Exception("Corrupted file")

    mocker.patch('src.app.classify_file', mock_classify_file)

    data = {'file': (BytesIO(b"corrupted content"), 'corrupted.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "error processing file"}

def test_success(client, mocker):
    mocker.patch('src.app.classify_file', return_value='test_class')

    data = {'file': (BytesIO(b"dummy content"), 'file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "test_class"}

def test_classify_file_invoice(client, mocker):
    mocker.patch('src.classifier.extract_text_from_pdf', return_value='This is an invoice.')
    mocker.patch('src.classifier.classify_text', return_value='invoice')

    data = {'file': (BytesIO(b"%PDF-1.4..."), 'invoice.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "invoice"}

def test_large_file_upload(client, mocker):
    large_content = b"A" * (10 * 1024 * 1024)  # 10 MB of data

    mocker.patch('src.app.classify_file', return_value='large_file_class')

    data = {'file': (BytesIO(large_content), 'large_file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "large_file_class"}

# This depends on the purpose as it is not needed if only intended for single use
# def test_multiple_file_upload(client):
#     data = [
#         ('file', (BytesIO(b"content1"), 'file1.pdf')),
#         ('file', (BytesIO(b"content2"), 'file2.pdf')),
#     ]
#     response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    
#     assert response.status_code == 200
  




    