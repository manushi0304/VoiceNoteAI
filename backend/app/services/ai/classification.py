from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pathlib import Path
from typing import Dict


class ClassificationService:
    """
    ML-powered intent classifier for:
    - note
    - todo
    - reminder
    """

    _model = None
    _tokenizer = None

    LABELS = ["note", "todo", "reminder"]

    MODEL_PATH = Path("models/text_classifier")

    @classmethod
    def _load_model(cls):
        """
        Lazy-load model and tokenizer (loaded once per process).
        """
        if cls._model is None or cls._tokenizer is None:
            cls._tokenizer = AutoTokenizer.from_pretrained(cls.MODEL_PATH)
            cls._model = AutoModelForSequenceClassification.from_pretrained(
                cls.MODEL_PATH
            )
            cls._model.eval()  # IMPORTANT: inference mode

    @classmethod
    def classify(cls, text: str) -> Dict:
        """
        Classify text into note / todo / reminder.
        Returns label + confidence scores.
        """
        cls._load_model()

        inputs = cls._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )

        with torch.no_grad():
            outputs = cls._model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]

        predicted_idx = torch.argmax(probs).item()
        predicted_label = cls.LABELS[predicted_idx]

        return {
            "label": predicted_label,
            "confidence": float(probs[predicted_idx]),
            "scores": {
                cls.LABELS[i]: float(probs[i])
                for i in range(len(cls.LABELS))
            },
        }
