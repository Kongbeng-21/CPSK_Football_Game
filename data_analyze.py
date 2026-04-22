import pandas as pd
import matplotlib
matplotlib.use("Agg")                   # non-interactive backend — no GUI conflict
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import glob

# ── Config ────────────────────────────────────────────────────────────────────
CSV_PATH = "game_data.csv"
OUT_DIR  = "stats"
OUT_FILE = os.path.join(OUT_DIR, "stats_dashboard.png")
os.makedirs(OUT_DIR, exist_ok=True)

SKE_YELLOW = "#F5C518"
CPE_BLUE   = "#4A9EE0"
DRAW_GRAY  = "#AAAAAA"
GREEN_DARK = "#1A5C1A"
BG         = "#F4F8F4"
SIDEBAR_BG = "#1E3A1E"
TEXT       = "#1A1A1A"

# ── Load data ─────────────────────────────────────────────────────────────────
if not os.path.exists(CSV_PATH):
    print(f"[analyze] {CSV_PATH} not found — play at least one match first.")
    exit()

df = pd.read_csv(CSV_PATH)
numeric_cols = ["ball_speed", "score_p1", "score_p2", "score_diff",
                "kicks_p1", "kicks_p2", "jumps_p1", "jumps_p2",
                "possession", "touches_p1", "touches_p2", "shots_p1", "shots_p2"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

last        = df.groupby("match_id").last().reset_index()
avg_by_time = df.groupby("time").mean(numeric_only=True).reset_index()
total       = len(last)
bs          = df["ball_speed"]
ske_w       = int((last["score_p1"] > last["score_p2"]).sum())
draw_       = int((last["score_p1"] == last["score_p2"]).sum())
cpe_w       = int((last["score_p1"] < last["score_p2"]).sum())
ske_wr      = round(ske_w / total * 100) if total else 0
cpe_wr      = round(cpe_w / total * 100) if total else 0
acc_p1      = (last["shots_p1"] / last["kicks_p1"].replace(0, float("nan")) * 100).fillna(0)
acc_p2      = (last["shots_p2"] / last["kicks_p2"].replace(0, float("nan")) * 100).fillna(0)
poss_m      = df.groupby("match_id")["possession"].mean().reset_index()
poss_m.columns = ["match_id", "avg_poss"]
merged      = last.merge(poss_m, on="match_id")

print(f"[analyze] {total} matches  |  {len(df):,} rows loaded")

# ── Console summary ───────────────────────────────────────────────────────────
print(f"\n{'='*55}")
print(f"  SUMMARY STATISTICS  ({total} matches, {len(df):,} rows)")
print(f"{'='*55}")
print(f"  {'Feature':<28} {'Mean':>7} {'Min':>6} {'Max':>6}")
print(f"  {'-'*52}")
for name, col in [("Kicks SKE", "kicks_p1"), ("Kicks CPE", "kicks_p2"),
                  ("Jumps SKE", "jumps_p1"), ("Jumps CPE", "jumps_p2"),
                  ("Goals SKE", "score_p1"), ("Goals CPE", "score_p2")]:
    s = last[col]
    print(f"  {name+' (per match)':<28} {s.mean():>7.2f} {s.min():>6.0f} {s.max():>6.0f}")
print(f"  {'Ball speed (per sec)':<28} {bs.mean():>7.2f} {bs.min():>6.0f} {bs.max():>6.0f}")
print(f"  {'-'*52}")
print(f"  Win record  SKE {ske_w}W | Draw {draw_} | CPE {cpe_w}W (/{total})")
print(f"{'='*55}\n")


# ── Shared style helper ───────────────────────────────────────────────────────
def style(ax, title="", xlabel="", ylabel="", fs=13, cat_color=TEXT):
    ax.set_facecolor("#EEF7EE")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    ax.tick_params(colors=TEXT, labelsize=10)
    ax.set_title(title, fontsize=fs, fontweight="bold", color=cat_color, pad=10)
    if xlabel: ax.set_xlabel(xlabel, fontsize=10, color="#444")
    if ylabel: ax.set_ylabel(ylabel, fontsize=10, color="#444")
    ax.yaxis.grid(True, color="#DDDDDD", linewidth=0.6, linestyle="--")
    ax.set_axisbelow(True)


# ── Individual panel draw functions ──────────────────────────────────────────
C1 = "#2E7D32"   # MATCH OVERVIEW color
C2 = "#1565C0"   # PLAYER ACTIVITY color
C3 = "#6A1B4D"   # GAMEPLAY FLOW color
C4 = "#BF360C"   # SUMMARY STATS color

def draw_score(ax):
    style(ax, "Final Score by Match", "Match ID", "Goals", cat_color=C1)
    ax.plot(last["match_id"], last["score_p1"], "o-",
            color=SKE_YELLOW, lw=1.8, ms=5, label="SKE")
    ax.plot(last["match_id"], last["score_p2"], "o-",
            color=CPE_BLUE, lw=1.8, ms=5, label="CPE")
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=11, framealpha=0.8)

