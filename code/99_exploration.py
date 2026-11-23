import csv

import pandas as pd

data = pd.read_csv("data/clean_data/candidates_proposal.csv")

data.columns

data["candidate"].unique()
data["district"].unique()

data["n_paragraphs"].describe()
data["n_chars"].describe()
