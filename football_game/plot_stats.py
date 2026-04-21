import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("game_data.csv")

match_summary = df.groupby("match_id").agg({
    "score_p1": "max",
    "score_p2": "max",
    "ball_speed": "mean",
    "kicks_p1": "max",
    "kicks_p2": "max",
    "winner": "last",
}).reset_index()

plt.style.use("seaborn-v0_8-whitegrid")

# Figure 1: Gameplay overview
fig1, axes1 = plt.subplots(2, 3, figsize=(14, 7))
fig1.suptitle("SKE vs CPE - Gameplay Statistics", fontsize=16, fontweight="bold")

axes1[0, 0].plot(df["time"], df["ball_speed"], color="green", linewidth=2)
axes1[0, 0].set_title("Ball Speed Over Time")
axes1[0, 0].set_xlabel("Time")
axes1[0, 0].set_ylabel("Ball Speed")

axes1[0, 1].plot(df["time"], df["score_diff"], color="orange", linewidth=2)
axes1[0, 1].set_title("Score Difference Over Time")
axes1[0, 1].set_xlabel("Time")
axes1[0, 1].set_ylabel("Score Diff")

df["possession"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=axes1[0, 2],
    colors=["dodgerblue", "gold"],
)
axes1[0, 2].set_title("Possession")
axes1[0, 2].set_ylabel("")

df["ball_zone"].value_counts().reindex(["LEFT", "CENTER", "RIGHT"]).plot(
    kind="bar",
    color="dodgerblue",
    ax=axes1[1, 0],
    edgecolor="black",
)
axes1[1, 0].set_title("Ball Zone")
axes1[1, 0].set_xlabel("Zone")
axes1[1, 0].set_ylabel("Count")
axes1[1, 0].tick_params(axis="x", rotation=0)

df["attacking_side"].value_counts().reindex(["CPE_ATTACK", "NEUTRAL", "SKE_ATTACK"]).plot(
    kind="bar",
    color="gold",
    ax=axes1[1, 1],
    edgecolor="black",
)
axes1[1, 1].set_title("Attacking Side")
axes1[1, 1].set_xlabel("Side")
axes1[1, 1].set_ylabel("Count")
axes1[1, 1].set_xticklabels(["CPE", "Neutral", "SKE"], rotation=0)

shot_labels = ["SKE Shots", "CPE Shots", "SKE Touches", "CPE Touches"]
shot_values = [
    int(df["shots_p1"].fillna(0).max()),
    int(df["shots_p2"].fillna(0).max()),
    int(df["touches_p1"].fillna(0).max()),
    int(df["touches_p2"].fillna(0).max()),
]

axes1[1, 2].bar(
    shot_labels,
    shot_values,
    color=["gold", "dodgerblue", "lightgreen", "white"],
    edgecolor="black",
)
axes1[1, 2].set_title("Shots and Touches")
axes1[1, 2].set_ylabel("Count")
axes1[1, 2].set_xticklabels(["SKE\nShots", "CPE\nShots", "SKE\nTouches", "CPE\nTouches"])

fig1.tight_layout(rect=[0, 0, 1, 0.94])
fig1.savefig("game_statistics_overview.png", dpi=300)


# Figure 2: Match summary
fig2, axes2 = plt.subplots(1, 3, figsize=(14, 4))
fig2.suptitle("SKE vs CPE - Match Summary", fontsize=16, fontweight="bold")

axes2[0].plot(
    match_summary["match_id"],
    match_summary["score_p1"],
    marker="o",
    label="SKE",
    color="gold",
)
axes2[0].plot(
    match_summary["match_id"],
    match_summary["score_p2"],
    marker="o",
    label="CPE",
    color="dodgerblue",
)
axes2[0].set_title("Final Score by Match")
axes2[0].set_xlabel("Match ID")
axes2[0].set_ylabel("Goals")
axes2[0].legend()

axes2[1].bar(
    match_summary["match_id"].astype(str),
    match_summary["ball_speed"],
    color="green",
    edgecolor="black",
)
axes2[1].set_title("Average Ball Speed by Match")
axes2[1].set_xlabel("Match ID")
axes2[1].set_ylabel("Average Speed")

match_summary["winner"].value_counts().reindex(["SKE", "CPE", "DRAW"]).fillna(0).plot(
    kind="bar",
    color=["gold", "dodgerblue", "lightgray"],
    ax=axes2[2],
    edgecolor="black",
)
axes2[2].set_title("Winner Count")
axes2[2].set_xlabel("Winner")
axes2[2].set_ylabel("Matches")
axes2[2].tick_params(axis="x", rotation=0)

fig2.tight_layout(rect=[0, 0, 1, 0.88])
fig2.savefig("game_statistics_by_match.png", dpi=300)

plt.show()

print("=== STATISTICS ===")
print("Matches Played:", df["match_id"].nunique())
print("Latest Match:", df["match_id"].max())
print("Mean Ball Speed:", round(df["ball_speed"].mean(), 2))
print("Max Ball Speed:", round(df["ball_speed"].max(), 2))
print("SKE Shots:", df["shots_p1"].max())
print("CPE Shots:", df["shots_p2"].max())
print("SKE Touches:", df["touches_p1"].max())
print("CPE Touches:", df["touches_p2"].max())
print("Most Possession:", df["possession"].mode()[0])

print("\nFinal Score by Match:")
print(match_summary[["match_id", "score_p1", "score_p2", "winner"]])
