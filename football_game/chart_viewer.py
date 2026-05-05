"""
chart_viewer.py  — In-game interactive chart browser for CPSK Football Game
Renders matplotlib charts directly onto the Pygame screen via the Agg backend.
Called from game.py as:  run_chart_viewer(screen, clock)
"""

import io
import os
import pygame
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                       # must stay before pyplot import
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── Colours (match data_analyze palette) ──────────────────────────────────────
SKE_YELLOW = "#F5C518"
CPE_BLUE   = "#4A9EE0"
DRAW_GRAY  = "#AAAAAA"
GREEN_DARK = "#1A5C1A"
BG         = "#F4F8F4"
TEXT       = "#1A1A1A"

C1 = "#2E7D32"   # MATCH OVERVIEW
C2 = "#1565C0"   # PLAYER ACTIVITY
C3 = "#6A1B4D"   # GAMEPLAY FLOW
C4 = "#BF360C"   # SUMMARY STATS

CAT_COLOR_HEX = {
    "MATCH OVERVIEW":  C1,
    "PLAYER ACTIVITY": C2,
    "GAMEPLAY FLOW":   C3,
    "SUMMARY STATS":   C4,
}

# Pygame colours
PG_BG        = (18, 44, 18)
PG_TOPBAR    = (12, 30, 12)
PG_BOTBAR    = (10, 26, 10)
PG_WHITE     = (255, 255, 255)
PG_GRAY      = (160, 170, 160)
PG_GOLD      = (255, 210,  0)
PG_BTN_DARK  = (30,  60,  30)
PG_BTN_HOV   = (60, 120,  60)
PG_HINT      = (120, 150, 120)


# ── Data loader ───────────────────────────────────────────────────────────────
def _load_data():
    """Return (df, last, avg_by_time, merged, stats_dict) or None if no CSV."""
    csv = "game_data.csv"
    if not os.path.exists(csv):
        return None

    df = pd.read_csv(csv)
    num = ["ball_speed","score_p1","score_p2","score_diff",
           "kicks_p1","kicks_p2","jumps_p1","jumps_p2",
           "possession","touches_p1","touches_p2","shots_p1","shots_p2"]
    for c in num:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    last        = df.groupby("match_id").last().reset_index()
    avg_by_time = df.groupby("time").mean(numeric_only=True).reset_index()
    poss_m      = df.groupby("match_id")["possession"].mean().reset_index()
    poss_m.columns = ["match_id", "avg_poss"]
    merged      = last.merge(poss_m, on="match_id")

    total  = len(last)
    bs     = df["ball_speed"]
    ske_w  = int((last["score_p1"] > last["score_p2"]).sum())
    draw_  = int((last["score_p1"] == last["score_p2"]).sum())
    cpe_w  = int((last["score_p1"] < last["score_p2"]).sum())
    ske_wr = round(ske_w / total * 100) if total else 0
    cpe_wr = round(cpe_w / total * 100) if total else 0
    acc_p1 = (last["shots_p1"] / last["kicks_p1"].replace(0, float("nan")) * 100).fillna(0)
    acc_p2 = (last["shots_p2"] / last["kicks_p2"].replace(0, float("nan")) * 100).fillna(0)

    return dict(df=df, last=last, avg_by_time=avg_by_time, merged=merged,
                total=total, bs=bs, ske_w=ske_w, draw_=draw_, cpe_w=cpe_w,
                ske_wr=ske_wr, cpe_wr=cpe_wr, acc_p1=acc_p1, acc_p2=acc_p2)


# ── Style helper ──────────────────────────────────────────────────────────────
def _style(ax, title="", xlabel="", ylabel="", fs=13, cat_color=TEXT):
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