def draw_winrate(ax):
    style(ax, "Win Rate  &  Win Record", "", "Number of Matches", cat_color=C1)
    vals    = [ske_w, draw_, cpe_w]
    max_val = max(vals)
    bars    = ax.bar(["SKE", "DRAW", "CPE"], vals,
                     color=[SKE_YELLOW, DRAW_GRAY, CPE_BLUE],
                     edgecolor="#888", linewidth=0.8, width=0.45)
    ax.set_ylim(0, max_val * 1.30)
    for b, v, pct in zip(bars, vals, [f"{ske_wr}%", "", f"{cpe_wr}%"]):
        ax.text(b.get_x() + b.get_width()/2, v + max_val * 0.02,
                str(v), ha="center", va="bottom",
                fontsize=14, fontweight="bold", color=TEXT)
        if pct and v > 0:
            ax.text(b.get_x() + b.get_width()/2, v * 0.5, pct,
                    ha="center", va="center",
                    fontsize=13, color="white", fontweight="bold")

def draw_accuracy(ax):
    # Cap accuracy at 100% (shots can exceed kicks due to tracking logic)
    a1 = acc_p1.clip(upper=100)
    a2 = acc_p2.clip(upper=100)
    style(ax, "Shot Accuracy by Match  (shots ÷ kicks × 100%)",
          "Match ID", "Accuracy (%)", cat_color=C1)
    ax.plot(last["match_id"], a1, "o-", color=SKE_YELLOW, lw=1.6, ms=4, label="SKE")
    ax.plot(last["match_id"], a2, "o-", color=CPE_BLUE,   lw=1.6, ms=4, label="CPE")
    ax.axhline(a1.mean(), color=SKE_YELLOW, lw=1.4, ls="--", alpha=0.8,
               label=f"SKE avg {a1.mean():.1f}%")
    ax.axhline(a2.mean(), color=CPE_BLUE,   lw=1.4, ls="--", alpha=0.8,
               label=f"CPE avg {a2.mean():.1f}%")
    ax.set_ylim(0, 108)
    ax.legend(fontsize=10)

def draw_kicks(ax):
    w = 0.4
    style(ax, "Kicks per Match  ✦ Proposal Feature", "Match ID", "Kicks", cat_color=C2)
    ax.bar(last["match_id"] - w/2, last["kicks_p1"], width=w,
           color=SKE_YELLOW, edgecolor=GREEN_DARK, lw=0.4,
           label=f"SKE  (avg {last['kicks_p1'].mean():.1f})")
    ax.bar(last["match_id"] + w/2, last["kicks_p2"], width=w,
           color=CPE_BLUE, edgecolor=GREEN_DARK, lw=0.4,
           label=f"CPE  (avg {last['kicks_p2'].mean():.1f})")
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=11)

