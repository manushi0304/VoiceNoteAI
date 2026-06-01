import pandas as pd

df = pd.read_csv("data/train.csv")

before = len(df)
df = df.drop_duplicates(subset=["text", "label"])
after = len(df)

print(f"Removed {before - after} duplicates")

df.to_csv("data/train_dedup.csv", index=False)
