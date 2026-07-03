from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# Training data
texts = [
    "Received online assessment link",
    "HR scheduled technical interview",
    "Congratulations you are selected",
    "We regret to inform you that you are rejected",
    "Interview completed successfully",
    "Offer letter has been sent",
    "Coding test invitation",
    "Application rejected after interview",
    "HR called for interview",
    "Online coding assessment received"
]

labels = [
    "OA",
    "Interview",
    "Offer",
    "Rejected",
    "Interview",
    "Offer",
    "OA",
    "Rejected",
    "Interview",
    "OA"
]

# Convert text into vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train model
model = MultinomialNB()
model.fit(X, labels)

# Create folder if it doesn't exist
os.makedirs("saved_models", exist_ok=True)

# Save model and vectorizer
joblib.dump(model, "saved_models/status_model.pkl")
joblib.dump(vectorizer, "saved_models/vectorizer.pkl")

print("Model trained successfully!")