import json

import pandas as pd

# Import the json file
with open("data/results/output_0.json", encoding="utf-8") as f:
    data = json.load(f)

# Normalize to the pandas format
paras = pd.json_normalize(data["paragraphs"])
paras = paras.sort_values("order")
print(paras[["order", "direction", "role", "contents"]])

# Count the number of paragraphs
print(paras["role"].value_counts(dropna=False))

# Extract the full text
full_text = "\n".join(paras["contents"])
print(full_text)