def draw_jumps(ax):
    w = 0.4
    style(ax, "Jumps per Match  ✦ Proposal Feature", "Match ID", "Jumps", cat_color=C2)
    ax.bar(last["match_id"] - w/2, last["jumps_p1"], width=w,
           color=SKE_YELLOW, edgecolor=GREEN_DARK, lw=0.4,
           label=f"SKE  (avg {last['jumps_p1'].mean():.1f})")
    ax.bar(last["match_id"] + w/2, last["jumps_p2"], width=w,
           color=CPE_BLUE, edgecolor=GREEN_DARK, lw=0.4,
           label=f"CPE  (avg {last['jumps_p2'].mean():.1f})")
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=11)

def draw_shots_touches(ax):
    style(ax, "Total Shots & Touches  (cumulative across all matches)",
          "", "Count", cat_color=C2)
    cats = ["SKE Shots", "CPE Shots", "SKE Touches", "CPE Touches"]
    vals = [int(last["shots_p1"].sum()), int(last["shots_p2"].sum()),
            int(last["touches_p1"].sum()), int(last["touches_p2"].sum())]
    colors = [SKE_YELLOW, CPE_BLUE, SKE_YELLOW, CPE_BLUE]
    bars = ax.bar(cats, vals, color=colors, edgecolor=GREEN_DARK, lw=0.8, width=0.5)
    max_v = max(vals)
    ax.set_ylim(0, max_v * 1.18)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + max_v * 0.025,
                f"{v:,}", ha="center", va="bottom",
                fontsize=12, fontweight="bold", color=TEXT)

def draw_score_diff(ax):
    style(ax, "Average Score Difference Over Time  (SKE − CPE)",
          "Time (seconds)", "Score Difference", cat_color=C3)
    sd = avg_by_time["score_diff"]
    ax.plot(avg_by_time["time"], sd, color=SKE_YELLOW, lw=2.2)
    ax.axhline(0, color="#888", lw=1.2, ls="--")
    ax.fill_between(avg_by_time["time"], sd, 0,
                    where=(sd >= 0), alpha=0.30, color=SKE_YELLOW, label="SKE ahead on average")
    ax.fill_between(avg_by_time["time"], sd, 0,
                    where=(sd < 0), alpha=0.30, color=CPE_BLUE, label="CPE ahead on average")
    ax.legend(fontsize=11)

def draw_possession(ax):
    ax.set_facecolor(BG)
    avg_ske = df["possession"].mean()
    ax.set_title(f"Average Ball Possession  ({total} matches)",
                 fontsize=13, fontweight="bold", color=C3, pad=10)
    wedges, texts, autotexts = ax.pie(
        [avg_ske, 100 - avg_ske],
        labels=["SKE", "CPE"],
        colors=[SKE_YELLOW, CPE_BLUE],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 3},
        textprops={"fontsize": 15, "fontweight": "bold"},
        radius=0.85,
    )
    for at in autotexts:
        at.set_fontsize(13)

def draw_poss_result(ax):
    style(ax, "Possession vs Result  (does more possession = winning?)",
          "Avg Possession SKE (%)", "Score Diff (SKE − CPE)", cat_color=C3)
    cmap_ = {"p1": SKE_YELLOW, "p2": CPE_BLUE, "draw": DRAW_GRAY}
    lmap_ = {"p1": "SKE Win",  "p2": "CPE Win", "draw": "Draw"}
    plotted = set()
    for _, row in merged.iterrows():
        w   = row["winner"]
        lbl = lmap_.get(w, "")
        kw  = dict(color=cmap_.get(w, DRAW_GRAY), edgecolors="#444",
                   linewidth=0.6, s=75, alpha=0.85, zorder=3)
        if lbl and lbl not in plotted:
            ax.scatter(row["avg_poss"], row["score_p1"] - row["score_p2"],
                       label=lbl, **kw)
            plotted.add(lbl)
        else:
            ax.scatter(row["avg_poss"], row["score_p1"] - row["score_p2"], **kw)
    ax.axhline(0, color="#888", lw=1, ls="--")
    ax.axvline(50, color="#888", lw=1, ls="--")
    clean = merged.dropna(subset=["avg_poss", "score_p1", "score_p2"])
    if len(clean) >= 2:
        z    = np.polyfit(clean["avg_poss"], clean["score_p1"] - clean["score_p2"], 1)
        xfit = np.linspace(clean["avg_poss"].min(), clean["avg_poss"].max(), 100)
        ax.plot(xfit, np.poly1d(z)(xfit), color="tomato", lw=2, label="Trend line")
    ax.legend(fontsize=10, framealpha=0.8)