# ── Draw functions (one per panel) ───────────────────────────────────────────
def _make_draw_fns(d):
    """Return list of (label, category, draw_fn(ax)) tuples given loaded data dict d."""

    last        = d["last"]
    avg_by_time = d["avg_by_time"]
    merged      = d["merged"]
    df          = d["df"]
    bs          = d["bs"]
    ske_w, draw_, cpe_w = d["ske_w"], d["draw_"], d["cpe_w"]
    ske_wr, cpe_wr      = d["ske_wr"], d["cpe_wr"]
    acc_p1, acc_p2      = d["acc_p1"], d["acc_p2"]
    total               = d["total"]

    def draw_score(ax):
        _style(ax, "Final Score by Match", "Match ID", "Goals", cat_color=C1)
        ax.plot(last["match_id"], last["score_p1"], "o-",
                color=SKE_YELLOW, lw=1.8, ms=5, label="SKE")
        ax.plot(last["match_id"], last["score_p2"], "o-",
                color=CPE_BLUE,   lw=1.8, ms=5, label="CPE")
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=11, framealpha=0.8)

    def draw_winrate(ax):
        _style(ax, "Win Rate  &  Win Record", "", "Number of Matches", cat_color=C1)
        vals    = [ske_w, draw_, cpe_w]
        max_val = max(vals) if max(vals) > 0 else 1
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
        a1 = acc_p1.clip(upper=100)
        a2 = acc_p2.clip(upper=100)
        _style(ax, "Shot Accuracy by Match  (shots / kicks x 100%)",
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
        _style(ax, "Kicks per Match", "Match ID", "Kicks", cat_color=C2)
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
        _style(ax, "Jumps per Match", "Match ID", "Jumps", cat_color=C2)
        ax.bar(last["match_id"] - w/2, last["jumps_p1"], width=w,
               color=SKE_YELLOW, edgecolor=GREEN_DARK, lw=0.4,
               label=f"SKE  (avg {last['jumps_p1'].mean():.1f})")
        ax.bar(last["match_id"] + w/2, last["jumps_p2"], width=w,
               color=CPE_BLUE, edgecolor=GREEN_DARK, lw=0.4,
               label=f"CPE  (avg {last['jumps_p2'].mean():.1f})")
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=11)

    def draw_shots_touches(ax):
        _style(ax, "Total Shots & Touches  (all matches combined)",
               "", "Count", cat_color=C2)
        cats   = ["SKE Shots", "CPE Shots", "SKE Touches", "CPE Touches"]
        vals   = [int(last["shots_p1"].sum()), int(last["shots_p2"].sum()),
                  int(last["touches_p1"].sum()), int(last["touches_p2"].sum())]
        colors = [SKE_YELLOW, CPE_BLUE, SKE_YELLOW, CPE_BLUE]
        bars   = ax.bar(cats, vals, color=colors, edgecolor=GREEN_DARK,
                        lw=0.8, width=0.5)
        max_v  = max(vals) if max(vals) > 0 else 1
        ax.set_ylim(0, max_v * 1.18)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + max_v * 0.025,
                    f"{v:,}", ha="center", va="bottom",
                    fontsize=12, fontweight="bold", color=TEXT)

    def draw_score_diff(ax):
        _style(ax, "Average Score Difference Over Time  (SKE - CPE)",
               "Time (seconds)", "Score Difference", cat_color=C3)
        sd = avg_by_time["score_diff"]
        ax.plot(avg_by_time["time"], sd, color=SKE_YELLOW, lw=2.2)
        ax.axhline(0, color="#888", lw=1.2, ls="--")
        ax.fill_between(avg_by_time["time"], sd, 0,
                        where=(sd >= 0), alpha=0.30, color=SKE_YELLOW,
                        label="SKE ahead on average")
        ax.fill_between(avg_by_time["time"], sd, 0,
                        where=(sd < 0),  alpha=0.30, color=CPE_BLUE,
                        label="CPE ahead on average")
        ax.legend(fontsize=11)

    def draw_possession(ax):
        ax.set_facecolor(BG)
        avg_ske = df["possession"].mean()
        ax.set_title(f"Average Ball Possession  ({total} matches)",
                     fontsize=13, fontweight="bold", color=C3, pad=10)
        _, _, autotexts = ax.pie(
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
        _style(ax, "Possession vs Result  (more possession = winning?)",
               "Avg Possession SKE (%)", "Score Diff (SKE - CPE)", cat_color=C3)
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
            z    = np.polyfit(clean["avg_poss"],
                              clean["score_p1"] - clean["score_p2"], 1)
            xfit = np.linspace(clean["avg_poss"].min(), clean["avg_poss"].max(), 100)
            ax.plot(xfit, np.poly1d(z)(xfit), color="tomato", lw=2, label="Trend")
        ax.legend(fontsize=10, framealpha=0.8)

    def draw_table(ax):
        ax.axis("off")
        rows = [
            ["Ball speed (per sec)",  f"{bs.mean():.2f}",
             f"{bs.min():.2f}",  f"{bs.max():.2f}",  "Ball",   "Line graph"],
            ["Kicks — SKE (per match)", f"{last['kicks_p1'].mean():.1f}",
             f"{int(last['kicks_p1'].min())}", f"{int(last['kicks_p1'].max())}",
             "Player", "Bar chart"],
            ["Kicks — CPE (per match)", f"{last['kicks_p2'].mean():.1f}",
             f"{int(last['kicks_p2'].min())}", f"{int(last['kicks_p2'].max())}",
             "Player", "Bar chart"],
            ["Jumps — SKE (per match)", f"{last['jumps_p1'].mean():.1f}",
             f"{int(last['jumps_p1'].min())}", f"{int(last['jumps_p1'].max())}",
             "Player", "Bar chart"],
            ["Jumps — CPE (per match)", f"{last['jumps_p2'].mean():.1f}",
             f"{int(last['jumps_p2'].min())}", f"{int(last['jumps_p2'].max())}",
             "Player", "Bar chart"],
            ["Goals — SKE (per match)", f"{last['score_p1'].mean():.2f}",
             f"{int(last['score_p1'].min())}", f"{int(last['score_p1'].max())}",
             "Game",   "Line chart"],
            ["Goals — CPE (per match)", f"{last['score_p2'].mean():.2f}",
             f"{int(last['score_p2'].min())}", f"{int(last['score_p2'].max())}",
             "Game",   "Line chart"],
        ]
        headers = ["Feature", "Mean", "Min", "Max", "Source Class", "Display Method"]
        col_w   = [0.30, 0.10, 0.07, 0.07, 0.18, 0.22]
        tbl = ax.table(cellText=rows, colLabels=headers,
                       cellLoc="center", loc="center", colWidths=col_w)
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1, 2.0)
        for (r, c), cell in tbl.get_celld().items():
            cell.set_edgecolor("#CCCCCC")
            if r == 0:
                cell.set_facecolor(GREEN_DARK)
                cell.set_text_props(color="white", fontweight="bold")
            elif r % 2 == 0:
                cell.set_facecolor("#DFF2DF")
            else:
                cell.set_facecolor(BG)
        win_txt = (f"Win record ({total} matches):  "
                   f"SKE {ske_w}W  |  Draw {draw_}  |  CPE {cpe_w}W   "
                   f"(SKE {ske_wr}%  /  CPE {cpe_wr}%)")
        ax.text(0.5, 0.02, win_txt, transform=ax.transAxes,
                ha="center", va="bottom", fontsize=10, color="#333",
                fontweight="bold")

    return [
        ("Final Score by Match",     "MATCH OVERVIEW",  draw_score),
        ("Win Rate & Win Record",    "MATCH OVERVIEW",  draw_winrate),
        ("Shot Accuracy by Match",   "MATCH OVERVIEW",  draw_accuracy),
        ("Kicks per Match",          "PLAYER ACTIVITY", draw_kicks),
        ("Jumps per Match",          "PLAYER ACTIVITY", draw_jumps),
        ("Total Shots & Touches",    "PLAYER ACTIVITY", draw_shots_touches),
        ("Score Diff Over Time",     "GAMEPLAY FLOW",   draw_score_diff),
        ("Average Possession",       "GAMEPLAY FLOW",   draw_possession),
        ("Possession vs Result",     "GAMEPLAY FLOW",   draw_poss_result),
        ("Summary Statistics Table", "SUMMARY STATS",   draw_table),
    ]


