# src/app.py

from flask import Flask, request, jsonify
from src.classifier import classify_file
from werkzeug.utils import secure_filename
import os
import logging  

from .classifier import classify_file
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'docx'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    # Depending on if the intention is to or not to allow multiple files, the below could be implemented
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file part in the request"}), 400
    # files = request.files.getlist('file')
    # if len(files) > 1:
    #     return jsonify({"error": "Multiple file upload not supported"}), 400
    # file = files[0]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            file_class = classify_file(file)
            return jsonify({"file_class": file_class}), 200
        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {e}")
            return jsonify({"file_class": "error processing file"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