def draw_table(ax):
    ax.axis("off")
    rows = [
        ["Ball speed (per second)",  f"{bs.mean():.2f}",                       f"{bs.min():.2f}",                       f"{bs.max():.2f}",                       "Ball",   "Line graph"],
        ["Kicks — SKE (per match)",  f"{last['kicks_p1'].mean():.1f}",          f"{int(last['kicks_p1'].min())}",        f"{int(last['kicks_p1'].max())}",        "Player", "Bar chart"],
        ["Kicks — CPE (per match)",  f"{last['kicks_p2'].mean():.1f}",          f"{int(last['kicks_p2'].min())}",        f"{int(last['kicks_p2'].max())}",        "Player", "Bar chart"],
        ["Jumps — SKE (per match)",  f"{last['jumps_p1'].mean():.1f}",          f"{int(last['jumps_p1'].min())}",        f"{int(last['jumps_p1'].max())}",        "Player", "Bar chart"],
        ["Jumps — CPE (per match)",  f"{last['jumps_p2'].mean():.1f}",          f"{int(last['jumps_p2'].min())}",        f"{int(last['jumps_p2'].max())}",        "Player", "Bar chart"],
        ["Goals — SKE (per match)",  f"{last['score_p1'].mean():.2f}",          f"{int(last['score_p1'].min())}",        f"{int(last['score_p1'].max())}",        "Game",   "Line chart"],
        ["Goals — CPE (per match)",  f"{last['score_p2'].mean():.2f}",          f"{int(last['score_p2'].min())}",        f"{int(last['score_p2'].max())}",        "Game",   "Line chart"],
        ["Match duration (seconds)", f"{last['match_duration'].mean():.1f}",    f"{int(last['match_duration'].min())}",  f"{int(last['match_duration'].max())}",  "Timer",  "Summary"],
    ]
    headers = ["Feature", "Mean", "Min", "Max", "Source Class", "Display Method"]
    col_w   = [0.28, 0.10, 0.07, 0.07, 0.16, 0.20]
    tbl = ax.table(cellText=rows, colLabels=headers,
                   cellLoc="center", loc="center", colWidths=col_w)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 2.2)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#CCCCCC")
        if r == 0:
            cell.set_facecolor(GREEN_DARK)
            cell.set_text_props(color="white", fontweight="bold")
        elif r % 2 == 0:
            cell.set_facecolor("#DFF2DF")
        else:
            cell.set_facecolor("#F4F8F4")
    win_txt = (f"Win record across {total} matches:  "
               f"SKE {ske_w}W  |  Draw {draw_}  |  CPE {cpe_w}W   "
               f"(SKE {ske_wr}%  /  CPE {cpe_wr}%)")
    ax.text(0.5, 0.02, win_txt, transform=ax.transAxes,
            ha="center", va="bottom", fontsize=10, color="#333",
            fontweight="bold")


# ── Save full dashboard PNG (no UI, Agg-safe) ─────────────────────────────────
for old in glob.glob(os.path.join(OUT_DIR, "*.png")):
    os.remove(old)

