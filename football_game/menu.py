import pygame
import math
import random


class Menu:
    def __init__(self, screen, font_big, font_mid):
        self.screen = screen
        self.options = ["PLAY", "STATS", "HOW TO PLAY"]
        self.selected = 0
        self.start_game    = False
        self.show_stats    = False
        self.show_tutorial = False
        self.tick = 0

        W, H = screen.get_size()

        self._particles = [
            {
                "x": random.uniform(0, W),
                "y": random.uniform(0, H),
                "r": random.uniform(1.5, 4.0),
                "alpha": random.randint(18, 55),
                "speed": random.uniform(0.15, 0.55),
                "drift": random.uniform(-0.2, 0.2),
            }
            for _ in range(35)
        ]

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if   self.selected == 0: self.start_game    = True
                elif self.selected == 1: self.show_stats    = True
                elif self.selected == 2: self.show_tutorial = True

    def draw(self):
        self.tick += 1
        W, H = self.screen.get_size()
        self._update_particles(W, H)
        self._draw_stripes(W, H)
        self._draw_pitch_lines(W, H)
        self._draw_vignette(W, H)
        self._draw_particles()
        self._draw_title(W, H)
        self._draw_buttons(W, H)
        self._draw_hint(W, H)

    def _update_particles(self, W, H):
        for p in self._particles:
            p["y"] -= p["speed"]
            p["x"] += p["drift"]
            if p["y"] < -p["r"]:
                p["y"] = H + p["r"]
                p["x"] = random.uniform(0, W)

    def _draw_stripes(self, W, H):
        sw = 70
        for i in range(W // sw + 1):
            c = (32, 108, 32) if i % 2 == 0 else (26, 90, 26)
            pygame.draw.rect(self.screen, c, (i * sw, 0, sw, H))

    def _draw_pitch_lines(self, W, H):
        lc = (200, 225, 200)
        lw = 2
        cx, cy = W // 2, H // 2

        def arc(ox, oy, r, a0, a1, steps=72):
            pts = []
            for i in range(steps + 1):
                a = math.radians(a0 + i * (a1 - a0) / steps)
                pts.append((int(ox + r * math.cos(a)), int(oy + r * math.sin(a))))
            if len(pts) >= 2:
                pygame.draw.lines(self.screen, lc, False, pts, lw)

        m = 5

        pygame.draw.rect(self.screen, lc, (m, m, W - m*2, H - m*2), lw)

        pygame.draw.line(self.screen, lc, (cx, m), (cx, H - m), lw)

        arc(cx, cy, 110, 0, 360)
        pygame.draw.circle(self.screen, lc, (cx, cy), 4)

        pa_d, pa_h = 145, 310
        pa_y = cy - pa_h // 2
        pygame.draw.rect(self.screen, lc, (m, pa_y, pa_d, pa_h), lw)
        pygame.draw.rect(self.screen, lc, (W - m - pa_d, pa_y, pa_d, pa_h), lw)

        ga_d, ga_h = 68, 145
        ga_y = cy - ga_h // 2
        pygame.draw.rect(self.screen, lc, (m, ga_y, ga_d, ga_h), lw)
        pygame.draw.rect(self.screen, lc, (W - m - ga_d, ga_y, ga_d, ga_h), lw)

        sd = 90
        pl_x = m + sd
        pr_x = W - m - sd
        pygame.draw.circle(self.screen, lc, (pl_x, cy), 4)
        pygame.draw.circle(self.screen, lc, (pr_x, cy), 4)

        arc_r = 85
        a_cut = math.degrees(math.acos(min(1.0, (pa_d - sd) / arc_r)))
        arc(pl_x, cy, arc_r, -a_cut,       a_cut)
        arc(pr_x, cy, arc_r, 180 - a_cut, 180 + a_cut)

        cr = 22
        arc(m,     m,     cr,   0,  90)
        arc(W - m, m,     cr,  90, 180)
        arc(m,     H - m, cr, -90,   0)
        arc(W - m, H - m, cr, 180, 270)
    
    def _draw_vignette(self, W, H):
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 112))
        self.screen.blit(ov, (0, 0))

        vig = pygame.Surface((W, H), pygame.SRCALPHA)
        for r in range(max(W, H), 0, -8):
            t = r / max(W, H)
            a = int(max(0, 60 * (1 - t * 1.4)))
            if a <= 0:
                continue
            pygame.draw.ellipse(
                vig, (0, 0, 0, a),
                (W//2 - r, H//2 - int(r * 0.7),
                 r * 2, int(r * 1.4)), 8,
            )
        self.screen.blit(vig, (0, 0))

    def _draw_particles(self):
        for p in self._particles:
            s = pygame.Surface((int(p["r"]*2), int(p["r"]*2)), pygame.SRCALPHA)
            pygame.draw.circle(
                s, (210, 240, 210, p["alpha"]),
                (int(p["r"]), int(p["r"])), int(p["r"]),
            )
            self.screen.blit(s, (int(p["x"] - p["r"]), int(p["y"] - p["r"])))

    def _draw_title(self, W, H):
        font_team = pygame.font.SysFont("Impact", 108)
        font_vs   = pygame.font.SysFont("Impact", 60)

        title_y  = 38
        ske_surf = font_team.render("SKE", True, (255, 210, 0))
        cpe_surf = font_team.render("CPE", True, (255, 255, 255))
        vs_r     = 52
        gap      = 30
        ske_x    = W // 2 - vs_r - gap - ske_surf.get_width()
        cpe_x    = W // 2 + vs_r + gap

        for ox, oy in [(-3, 4), (3, 4), (0, 5)]:
            self.screen.blit(font_team.render("SKE", True, (45, 30, 0)),
                             (ske_x + ox, title_y + oy))
        self.screen.blit(ske_surf, (ske_x, title_y))
        pygame.draw.rect(self.screen, (255, 210, 0),
                         (ske_x, title_y + ske_surf.get_height() + 4,
                          ske_surf.get_width(), 5), border_radius=3)

        for ox, oy in [(-3, 4), (3, 4), (0, 5)]:
            self.screen.blit(font_team.render("CPE", True, (20, 20, 20)),
                             (cpe_x + ox, title_y + oy))
        self.screen.blit(cpe_surf, (cpe_x, title_y))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (cpe_x, title_y + cpe_surf.get_height() + 4,
                          cpe_surf.get_width(), 5), border_radius=3)

        pulse  = 0.88 + 0.12 * math.sin(self.tick * 0.07)
        vs_rad = int(vs_r * pulse)
        cx     = W // 2
        cy     = title_y + ske_surf.get_height() // 2 + 8
        pygame.draw.circle(self.screen, (15, 50, 15), (cx, cy), vs_rad + 5)
        pygame.draw.circle(self.screen, (30, 140, 30), (cx, cy), vs_rad)
        pygame.draw.circle(self.screen, (80, 200, 80), (cx, cy), vs_rad, 3)
        vs_t = font_vs.render("VS", True, (255, 255, 255))
        self.screen.blit(vs_t, vs_t.get_rect(center=(cx, cy)))

    def _draw_buttons(self, W, H):
        font_btn = pygame.font.SysFont("Arial", 34, bold=True)
        btn_w, btn_h = 370, 58
        gap     = 14
        start_y = 262

        for i, label in enumerate(self.options):
            bx   = W // 2 - btn_w // 2
            by   = start_y + i * (btn_h + gap)
            rect = pygame.Rect(bx, by, btn_w, btn_h)

            if i == self.selected:
                ga = int(80 + 55 * math.sin(self.tick * 0.12))
                for gw in range(8, 0, -2):
                    gs = pygame.Surface((btn_w + gw*2, btn_h + gw*2), pygame.SRCALPHA)
                    pygame.draw.rect(gs, (255, 218, 0, ga // max(1, gw)),
                                     (0, 0, btn_w + gw*2, btn_h + gw*2),
                                     border_radius=10)
                    self.screen.blit(gs, (bx - gw, by - gw))
                pygame.draw.rect(self.screen, (255, 210, 0), rect, border_radius=8)
                txt_color = (10, 10, 10)
                ax, ay = bx - 38, by + btn_h // 2
                pygame.draw.polygon(self.screen, (255, 210, 0),
                                    [(ax, ay-12), (ax+22, ay), (ax, ay+12)])
            else:
                bg = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
                bg.fill((0, 0, 0, 130))
                self.screen.blit(bg, rect.topleft)
                pygame.draw.rect(self.screen, (80, 160, 80), rect, 2, border_radius=8)
                txt_color = (220, 240, 220)

            txt = font_btn.render(label, True, txt_color)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw_hint(self, W, H):
        font_hint = pygame.font.SysFont("Arial", 16)
        hint = font_hint.render("↑ ↓  select     ENTER  confirm",
                                True, (140, 190, 140))
        btn_h, gap = 58, 14
        self.screen.blit(hint, hint.get_rect(
            center=(W // 2, 262 + 3*(btn_h+gap) + 18)))


def draw_tutorial(screen, tick=0):
    W, H = screen.get_size()
    sw = 80
    for i in range(W // sw + 1):
        c = (32, 108, 32) if i % 2 == 0 else (26, 90, 26)
        pygame.draw.rect(screen, c, (i * sw, 0, sw, H))

    lc = (200, 225, 200)
    cx, cy = W // 2, H // 2
    pygame.draw.line(screen, lc, (cx, 0), (cx, H), 2)
    pygame.draw.circle(screen, lc, (cx, cy), 110, 2)

    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 130))
    screen.blit(ov, (0, 0))

    font_h1   = pygame.font.SysFont("Impact",   62)
    font_sec  = pygame.font.SysFont("Arial",    26, bold=True)
    font_body = pygame.font.SysFont("Consolas", 22)
    font_hint = pygame.font.SysFont("Arial",    18)

    tbar = pygame.Surface((W, 72), pygame.SRCALPHA)
    tbar.fill((0, 0, 0, 160))
    screen.blit(tbar, (0, 0))
    title = font_h1.render("HOW TO PLAY", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(W // 2, 36)))
    pygame.draw.rect(screen, (255, 210, 0), (W//2 - 200, 68, 400, 4), border_radius=2)

    card_w, card_h = 520, 310
    gap    = 40
    card_y = 95
    cx1    = (W - (card_w * 2 + gap)) // 2
    cx2    = cx1 + card_w + gap

    def draw_card(cx, cy, cw, ch, hdr_color, hdr_text, rows):
        cs = pygame.Surface((cw, ch), pygame.SRCALPHA)
        cs.fill((10, 50, 10, 210))
        screen.blit(cs, (cx, cy))
        pygame.draw.rect(screen, (80, 160, 80), (cx, cy, cw, ch), 2, border_radius=12)
        pygame.draw.rect(screen, hdr_color, (cx, cy, cw, 48), border_radius=12)
        pygame.draw.rect(screen, hdr_color, (cx, cy+24, cw, 24))
        pygame.draw.rect(screen, (80, 160, 80), (cx, cy, cw, 48), 2, border_radius=12)
        ht = font_sec.render(hdr_text, True, (255, 255, 255))
        screen.blit(ht, ht.get_rect(center=(cx + cw//2, cy + 24)))
        pygame.draw.line(screen, (80, 160, 80), (cx+16, cy+52), (cx+cw-16, cy+52), 1)
        for idx, (key, desc, note) in enumerate(rows):
            ry = cy + 68 + idx * 56
            ks = font_body.render(key, True, (255, 255, 255))
            kw = max(ks.get_width() + 20, 90)
            kh = 32
            kb = pygame.Surface((kw, kh), pygame.SRCALPHA)
            kb.fill((0, 0, 0, 190))
            screen.blit(kb, (cx+18, ry))
            pygame.draw.rect(screen, (160, 200, 160), (cx+18, ry, kw, kh), 1, border_radius=5)
            screen.blit(ks, ks.get_rect(center=(cx+18+kw//2, ry+kh//2)))
            screen.blit(font_sec.render(desc, True, (230, 240, 230)), (cx+18+kw+18, ry+4))
            if note:
                screen.blit(font_hint.render(note, True, (140, 200, 140)),
                            (cx+18+kw+18, ry+30))

    draw_card(cx1, card_y, card_w, card_h, (160, 110, 0), "Player 1  (SKE)", [
        ("A  /  D", "Move left / right", "Hold to run"),
        ("W",       "Jump",               "Press while on ground"),
        ("E",       "Kick the ball",      "Aim with movement direction"),
    ])
    draw_card(cx2, card_y, card_w, card_h, (20, 80, 20), "Player 2  (CPE)", [
        ("Left / Right", "Move left / right", "Hold to run"),
        ("Up",           "Jump",               "Press while on ground"),
        ("SPACE",        "Kick the ball",      "Aim with movement direction"),
    ])

    tips_y = card_y + card_h + 24
    tips = [
        ("GOAL",    "Score by kicking the ball into the opponent's net"),
        ("TIMER",   "60-second match — most goals wins"),
        ("PHYSICS", "Ball bounces realistically — angle your kicks!"),
    ]
    tip_w = (W - 120) // 3
    for i, (label, text) in enumerate(tips):
        tx = 60 + i * (tip_w + 20)
        ts = pygame.Surface((tip_w, 68), pygame.SRCALPHA)
        ts.fill((10, 50, 10, 170))
        screen.blit(ts, (tx, tips_y))
        pygame.draw.rect(screen, (80, 160, 80), (tx, tips_y, tip_w, 68), 1, border_radius=8)
        lt = font_hint.render(label, True, (255, 210, 0))
        screen.blit(lt, lt.get_rect(center=(tx + tip_w//2, tips_y + 16)))
        pygame.draw.line(screen, (80, 160, 80),
                         (tx+16, tips_y+28), (tx+tip_w-16, tips_y+28), 1)
        bt = font_hint.render(text, True, (200, 230, 200))
        screen.blit(bt, bt.get_rect(center=(tx + tip_w//2, tips_y + 48)))

    esc = font_hint.render("Press  ESC  to return to menu", True, (160, 200, 160))
    screen.blit(esc, esc.get_rect(center=(W//2, tips_y + 90)))
    pygame.draw.rect(screen, (80, 160, 80),
                     esc.get_rect(center=(W//2, tips_y+90)).inflate(20, 10),
                     1, border_radius=6)