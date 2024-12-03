# src/classifierMLExample.py

import pickle
from .extractors import extract_text_from_pdf, extract_text_from_image, extract_text_from_docx
from .preprocessing import preprocess_text

# Load the model and vectorizer
with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('models/model.pkl', 'rb') as f:
    model = pickle.load(f)

def classify_file(file: FileStorage) -> str:
    filename = file.filename.lower()
    file_extension = filename.rsplit('.', 1)[1]

    try:
        # Extract text
        if file_extension == 'pdf':
            text = extract_text_from_pdf(file)
        elif file_extension in ['png', 'jpg', 'jpeg']:
            text = extract_text_from_image(file)
        elif file_extension == 'docx':
            text = extract_text_from_docx(file)
        else:
            return 'unsupported file type'

        # Preprocess text
        preprocessed_text = preprocess_text(text)

        # Vectorize text
        features = vectorizer.transform([preprocessed_text])

        # Predict document type
        prediction = model.predict(features)
        predicted_class = prediction[0]
        return predicted_class

    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}")
        return 'error processing file'
