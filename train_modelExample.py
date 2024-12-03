# train_modelExample.py
# This is a simplified example of how model training would look

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.preprocessing import preprocess_text

# Load and preprocess your dataset
texts = [...]  # List of extracted texts
labels = [...]  # Corresponding labels
preprocessed_texts = [preprocess_text(text) for text in texts]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(preprocessed_texts, labels, test_size=0.2, random_state=42)

# Feature extraction
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Model training
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Evaluation
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)