_fig = plt.figure(figsize=(18, 18))
_fig.patch.set_facecolor(BG)
_fig.suptitle(f"SKE vs CPE Football Battle — Statistics Dashboard  ({total} matches)",
              fontsize=15, fontweight="bold", color=TEXT, y=0.98)
_gs = gridspec.GridSpec(4, 3, figure=_fig, hspace=0.52, wspace=0.38,
                        left=0.06, right=0.97, top=0.93, bottom=0.04,
                        height_ratios=[1, 1, 1, 0.6])
sec = dict(fontsize=8, fontweight="bold", color="#555", transform=_fig.transFigure, ha="left")
_fig.text(0.06, 0.966, "▌ MATCH OVERVIEW", **sec)
_fig.text(0.06, 0.726, "▌ PLAYER ACTIVITY  (Proposal: kicks · jumps)", **sec)
_fig.text(0.06, 0.486, "▌ GAMEPLAY FLOW & INSIGHT", **sec)
_fig.text(0.06, 0.226, "▌ SUMMARY STATISTICS  (Proposal: Section 4.3)", **sec)

fns_grid = [draw_score, draw_winrate, draw_accuracy,
            draw_kicks, draw_jumps, draw_shots_touches,
            draw_score_diff, draw_possession, draw_poss_result]
