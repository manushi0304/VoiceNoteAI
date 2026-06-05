import os
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
    _model_loaded = None

    LABELS = ["note", "todo", "reminder"]

    MODEL_PATH = Path("models/text_classifier")

    @classmethod
    def _check_and_load_model(cls):
        """
        Check if model weights exist and lazy-load tokenizer and model.
        """
        if cls._model_loaded is None:
            weights_file = cls.MODEL_PATH / "model.safetensors"
            if cls.MODEL_PATH.exists() and weights_file.exists():
                try:
                    from transformers import AutoTokenizer, AutoModelForSequenceClassification
                    cls._tokenizer = AutoTokenizer.from_pretrained(cls.MODEL_PATH)
                    cls._model = AutoModelForSequenceClassification.from_pretrained(
                        cls.MODEL_PATH
                    )
                    cls._model.eval()
                    cls._model_loaded = True
                except Exception as e:
                    print(f"⚠️ Failed to load ML model: {e}")
                    cls._model_loaded = False
            else:
                cls._model_loaded = False

    @classmethod
    def classify(cls, text: str) -> Dict:
        """
        Classify text into note / todo / reminder.
        Returns label + confidence scores.
        """
        cls._check_and_load_model()

        if not cls._model_loaded:
            # Keyword fallback
            lower = text.lower()
            if "remind" in lower or "tomorrow" in lower or "at" in lower or "schedule" in lower:
                label = "reminder"
            elif "buy" in lower or "todo" in lower or "task" in lower or "finish" in lower or "complete" in lower:
                label = "todo"
            else:
                label = "note"
            return {
                "label": label,
                "confidence": 1.0,
                "scores": {
                    "note": 1.0 if label == "note" else 0.0,
                    "todo": 1.0 if label == "todo" else 0.0,
                    "reminder": 1.0 if label == "reminder" else 0.0,
                }
            }

        # Real model execution
        import torch
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
