import os
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from app.config import settings
from app.ml.dataset import generate_training_data

MODEL_PATH = settings.MODEL_DIR / "job_role_pipeline.joblib"

def train_and_save_model() -> Pipeline:
    """
    Trains a Scikit-learn TF-IDF + LogisticRegression model on the generated job-roles dataset
    and persists the model pipeline to disk.
    """
    print("[ML] Generating synthetic and authoritative training dataset...")
    df = generate_training_data(samples_per_role=60)
    print(f"[ML] Total training instances: {len(df)} across {df['role'].nunique()} classes.")

    X = df["text"]
    y = df["role"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=4000,
            sublinear_tf=True,
            stop_words="english"
        )),
        ("classifier", LogisticRegression(
            C=2.5,
            max_iter=1000,
            solver="lbfgs"
        ))
    ])

    print("[ML] Training ML pipeline...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[ML] Model Training Completed. Test Accuracy: {acc * 100:.2f}%")
    print(classification_report(y_test, y_pred, zero_division=0))

    settings.MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"[ML] Saved model pipeline to: {MODEL_PATH}")

    return pipeline

def get_or_load_model() -> Pipeline:
    """
    Loads persisted model, or trains it if not present.
    """
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"[ML] Error loading model from {MODEL_PATH}: {e}. Retraining...")
    
    return train_and_save_model()

if __name__ == "__main__":
    train_and_save_model()
