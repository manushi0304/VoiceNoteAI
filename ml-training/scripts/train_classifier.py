
import pandas as pd
import yaml
import torch

from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)

with open("configs/classification.yaml") as f:
    cfg = yaml.safe_load(f)

label2id = {"note": 0, "todo": 1, "reminder": 2}
id2label = {v: k for k, v in label2id.items()}

def load_data(path):
    df = pd.read_csv(path)
    df["label"] = df["label"].map(label2id)
    return Dataset.from_pandas(df)

train_ds = load_data("data/processed/train.csv")
val_ds = load_data("data/processed/val.csv")


tokenizer = DistilBertTokenizerFast.from_pretrained(cfg["model_name"])

def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=cfg["max_length"],
    )

train_ds = train_ds.map(tokenize, batched=True)
val_ds = val_ds.map(tokenize, batched=True)

train_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])
val_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])

model = DistilBertForSequenceClassification.from_pretrained(
    cfg["model_name"],
    num_labels=cfg["num_labels"],
    id2label=id2label,
    label2id=label2id,
)

args = TrainingArguments(
    output_dir=cfg["output_dir"],
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=float(cfg["learning_rate"]),
    per_device_train_batch_size=cfg["batch_size"],
    per_device_eval_batch_size=cfg["batch_size"],
    num_train_epochs=cfg["epochs"],
    weight_decay=0.01,
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
)

trainer.train()
trainer.save_model(cfg["output_dir"])
tokenizer.save_pretrained(cfg["output_dir"])

print("✅ Model training complete")
