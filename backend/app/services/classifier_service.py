# backend/app/services/classifier_service.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

class TextClassifierService:
    def __init__(self):
        print("✅ TextClassifierService loaded (model + tokenizer)")

        # Try the local backend/models path first (perfect for Render and local)
        MODEL_PATH = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../../models/text_classifier"
        ))

        # Fallback to the sibling ml-training path if needed
        if not os.path.exists(MODEL_PATH):
            MODEL_PATH = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                "../../../ml-training/models/text_classifier"
            ))


        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        self.model.eval()

    def predict(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)

        confidence, pred_id = torch.max(probs, dim=1)
        label = self.model.config.id2label[pred_id.item()]

        return label, confidence.item()
