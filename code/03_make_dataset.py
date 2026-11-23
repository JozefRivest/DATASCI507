import json
from pathlib import Path

import pandas as pd


def dataset_maker(path, output):

    RESULTS = Path(path)  # set the path to iterate over files

    files = sorted(RESULTS.rglob("*.json"))  # Get the candidates json files
    len(files)  # To be removed, check that the previous lines got the correct files

    frames = []
    for path in files:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        df = pd.json_normalize(data["paragraphs"])
        df["file"] = path.stem
        frames.append(df)

    paras = pd.concat(frames, ignore_index=True)
    paras.head()

    # Transform the metadata from the file name into variables
    paras[["ballot_no", "district", "candidate", "party"]] = paras["file"].str.split(
        "_", expand=True
    )
    paras.groupby("district")["candidate"].nunique()  # candidates per district

    # Clean the text
    paras["contents"].isna().sum()  # how many empty paragraphs?
    paras = paras.dropna(subset=["contents"])
    # TODO: NFKC-normalize, and decide whether to remove "\n" inside paragraphs
    # paras["contents"] = paras["contents"].str.normalize("NFKC")

    # Collapse to one row per candidate
    ids = ["file", "ballot_no", "district", "candidate", "party"]

    cands = (
        paras.sort_values(ids + ["order"])
        .groupby(ids, as_index=False)
        .agg(text=("contents", "\n".join), n_paragraphs=("contents", "size"))
    )
    cands["n_chars"] = cands["text"].str.len()
    len(cands)  # expect 68
    print(cands.loc[0, "text"])  # read this next to the crop

    output_path = f"data/clean_data/{output}.csv"
    cands.to_csv(output_path, index=False, encoding="utf-8-sig")
    return cands


dataset_maker(path="data/results", output="candidates_proposal")
