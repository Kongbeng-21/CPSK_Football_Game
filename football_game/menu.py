import pygame
import math

class Menu:
    def __init__(self, screen, font_big, font_mid):
        self.screen = screen
        self.options = ["Play", "Stats"]
        self.selected = 0
        self.start_game = False
        self.show_stats = False
        self.tick = 0

        self.font_title_big = pygame.font.SysFont("Avenir Next Condensed", 104, bold=True)
        self.font_vs        = pygame.font.SysFont("Avenir Next Condensed", 58, bold=True)
        self.font_sub       = pygame.font.SysFont("Arial",  24, bold=True)
        self.font_option    = pygame.font.SysFont("Arial",  36, bold=True)
        self.font_howto     = pygame.font.SysFont("Arial",  24, bold=True)
        self.font_label     = pygame.font.SysFont("Arial",  26, bold=True)
        self.font_ctrl      = pygame.font.SysFont("Consolas", 23)
        self.font_key       = pygame.font.SysFont("Consolas", 21, bold=True)
        self.font_hint      = pygame.font.SysFont("Arial",  19)


    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.start_game = True
                elif self.selected == 1:
                    self.show_stats = True

    # ─────────────────────────────── MAIN MENU ───────────────────────────────

    def draw(self):
        self.tick += 1
        W, H = self.screen.get_size()
        self._draw_field(W, H)
        self._draw_title(W)
        self._draw_menu(W)
        self._draw_controls_panel(W)
        self._draw_hints(W)

    def _draw_field(self, W, H):
        stripe_w = 80
        for i in range(W // stripe_w + 1):
            c = (34, 110, 34) if i % 2 == 0 else (28, 95, 28)
            pygame.draw.rect(self.screen, c, (i * stripe_w, 0, stripe_w, H))

        line_color = (210, 230, 210)

        pygame.draw.line(self.screen, line_color, (W // 2, 0), (W // 2, H), 2)
        pygame.draw.circle(self.screen, line_color, (W // 2, H // 2), 105, 2)

        penalty_w = 145
        penalty_h = 310
        penalty_y = H // 2 - penalty_h // 2

        pygame.draw.rect(self.screen, line_color, (0, penalty_y, penalty_w, penalty_h), 2)
        pygame.draw.rect(self.screen, line_color, (W - penalty_w, penalty_y, penalty_w, penalty_h), 2)

        goal_area_w = 68
        goal_area_h = 145
        goal_area_y = H // 2 - goal_area_h // 2

        pygame.draw.rect(self.screen, line_color, (0, goal_area_y, goal_area_w, goal_area_h), 2)
        pygame.draw.rect(self.screen, line_color, (W - goal_area_w, goal_area_y, goal_area_w, goal_area_h), 2)

        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 115))
        self.screen.blit(ov, (0, 0))



    def _draw_title(self, W):
        left_text = "CPE"
        right_text = "SKE"

        title_y = 38
        left_x = W // 2 - 300
        right_x = W // 2 + 95

        def draw_outlined_text(text, x, y, color):
            base = self.font_title_big.render(text, True, color)
            shadow = self.font_title_big.render(text, True, (0, 0, 0))

            for ox, oy in [(-3,0), (3,0), (0,-3), (0,3), (-3,-3), (3,-3), (-3,3), (3,3)]:
                self.screen.blit(shadow, (x + ox, y + oy))

            self.screen.blit(base, (x, y))
            return base

        left_surf = draw_outlined_text(left_text, left_x, title_y, (255, 255, 255))
        right_surf = draw_outlined_text(right_text, right_x, title_y, (255, 255, 255))

        bar_h = 7
        bar_y = title_y + left_surf.get_height() + 8

        pygame.draw.rect(self.screen, (255, 210, 0), (left_x, bar_y, left_surf.get_width(), bar_h), border_radius=3)
        pygame.draw.rect(self.screen, (255, 210, 0), (right_x, bar_y, right_surf.get_width(), bar_h), border_radius=3)

        pulse = int(215 + 35 * math.sin(self.tick * 0.05))
        vs_surf = self.font_vs.render("VS", True, (255, pulse, 0))
        vs_rect = vs_surf.get_rect(center=(W // 2, title_y + left_surf.get_height() // 2 + 5))

        pygame.draw.circle(self.screen, (20, 25, 20), vs_rect.center, 48)
        pygame.draw.circle(self.screen, (255, 210, 0), vs_rect.center, 48, 3)
        self.screen.blit(vs_surf, vs_rect)

        derby = self.font_sub.render("CPSK DERBY  -  2D FOOTBALL BATTLE", True, (180, 255, 180))
        derby_rect = derby.get_rect(center=(W // 2, bar_y + 38))
        self.screen.blit(derby, derby_rect)

        

    def _draw_menu(self, W):
        labels = ["PLAY", "STATS"]
        btn_w, btn_h = 340, 52
        gap = 12
        start_y = 265

        for i, label in enumerate(labels):
            bx = W//2 - btn_w//2
            by = start_y + i * (btn_h + gap)
            rect = pygame.Rect(bx, by, btn_w, btn_h)

            if i == self.selected:
                for gw in range(5, 0, -1):
                    gr = pygame.Rect(bx-gw, by-gw, btn_w+gw*2, btn_h+gw*2)
                    gs = pygame.Surface((gr.width, gr.height), pygame.SRCALPHA)
                    gs.fill((255,220,0, 20))
                    self.screen.blit(gs, gr.topleft)
                pygame.draw.rect(self.screen, (255,220,0), rect, border_radius=8)
                txt = self.font_option.render(label, True, (15,15,15))
                ax, ay = bx - 30, by + btn_h//2
                pygame.draw.polygon(self.screen, (255,220,0),
                                    [(ax,ay-10),(ax+18,ay),(ax,ay+10)])
            else:
                bs = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
                bs.fill((0,0,0,130))
                self.screen.blit(bs, rect.topleft)
                pygame.draw.rect(self.screen, (160,160,160), rect, width=2, border_radius=8)
                txt = self.font_option.render(label, True, (200,200,200))

            tr = txt.get_rect(center=rect.center)
            self.screen.blit(txt, tr)

    def _draw_controls_panel(self, W):
        pw, ph = 600, 200
        px = (W - pw)//2
        py = 405

        panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
        panel.fill((10,50,10, 205))
        self.screen.blit(panel, (px, py))
        pygame.draw.rect(self.screen, (80,160,80), (px,py,pw,ph), width=2, border_radius=10)

        hbar = pygame.Surface((pw, 38), pygame.SRCALPHA)
        hbar.fill((0,0,0,160))
        self.screen.blit(hbar, (px, py))
        hw = self.font_howto.render("HOW  TO  PLAY", True, (255,255,255))
        self.screen.blit(hw, hw.get_rect(center=(px+pw//2, py+19)))

        pygame.draw.line(self.screen, (80,160,80), (px+20,py+42), (px+pw-20,py+42), 1)
        mid = px + pw//2
        pygame.draw.line(self.screen, (80,160,80), (mid,py+50), (mid,py+ph-14), 1)

        self.screen.blit(self.font_label.render("Player 1  (SKE)", True, (255,220,0)), (px+28, py+52))
        for j,(k,a) in enumerate([("A  D","Move"),("W","Jump"),("E","Kick")]):
            y = py+86+j*36
            self._draw_key(k, px+28, y)
            self.screen.blit(self.font_ctrl.render("--", True, (100,160,100)), (px+114, y+2))
            self.screen.blit(self.font_ctrl.render(a,   True, (220,220,220)),  (px+150, y+2))

        self.screen.blit(self.font_label.render("Player 2  (CPE)", True, (85,170,255)), (mid+20, py+52))
        for j,(k,a) in enumerate([("< >","Move"),("UP","Jump"),("SPC","Kick")]):
            y = py+86+j*36
            self._draw_key(k, mid+20, y)
            self.screen.blit(self.font_ctrl.render("--", True, (100,160,100)), (mid+114, y+2))
            self.screen.blit(self.font_ctrl.render(a,   True, (220,220,220)),  (mid+150, y+2))

    def _draw_key(self, text, x, y):
        surf = self.font_key.render(text, True, (255,255,255))
        w = max(surf.get_width()+16, 74)
        h = 26
        box = pygame.Surface((w, h), pygame.SRCALPHA)
        box.fill((0,0,0,190))
        self.screen.blit(box, (x, y))
        pygame.draw.rect(self.screen, (160,200,160), (x,y,w,h), width=1, border_radius=4)
        self.screen.blit(surf, surf.get_rect(center=(x+w//2, y+h//2)))

    def _draw_hints(self, W):
        pass

# ─────────────────────────── TUTORIAL SCREEN ────────────────────────────────

def draw_tutorial(screen, tick=0):
    """Call this from game.py instead of the old plain-text tutorial."""
    W, H = screen.get_size()

    # ── Field background (same as menu) ──────────────────────────────────────
    stripe_w = 80
    for i in range(W // stripe_w + 1):
        c = (34,110,34) if i % 2 == 0 else (28,95,28)
        pygame.draw.rect(screen, c, (i*stripe_w, 0, stripe_w, H))
    pygame.draw.circle(screen, (255,255,255), (W//2, H//2), 100, 2)
    pygame.draw.line(screen, (255,255,255), (W//2,0), (W//2,H), 2)
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0,0,0,140))
    screen.blit(ov, (0,0))

    font_h1   = pygame.font.SysFont("Impact", 64, bold=True)
    font_sec  = pygame.font.SysFont("Arial", 26, bold=True)
    font_body = pygame.font.SysFont("Consolas", 22)
    font_hint = pygame.font.SysFont("Arial", 18)

    # ── Title bar ─────────────────────────────────────────────────────────────
    tbar = pygame.Surface((W, 72), pygame.SRCALPHA)
    tbar.fill((0,0,0,160))
    screen.blit(tbar, (0,0))

    title = font_h1.render("HOW TO PLAY", True, (255,255,255))
    screen.blit(title, title.get_rect(center=(W//2, 36)))
    pygame.draw.rect(screen, (255,210,0), (W//2-200, 68, 400, 4), border_radius=2)

    # ── Two-column card layout ────────────────────────────────────────────────
    card_w, card_h = 520, 310
    gap = 40
    total_w = card_w*2 + gap
    card_y = 95
    card_x1 = (W - total_w)//2
    card_x2 = card_x1 + card_w + gap

    def draw_card(cx, cy, cw, ch, header_color, header_text, rows):
        # Card bg
        cs = pygame.Surface((cw, ch), pygame.SRCALPHA)
        cs.fill((10,50,10,200))
        screen.blit(cs, (cx, cy))
        pygame.draw.rect(screen, (80,160,80), (cx,cy,cw,ch), width=2, border_radius=12)

        # Header stripe
        hs = pygame.Surface((cw, 48), pygame.SRCALPHA)
        hs.fill((0,0,0,170))
        screen.blit(hs, (cx, cy))
        pygame.draw.rect(screen, header_color, (cx,cy,cw,48), width=0, border_radius=12)
        # re-draw bottom corners flat
        pygame.draw.rect(screen, header_color, (cx, cy+24, cw, 24))
        # border on top only
        pygame.draw.rect(screen, (80,160,80), (cx,cy,cw,48), width=2, border_radius=12)

        ht = font_sec.render(header_text, True, (255,255,255))
        screen.blit(ht, ht.get_rect(center=(cx+cw//2, cy+24)))

        pygame.draw.line(screen, (80,160,80), (cx+16,cy+52), (cx+cw-16,cy+52), 1)

        for idx,(key,desc,note) in enumerate(rows):
            ry = cy + 68 + idx*56

            # Key badge
            ks = font_body.render(key, True, (255,255,255))
            kw = max(ks.get_width()+20, 90)
            kh = 32
            kbox = pygame.Surface((kw,kh), pygame.SRCALPHA)
            kbox.fill((0,0,0,200))
            screen.blit(kbox, (cx+18, ry))
            pygame.draw.rect(screen, (180,220,180), (cx+18,ry,kw,kh), width=1, border_radius=5)
            screen.blit(ks, ks.get_rect(center=(cx+18+kw//2, ry+kh//2)))

            # Action
            at = font_sec.render(desc, True, (230,230,230))
            screen.blit(at, (cx+18+kw+18, ry+4))

            # Note (smaller, muted)
            if note:
                nt = font_hint.render(note, True, (140,200,140))
                screen.blit(nt, (cx+18+kw+18, ry+30))

    draw_card(
        card_x1, card_y, card_w, card_h,
        (180, 120, 0),
        "Player 1  (SKE)",
        [
            ("A  /  D",  "Move left / right", "Hold to run"),
            ("W",        "Jump",               "Press while on ground"),
            ("E",        "Kick the ball",      "Aim with movement direction"),
        ]
    )

    draw_card(
        card_x2, card_y, card_w, card_h,
        (20, 60, 140),
        "Player 2  (CPE)",
        [
            ("Left / Right", "Move left / right", "Hold to run"),
            ("Up",           "Jump",               "Press while on ground"),
            ("SPACE",        "Kick the ball",      "Aim with movement direction"),
        ]
    )

    # ── Tips row ──────────────────────────────────────────────────────────────
    tips_y = card_y + card_h + 24
    tips = [
        ("GOAL",    "Score by kicking the ball into the opponent's net"),
        ("TIMER",   "60-second match — most goals wins"),
        ("PHYSICS", "Ball bounces realistically — angle your kicks!"),
    ]
    tip_w = (W - 120) // len(tips)
    for i,(label,text) in enumerate(tips):
        tx = 60 + i*(tip_w+20)
        ts = pygame.Surface((tip_w, 68), pygame.SRCALPHA)
        ts.fill((0,0,0,160))
        screen.blit(ts, (tx, tips_y))
        pygame.draw.rect(screen, (60,140,60), (tx,tips_y,tip_w,68), width=1, border_radius=8)

        lt = font_hint.render(label, True, (255,210,0))
        screen.blit(lt, lt.get_rect(center=(tx+tip_w//2, tips_y+16)))
        pygame.draw.line(screen, (60,140,60), (tx+16,tips_y+28), (tx+tip_w-16,tips_y+28), 1)
        bt = font_hint.render(text, True, (200,230,200))
        screen.blit(bt, bt.get_rect(center=(tx+tip_w//2, tips_y+48)))

    # ── Footer ────────────────────────────────────────────────────────────────
    foot_y = tips_y + 80
    esc_s = font_hint.render("Press  ESC  to return to menu", True, (180,180,180))
    screen.blit(esc_s, esc_s.get_rect(center=(W//2, foot_y)))
    pygame.draw.rect(screen, (100,100,100), esc_s.get_rect(center=(W//2,foot_y)).inflate(20,10),
                     width=1, border_radius=6)