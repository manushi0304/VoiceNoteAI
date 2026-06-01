import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = r"C:\Users\Manus\Desktop\voicenote-ai\ml-training\models\text_classifier"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

model.eval()

def predict(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        pred_id = probs.argmax().item()
        confidence = probs.max().item()

    label = model.config.id2label[pred_id]
    return label, confidence


tests = [
    "Buy groceries tomorrow",
    "Remind me to take medicine at 8 PM",
    "This idea could be useful for future development",
]

for t in tests:
    label, conf = predict(t)
    print(f"{t} → {label} ({conf:.2f})")
