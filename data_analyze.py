import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import glob

CSV_PATH = "game_data.csv"
OUT_DIR  = "stats"
OUT_FILE = os.path.join(OUT_DIR, "stats_dashboard.png")
os.makedirs(OUT_DIR, exist_ok=True)

for old in glob.glob(os.path.join(OUT_DIR, "*.png")):
    os.remove(old)

SKE_YELLOW = "#F5C518"
CPE_BLUE   = "#4A9EE0"
DRAW_GRAY  = "#AAAAAA"
GREEN_DARK = "#1A5C1A"
GREEN_MID  = "#2E8B2E"
BG         = "#F4F8F4"
TEXT       = "#1A1A1A"

if not os.path.exists(CSV_PATH):
    print(f"[analyze] {CSV_PATH} not found — play at least one match first.")
    exit()

df          = pd.read_csv(CSV_PATH)
numeric_cols = ["ball_speed","score_p1","score_p2","score_diff",
                "kicks_p1","kicks_p2","jumps_p1","jumps_p2",
                "possession","touches_p1","touches_p2","shots_p1","shots_p2"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
last        = df.groupby("match_id").last().reset_index()
wins        = df[df["winner"].notna() & (df["winner"] != "")].copy()
avg_by_time = df.groupby("time").mean(numeric_only=True).reset_index()
total       = len(last)
print(f"[analyze] {total} matches loaded from {CSV_PATH}")


def style(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor("#EEF7EE")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(colors=TEXT, labelsize=7.5)
    ax.set_title(title, fontsize=9.5, fontweight="bold", color=TEXT, pad=5)
    if xlabel: ax.set_xlabel(xlabel, fontsize=7.5, color="#444")
    if ylabel: ax.set_ylabel(ylabel, fontsize=7.5, color="#444")
    ax.yaxis.grid(True, color="#DDDDDD", linewidth=0.5, linestyle="--")
    ax.set_axisbelow(True)


fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor(BG)
fig.suptitle(
    f"SKE vs CPE Football Battle — Statistics Dashboard  ({total} matches)",
    fontsize=15, fontweight="bold", color=TEXT, y=0.98
)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.52, wspace=0.38,
                       left=0.06, right=0.97, top=0.93, bottom=0.06)

sec = dict(fontsize=8, fontweight="bold", color="#555", transform=fig.transFigure, ha="left")
fig.text(0.06, 0.956, "▌ MATCH OVERVIEW", **sec)
fig.text(0.06, 0.636, "▌ PLAYER ACTIVITY  (Proposal: kicks · jumps)", **sec)
fig.text(0.06, 0.316, "▌ GAMEPLAY FLOW & INSIGHT", **sec)


# ── Row 1: Match Overview ────────────────────────────────────────────────────

ax = fig.add_subplot(gs[0, 0])
style(ax, "Final Score by Match", "Match ID", "Goals")
ax.plot(last["match_id"], last["score_p1"], "o-",
        color=SKE_YELLOW, lw=1.3, ms=3, label="SKE")
ax.plot(last["match_id"], last["score_p2"], "o-",
        color=CPE_BLUE, lw=1.3, ms=3, label="CPE")
ax.legend(fontsize=8, framealpha=0.7)

ax = fig.add_subplot(gs[0, 1])
style(ax, "Win Rate  ↔  Win Record", "", "Matches")
ske_w = int((last["score_p1"] > last["score_p2"]).sum())
draw_ = int((last["score_p1"] == last["score_p2"]).sum())
cpe_w = int((last["score_p1"] < last["score_p2"]).sum())
ske_wr = round(ske_w / total * 100) if total else 0
cpe_wr = round(cpe_w / total * 100) if total else 0
bars = ax.bar(["SKE", "DRAW", "CPE"], [ske_w, draw_, cpe_w],
              color=[SKE_YELLOW, DRAW_GRAY, CPE_BLUE],
              edgecolor="#888", linewidth=0.5, width=0.45)
for b, v, pct in zip(bars, [ske_w, draw_, cpe_w],
                     [f"{ske_wr}%", "", f"{cpe_wr}%"]):
    ax.text(b.get_x() + b.get_width()/2, v + 0.4, str(v),
            ha="center", va="bottom", fontsize=10, fontweight="bold", color=TEXT)
    if pct:
        ax.text(b.get_x() + b.get_width()/2, v / 2, pct,
                ha="center", va="center", fontsize=9, color="white", fontweight="bold")

ax = fig.add_subplot(gs[0, 2])
style(ax, "Shot Accuracy by Match\n(shots ÷ kicks %)", "Match ID", "Accuracy (%)")
acc_p1 = (last["shots_p1"] / last["kicks_p1"].replace(0, float("nan")) * 100).fillna(0)
acc_p2 = (last["shots_p2"] / last["kicks_p2"].replace(0, float("nan")) * 100).fillna(0)
ax.plot(last["match_id"], acc_p1, "o-", color=SKE_YELLOW, lw=1.2, ms=3, label="SKE")
ax.plot(last["match_id"], acc_p2, "o-", color=CPE_BLUE,   lw=1.2, ms=3, label="CPE")
ax.axhline(acc_p1.mean(), color=SKE_YELLOW, lw=1, ls="--", alpha=0.6)
ax.axhline(acc_p2.mean(), color=CPE_BLUE,   lw=1, ls="--", alpha=0.6)
ax.legend(fontsize=8)


# ── Row 2: Player Activity ───────────────────────────────────────────────────

ax = fig.add_subplot(gs[1, 0])
style(ax, "Kicks per Match  ✦ Proposal", "Match ID", "Kicks")
w = 0.4
ax.bar(last["match_id"] - w/2, last["kicks_p1"], width=w,
       color=SKE_YELLOW, edgecolor=GREEN_DARK, lw=0.3, label="SKE")
ax.bar(last["match_id"] + w/2, last["kicks_p2"], width=w,
       color=CPE_BLUE, edgecolor=GREEN_DARK, lw=0.3, label="CPE")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[1, 1])