for i, fn in enumerate(fns_grid):
    ax_ = _fig.add_subplot(_gs[i // 3, i % 3])
    fn(ax_)

ax_tbl_ = _fig.add_subplot(_gs[3, :])
draw_table(ax_tbl_)

_fig.savefig(OUT_FILE, dpi=150, bbox_inches="tight", facecolor=BG)
plt.close(_fig)
print(f"[analyze] Dashboard saved → {OUT_FILE}")


# ── Interactive viewer (tkinter + Agg + PIL — macOS safe) ────────────────────
# Uses matplotlib Agg to render charts as PNG images, then displays via PIL.
# This avoids all macOS/tkinter backend crashes.

PANELS = [
    ("Final Score by Match",     draw_score,        "MATCH OVERVIEW"),
    ("Win Rate & Win Record",    draw_winrate,       "MATCH OVERVIEW"),
    ("Shot Accuracy by Match",   draw_accuracy,      "MATCH OVERVIEW"),
    ("Kicks per Match",          draw_kicks,         "PLAYER ACTIVITY"),
    ("Jumps per Match",          draw_jumps,         "PLAYER ACTIVITY"),
    ("Total Shots & Touches",    draw_shots_touches, "PLAYER ACTIVITY"),
    ("Score Diff Over Time",     draw_score_diff,    "GAMEPLAY FLOW"),
    ("Avg Possession",           draw_possession,    "GAMEPLAY FLOW"),
    ("Possession vs Result",     draw_poss_result,   "GAMEPLAY FLOW"),
    ("Summary Statistics Table", draw_table,         "SUMMARY STATS"),
]

CATEGORIES = ["MATCH OVERVIEW", "PLAYER ACTIVITY", "GAMEPLAY FLOW", "SUMMARY STATS"]
CAT_PANELS = {c: [(lbl, fn) for lbl, fn, cat in PANELS if cat == c]
              for c in CATEGORIES}
CAT_COLOR_HEX = {
    "MATCH OVERVIEW":  C1,
    "PLAYER ACTIVITY": C2,
    "GAMEPLAY FLOW":   C3,
    "SUMMARY STATS":   C4,
}
TEMP_PNG = os.path.join(OUT_DIR, "_temp_chart.png")

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class StatsViewer:
    IMG_W, IMG_H = 1060, 620   # fixed chart render size (px)

    def __init__(self, root):
        self.root = root
        self.root.title("SKE vs CPE — Statistics Viewer")
        self.root.resizable(False, False)
        self.root.configure(bg="#EAEEF0")

        # ── Top control bar ───────────────────────────────────────────────────
        ctrl = tk.Frame(self.root, bg="#D6DDE0", pady=10, padx=14)
        ctrl.pack(fill="x", side="top")

        tk.Label(ctrl, text="SKE vs CPE  Statistics",
                 bg="#D6DDE0", fg="#1B5E20",
                 font=("Helvetica", 13, "bold")).pack(side=tk.LEFT, padx=(0, 18))
        tk.Label(ctrl, text=f"{total} matches  ·  {len(df):,} rows",
                 bg="#D6DDE0", fg="#555",
                 font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0, 28))

        # Category dropdown
        tk.Label(ctrl, text="Category:",
                 bg="#D6DDE0", font=("Helvetica", 11)).pack(side=tk.LEFT, padx=(0, 5))
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        self.cat_dd  = ttk.Combobox(ctrl, textvariable=self.cat_var,
                                     values=CATEGORIES, width=20, state="readonly",
                                     font=("Helvetica", 11))
        self.cat_dd.pack(side=tk.LEFT, padx=(0, 22))
        self.cat_dd.bind("<<ComboboxSelected>>", self._on_cat)

        # Chart dropdown
        tk.Label(ctrl, text="Chart:",
                 bg="#D6DDE0", font=("Helvetica", 11)).pack(side=tk.LEFT, padx=(0, 5))
        init_charts = [lbl for lbl, _ in CAT_PANELS[CATEGORIES[0]]]
        self.chart_var = tk.StringVar(value=init_charts[0])
        self.chart_dd  = ttk.Combobox(ctrl, textvariable=self.chart_var,
                                       values=init_charts, width=28, state="readonly",
                                       font=("Helvetica", 11))
        self.chart_dd.pack(side=tk.LEFT)
        self.chart_dd.bind("<<ComboboxSelected>>", self._on_chart)

        # ── Coloured category strip ───────────────────────────────────────────
        self.strip = tk.Frame(self.root, height=5,
                              bg=CAT_COLOR_HEX[CATEGORIES[0]])
        self.strip.pack(fill="x", side="top")

        # ── Image display ─────────────────────────────────────────────────────
        self.img_lbl = tk.Label(self.root, bg="#EAEEF0")
        self.img_lbl.pack(padx=10, pady=(6, 10))

        # Apply combobox style
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox", padding=4,
                    fieldbackground="white", background="white")

        self._render()

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _on_cat(self, _=None):
        cat    = self.cat_var.get()
        charts = [lbl for lbl, _ in CAT_PANELS[cat]]
        self.chart_dd["values"] = charts
        self.chart_var.set(charts[0])
        self.strip.configure(bg=CAT_COLOR_HEX[cat])
        self._render()

    def _on_chart(self, _=None):
        self.strip.configure(bg=CAT_COLOR_HEX[self.cat_var.get()])
        self._render()

    # ── Render chart → PNG → display ──────────────────────────────────────────
    def _render(self):
        cat        = self.cat_var.get()
        chart_name = self.chart_var.get()
        fn_map     = {lbl: fn for lbl, fn in CAT_PANELS[cat]}
        draw_fn    = fn_map.get(chart_name)
        if draw_fn is None:
            return

        # Draw with matplotlib (Agg — saves to file, no GUI window)
        dpi = 110
        fig_w = self.IMG_W / dpi
        fig_h = self.IMG_H / dpi
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        draw_fn(ax)
        fig.tight_layout(pad=1.6)
        fig.savefig(TEMP_PNG, dpi=dpi, bbox_inches="tight", facecolor=BG)
        plt.close(fig)

        # Load saved PNG and show in tkinter
        img         = Image.open(TEMP_PNG).resize(
                          (self.IMG_W, self.IMG_H), Image.LANCZOS)
        self.photo  = ImageTk.PhotoImage(img)   # keep reference
        self.img_lbl.config(image=self.photo)


# ── Launch ─────────────────────────────────────────────────────────────────────
root = tk.Tk()
StatsViewer(root)
root.mainloop()
