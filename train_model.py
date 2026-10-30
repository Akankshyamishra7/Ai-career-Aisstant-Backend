"""
Standalone training script to generate datasets and train the ML job role prediction model.
Usage:
    python train_model.py
"""
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.ml.train import train_and_save_model

if __name__ == "__main__":
    print("=" * 60)
    print("AI Career Assistant - ML Model Training Pipeline")
    print("=" * 60)
    pipeline = train_and_save_model()
    print("Training finished successfully. The model is saved and ready for deployment.")
