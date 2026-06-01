import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

class TextClassifierService:
    _model = None
    _tokenizer = None
    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def __init__(self):
        if TextClassifierService._model is None:
            self._load_model()

    def _load_model(self):
        MODEL_PATH = Path(__file__).resolve().parents[4] / "ml-training/models/text_classifier"

        TextClassifierService._tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        TextClassifierService._model = AutoModelForSequenceClassification.from_pretrained(
            MODEL_PATH
        ).to(self._device)

        TextClassifierService._model.eval()

    def predict(self, text: str):
        inputs = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        ).to(self._device)

        with torch.no_grad():
            outputs = TextClassifierService._model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)

        confidence, pred_id = torch.max(probs, dim=1)
        label = TextClassifierService._model.config.id2label[pred_id.item()]

        return label, confidence.item()
