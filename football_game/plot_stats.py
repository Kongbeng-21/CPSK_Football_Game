import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("game_data.csv")

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle("SKE vs CPE Football Battle - Match Statistics", fontsize=18, fontweight="bold")

axes[0, 0].plot(df["time"], df["ball_speed"], color="green", linewidth=2)
axes[0, 0].set_title("Ball Speed Over Time")
axes[0, 0].set_xlabel("Time")
axes[0, 0].set_ylabel("Ball Speed")
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(df["time"], df["score_diff"], color="orange", linewidth=2)
axes[0, 1].set_title("Score Difference Over Time")
axes[0, 1].set_xlabel("Time")
axes[0, 1].set_ylabel("Score Difference")
axes[0, 1].grid(True, alpha=0.3)

df["possession"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=axes[0, 2])
axes[0, 2].set_title("Possession")
axes[0, 2].set_ylabel("")

df["ball_zone"].value_counts().plot(kind="bar", color="dodgerblue", ax=axes[1, 0])
axes[1, 0].set_title("Ball Zone Distribution")
axes[1, 0].set_xlabel("Zone")
axes[1, 0].set_ylabel("Count")

df["attacking_side"].value_counts().plot(kind="bar", color="gold", ax=axes[1, 1])
axes[1, 1].set_title("Attacking Side")
axes[1, 1].set_xlabel("Side")
axes[1, 1].set_ylabel("Count")

shot_data = {
    "SKE Shots": df["shots_p1"].max(),
    "CPE Shots": df["shots_p2"].max(),
    "SKE Touches": df["touches_p1"].max(),
    "CPE Touches": df["touches_p2"].max(),
}

axes[1, 2].bar(shot_data.keys(), shot_data.values(), color=["gold", "dodgerblue", "lightgreen", "white"])
axes[1, 2].set_title("Shots and Touches")
axes[1, 2].tick_params(axis="x", rotation=20)

plt.tight_layout()
plt.savefig("game_statistics.png", dpi=300)
plt.show()

print("=== STATISTICS ===")
print("Mean Ball Speed:", round(df["ball_speed"].mean(), 2))
print("Max Ball Speed:", round(df["ball_speed"].max(), 2))
print("SKE Shots:", df["shots_p1"].max())
print("CPE Shots:", df["shots_p2"].max())
print("SKE Touches:", df["touches_p1"].max())
print("CPE Touches:", df["touches_p2"].max())
print("Most Possession:", df["possession"].mode()[0])
