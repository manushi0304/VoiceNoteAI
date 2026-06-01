import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

model_path = "../models/text_classifier"

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    return model.config.id2label[probs.argmax().item()], probs.max().item()

tests = [
    "Buy groceries tomorrow",
    "Remind me to call mom at night",
    "The meeting notes are important",
]

for t in tests:
    print(t, "→", predict(t))