# ── matplotlib → pygame Surface ───────────────────────────────────────────────
def _render_to_surface(draw_fn, width, height):
    """Render one chart to a pygame Surface via Agg → BytesIO."""
    dpi   = 110
    fig_w = width  / dpi
    fig_h = height / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    draw_fn(ax)
    fig.tight_layout(pad=1.5)
    buf = io.BytesIO()
    fig.savefig(buf, format="PNG", dpi=dpi,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return pygame.image.load(buf, "chart.png").convert()


# ── Helpers ───────────────────────────────────────────────────────────────────
def _hex_to_pg(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _draw_pill(surf, rect, color, radius=10):
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def _arrow_polygon(cx, cy, size, direction="left"):
    if direction == "left":
        return [(cx + size, cy - size), (cx - size, cy), (cx + size, cy + size)]
    return [(cx - size, cy - size), (cx + size, cy), (cx - size, cy + size)]


# ── Main viewer loop ──────────────────────────────────────────────────────────
def run_chart_viewer(screen, clock):
    """
    Full-screen in-game chart browser.
    Returns when the user presses ESC or closes the viewer.
    """
    W, H = screen.get_size()

    # ── Load data ──────────────────────────────────────────────────────────────
    data = _load_data()
    if data is None:
        _draw_no_data(screen, W, H)
        clock.tick(30)
        pygame.event.clear()
        _wait_for_esc(screen, W, H, clock)
        return

    panels     = _make_draw_fns(data)    # [(label, category, fn), ...]
    total      = data["total"]
    n_panels   = len(panels)

    # ── State ──────────────────────────────────────────────────────────────────
    idx        = 0          # current panel index
    cache      = {}         # {idx: pygame.Surface}

    # Chart area
    TOP_H   = 56            # header bar height
    BOT_H   = 38            # footer bar height
    CHART_H = H - TOP_H - BOT_H
    CHART_W = W

    # ── Font setup ─────────────────────────────────────────────────────────────
    pygame.font.init()
    fn_bold  = pygame.font.SysFont("Avenir Next Condensed", 22, bold=True)
    fn_med   = pygame.font.SysFont("Avenir Next Condensed", 18, bold=False)
    fn_small = pygame.font.SysFont("Avenir Next Condensed", 16, bold=False)
    fn_nav   = pygame.font.SysFont("Avenir Next Condensed", 28, bold=True)

    def get_surface(i):
        if i not in cache:
            # Show loading indicator
            loading_surf = pygame.Surface((CHART_W, CHART_H))
            loading_surf.fill((20, 50, 20))
            lbl = panels[i][0]
            msg = fn_bold.render(f"Loading  {lbl} ...", True, (200, 230, 200))
            loading_surf.blit(msg, msg.get_rect(center=(CHART_W//2, CHART_H//2)))
            screen.blit(loading_surf, (0, TOP_H))
            pygame.display.flip()

            cache[i] = _render_to_surface(panels[i][2], CHART_W, CHART_H)
        return cache[i]

    # Pre-render current panel immediately
    get_surface(idx)

    # NAV button rects (in header)
    NAV_BTN_W, NAV_BTN_H = 44, 36
    btn_prev = pygame.Rect(8, (TOP_H - NAV_BTN_H)//2, NAV_BTN_W, NAV_BTN_H)
    btn_next = pygame.Rect(W - NAV_BTN_W - 8, (TOP_H - NAV_BTN_H)//2,
                           NAV_BTN_W, NAV_BTN_H)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    running = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    idx = (idx + 1) % n_panels
                    get_surface(idx)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    idx = (idx - 1) % n_panels
                    get_surface(idx)
                # Number keys 1-4 jump to first panel of each category
                elif event.key == pygame.K_1:
                    idx = 0; get_surface(idx)
                elif event.key == pygame.K_2:
                    idx = 3; get_surface(idx)
                elif event.key == pygame.K_3:
                    idx = 6; get_surface(idx)
                elif event.key == pygame.K_4:
                    idx = 9; get_surface(idx)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_prev.collidepoint(event.pos):
                    idx = (idx - 1) % n_panels
                    get_surface(idx)
                elif btn_next.collidepoint(event.pos):
                    idx = (idx + 1) % n_panels
                    get_surface(idx)

        # ── Draw ──────────────────────────────────────────────────────────────
        label, category, _ = panels[idx]
        cat_color_pg = _hex_to_pg(CAT_COLOR_HEX[category])

        # — Header bar —
        pygame.draw.rect(screen, PG_TOPBAR, (0, 0, W, TOP_H))
        # Category accent strip (left 6px)
        pygame.draw.rect(screen, cat_color_pg, (0, 0, 6, TOP_H))

        # PREV button
        prev_col = PG_BTN_HOV if btn_prev.collidepoint(mouse_pos) else PG_BTN_DARK
        _draw_pill(screen, btn_prev, prev_col, 8)
        pts_l = _arrow_polygon(btn_prev.centerx, btn_prev.centery, 8, "left")
        pygame.draw.polygon(screen, PG_WHITE, pts_l)

        # NEXT button
        next_col = PG_BTN_HOV if btn_next.collidepoint(mouse_pos) else PG_BTN_DARK
        _draw_pill(screen, btn_next, next_col, 8)
        pts_r = _arrow_polygon(btn_next.centerx, btn_next.centery, 8, "right")
        pygame.draw.polygon(screen, PG_WHITE, pts_r)

        # Category label (coloured)
        cat_surf = fn_med.render(category, True, cat_color_pg)
        # Chart name (white)
        chart_surf = fn_bold.render(label, True, PG_WHITE)
        # Counter  e.g.  3 / 10
        counter_surf = fn_med.render(f"{idx+1} / {n_panels}", True, PG_GRAY)

        # Lay out: [PREV] [cat · label] [counter] [NEXT]
        center_x = W // 2
        cat_surf_w = cat_surf.get_width()
        sep_surf   = fn_med.render("  |  ", True, (80, 110, 80))
        total_w    = cat_surf_w + sep_surf.get_width() + chart_surf.get_width()
        start_x    = center_x - total_w // 2

        ty = (TOP_H - cat_surf.get_height()) // 2
        screen.blit(cat_surf,   (start_x, ty))
        screen.blit(sep_surf,   (start_x + cat_surf_w, ty))
        screen.blit(chart_surf, (start_x + cat_surf_w + sep_surf.get_width(), ty))
        screen.blit(counter_surf, counter_surf.get_rect(right=btn_next.left - 14, centery=TOP_H//2))

        # — Chart area —
        chart_surf_img = get_surface(idx)
        # Scale to fit if needed
        cw, ch = chart_surf_img.get_size()
        if (cw, ch) != (CHART_W, CHART_H):
            chart_surf_img = pygame.transform.smoothscale(
                chart_surf_img, (CHART_W, CHART_H))
            cache[idx] = chart_surf_img
        screen.blit(chart_surf_img, (0, TOP_H))

        # — Category indicator strip under chart —
        pygame.draw.rect(screen, cat_color_pg, (0, TOP_H + CHART_H, W, 3))

        # — Footer bar —
        pygame.draw.rect(screen, PG_BOTBAR, (0, H - BOT_H, W, BOT_H))
        hints = ("LEFT / RIGHT  navigate     1 Match Overview  "
                 "2 Player Activity  3 Gameplay Flow  4 Summary     ESC back")
        hint_surf = fn_small.render(hints, True, PG_HINT)
        screen.blit(hint_surf, hint_surf.get_rect(center=(W//2, H - BOT_H//2)))

        # Cursor
        on_btn = btn_prev.collidepoint(mouse_pos) or btn_next.collidepoint(mouse_pos)
        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_HAND if on_btn else pygame.SYSTEM_CURSOR_ARROW
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


# ── No-data fallback ──────────────────────────────────────────────────────────
def _draw_no_data(screen, W, H):
    screen.fill(PG_BG)
    fn = pygame.font.SysFont("Avenir Next Condensed", 32, bold=True)
    msg = fn.render("No match data found — play at least one match first!", True, (220, 180, 80))
    screen.blit(msg, msg.get_rect(center=(W//2, H//2)))
    pygame.display.flip()

def _wait_for_esc(screen, W, H, clock):
    fn = pygame.font.SysFont("Avenir Next Condensed", 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                return
        hint = fn.render("Press any key to return", True, (150, 170, 150))
        screen.blit(hint, hint.get_rect(center=(screen.get_width()//2,
                                                screen.get_height()//2 + 50)))
        pygame.display.flip()
        clock.tick(30)
