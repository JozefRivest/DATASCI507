import csv
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_csv("data/clean_data/candidates_proposal.csv")

# New dataset exploration
data.columns

data["candidate"].unique()
data["district"].unique()

data["n_paragraphs"].describe()
data["n_chars"].describe()

# Making graphs for descriptive statistics

data.columns

data["party_en"] = data["party"].case_when(
    caselist=[
        (test["party"].eq("国民民主党"), "kokumin"),
        (test["party"].eq("チームみらい"), "Team Mirai"),
        (test["party"].eq("日本共産党"), "Communist"),
        (test["party"].eq("参政党"), "sanseito"),
        (test["party"].eq("自民党"), "LDP"),
        (test["party"].eq("自由民主党"), "LDP"),
        (test["party"].eq("中道改革連合"), "Chudo"),
        (test["party"].eq("中道"), "Chudo"),
        (test["party"].eq("日本維新の会"), "Ishin"),
        (test["party"].eq("社民党"), "Shaminto"),
        (test["party"].eq("消費税再生党"), "Independent"),
        (test["party"].eq("減税日本"), "Genzei"),
        (test["party"].eq("れいわ新選組"), "Reiwa"),
        (test["party"].eq("日本自由党"), "Liberal party"),
        (test["party"].eq("日本保守党"), "Hoshuto"),
        (test["party"].eq("無所属連合"), "Independent"),
        (test["party"].eq("無所属"), "Independent"),
    ]
)

avg_char = sns.pointplot(
    data=data,
    estimator="mean",
    y="party_en",
    x="n_chars",
    errorbar="ci",
    join=False,
)
sns.set_theme(context="paper", style="white")
avg_char.set_ylabel("Parties", fontsize=14)
avg_char.set_xlabel("Average number of character per bulletin", fontsize=14)
avg_char.tick_params(axis="both", labelsize=12)
plt.savefig("paper/figures/avg_char.pdf", bbox_inches="tight")
plt.show()
plt.close("all")

avg_par = sns.pointplot(
    data=data,
    estimator="mean",
    y="party_en",
    x="n_paragraphs",
    errorbar="ci",
    join=False,
)
avg_par.set_ylabel("Parties", fontsize=14)
avg_par.set_xlabel("Average number of paragraphs per bulletins", fontsize=14)
sns.set_theme(context="paper", style="white")
avg_par.tick_params(axis="both", labelsize=12)
plt.savefig("paper/figures/avg_par.pdf", bbox_inches="tight")
plt.show()
plt.close("all")
