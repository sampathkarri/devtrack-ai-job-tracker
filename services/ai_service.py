from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(
    resume_text: str,
    job_description: str
):
    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    score = round(similarity * 100, 2)

    return score
import joblib

# Load trained model and vectorizer
model = joblib.load("saved_models/status_model.pkl")
vectorizer = joblib.load("saved_models/vectorizer.pkl")


def predict_status(note: str):
    vector = vectorizer.transform([note])

    prediction = model.predict(vector)

    return prediction[0]