import pandas as pd

LABEL_MAP = {
    "note": 0,
    "todo": 1,
    "reminder": 2,
}

def convert(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df["label"] = df["label"].map(LABEL_MAP)

    if df["label"].isnull().any():
        raise ValueError("Unknown label found!")

    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    convert("data/train.csv", "data/train_encoded.csv")
    convert("data/val.csv", "data/val_encoded.csv")