style(ax, "Jumps per Match  ✦ Proposal", "Match ID", "Jumps")
ax.bar(last["match_id"] - w/2, last["jumps_p1"], width=w,
       color=SKE_YELLOW, edgecolor=GREEN_DARK, lw=0.3, label="SKE")
ax.bar(last["match_id"] + w/2, last["jumps_p2"], width=w,
       color=CPE_BLUE, edgecolor=GREEN_DARK, lw=0.3, label="CPE")
ax.legend(fontsize=8)

ax = fig.add_subplot(gs[1, 2])
style(ax, "Total Shots & Touches", "", "Count")
cats   = ["SKE\nShots", "CPE\nShots", "SKE\nTouches", "CPE\nTouches"]
vals   = [int(last["shots_p1"].sum()), int(last["shots_p2"].sum()),
          int(last["touches_p1"].sum()), int(last["touches_p2"].sum())]
bars   = ax.bar(cats, vals,
                color=[SKE_YELLOW, CPE_BLUE, SKE_YELLOW, CPE_BLUE],
                edgecolor=GREEN_DARK, lw=0.7, width=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + max(vals)*0.01,
            f"{v:,}", ha="center", va="bottom",
            fontsize=8, fontweight="bold", color=TEXT)


# ── Row 3: Gameplay Flow & Insight ───────────────────────────────────────────

ax = fig.add_subplot(gs[2, 0])
style(ax, "Avg Score Diff Over Time\n(SKE – CPE)", "Time (s)", "Diff")
sd = avg_by_time["score_diff"]
ax.plot(avg_by_time["time"], sd, color=SKE_YELLOW, lw=1.6)
ax.axhline(0, color="#999", lw=0.8, ls="--")
ax.fill_between(avg_by_time["time"], sd, 0,
                where=(sd >= 0), alpha=0.28, color=SKE_YELLOW, label="SKE ahead")
ax.fill_between(avg_by_time["time"], sd, 0,
                where=(sd < 0), alpha=0.28, color=CPE_BLUE, label="CPE ahead")
ax.legend(fontsize=7)

ax = fig.add_subplot(gs[2, 1])
ax.set_facecolor(BG)
ax.set_title("Avg Possession", fontsize=9.5, fontweight="bold", color=TEXT, pad=5)
avg_ske = df["possession"].mean()
wedges, texts, autotexts = ax.pie(
    [avg_ske, 100 - avg_ske],
    labels=["SKE", "CPE"],
    colors=[SKE_YELLOW, CPE_BLUE],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 10, "fontweight": "bold"},
)
for at in autotexts:
    at.set_fontsize(9)

ax = fig.add_subplot(gs[2, 2])
style(ax, "Possession vs Result\n(Does more possession = win?)",
      "Avg Possession SKE (%)", "Score Diff (SKE – CPE)")
poss_m  = df.groupby("match_id")["possession"].mean().reset_index()
poss_m.columns = ["match_id", "avg_poss"]
merged  = last.merge(poss_m, on="match_id")
cmap    = {"p1": SKE_YELLOW, "p2": CPE_BLUE, "draw": DRAW_GRAY}
lmap    = {"p1": "SKE Win",  "p2": "CPE Win", "draw": "Draw"}
plotted = set()
for _, row in merged.iterrows():
    w   = row["winner"]
    lbl = lmap.get(w, "")
    kw  = dict(color=cmap.get(w, DRAW_GRAY), edgecolors="#444",
               linewidth=0.5, s=55, alpha=0.85, zorder=3)
    if lbl not in plotted:
        ax.scatter(row["avg_poss"], row["score_p1"] - row["score_p2"],
                   label=lbl, **kw)
        plotted.add(lbl)
    else:
        ax.scatter(row["avg_poss"], row["score_p1"] - row["score_p2"], **kw)
ax.axhline(0, color="#999", lw=0.8, ls="--")
ax.axvline(50, color="#999", lw=0.8, ls="--")
clean = merged.dropna(subset=["avg_poss", "score_p1", "score_p2"])
if len(clean) >= 2:
    z    = np.polyfit(clean["avg_poss"], clean["score_p1"] - clean["score_p2"], 1)
    xfit = np.linspace(clean["avg_poss"].min(), clean["avg_poss"].max(), 100)
    ax.plot(xfit, np.poly1d(z)(xfit), color="tomato", lw=1.4, label="Trend")
ax.legend(fontsize=7, framealpha=0.7)

fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"[analyze] Saved → {OUT_FILE}")
plt.show()
