import pygame

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BG     = (20,  20,  20)
GOLD   = (220, 180,  50)
GREEN  = (60,  180,  60)
GRAY   = (100, 100, 100)


def _load_head(path, size=120):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except Exception:
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 200, 200), (size // 2, size // 2), size // 2)
        return surf


def run_skin_select(screen, clock):
    from football_game.player_skin import SKINS

    W, H = screen.get_size()

    font_title = pygame.font.SysFont("Avenir Next Condensed", 44, bold=True)
    font_name  = pygame.font.SysFont("Avenir Next Condensed", 28, bold=True)
    font_label = pygame.font.SysFont("Avenir Next Condensed", 22, bold=True)
    font_hint  = pygame.font.SysFont("Avenir Next Condensed", 20)

    head_imgs = [_load_head(s["head"]) for s in SKINS]

    sel   = [2, 1]
    ready = [False, False]

    PLAYERS = [
        {
            "label":   "PLAYER 1",
            "color":   (255, 210,  50),
            "left":    pygame.K_a,
            "right":   pygame.K_d,
            "confirm": pygame.K_e,
        },
        {
            "label":   "PLAYER 2",
            "color":   (80,  170, 255),
            "left":    pygame.K_LEFT,
            "right":   pygame.K_RIGHT,
            "confirm": pygame.K_SPACE,
        },
    ]

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                for i, p in enumerate(PLAYERS):
                    if not ready[i]:
                        if event.key == p["left"]:
                            sel[i] = (sel[i] - 1) % len(SKINS)
                        if event.key == p["right"]:
                            sel[i] = (sel[i] + 1) % len(SKINS)
                        if event.key == p["confirm"]:
                            ready[i] = True
                    else:
                        if event.key == p["confirm"]:
                            ready[i] = False

        if all(ready):
            print(f"[skin_select] returning P1={sel[0]} ({SKINS[sel[0]]['name']})  P2={sel[1]} ({SKINS[sel[1]]['name']})")
            return sel[0], sel[1]

        screen.fill(BG)

        stripe_w = 80
        for i in range(W // stripe_w + 1):
            c = (28, 28, 28) if i % 2 == 0 else (22, 22, 22)
            pygame.draw.rect(screen, c, (i * stripe_w, 0, stripe_w, H))

        title = font_title.render("SELECT YOUR SKIN", True, WHITE)
        screen.blit(title, title.get_rect(center=(W // 2, 46)))
        pygame.draw.rect(screen, GOLD, (W // 2 - 160, 72, 320, 4), border_radius=2)

        divider = pygame.Surface((2, H - 120), pygame.SRCALPHA)
        divider.fill((60, 60, 60, 200))
        screen.blit(divider, (W // 2 - 1, 90))

        for i, p in enumerate(PLAYERS):
            cx = W // 4 + i * (W // 2)

            plbl = font_label.render(p["label"], True, p["color"])
            screen.blit(plbl, plbl.get_rect(center=(cx, 104)))

            skin     = SKINS[sel[i]]
            head_img = head_imgs[sel[i]]
            if i == 1:
                head_img = pygame.transform.flip(head_img, True, False)
            head_x   = cx - head_img.get_width() // 2
            head_y   = 150

            if ready[i]:
                glow = pygame.Surface((head_img.get_width() + 16, head_img.get_height() + 16), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*GREEN, 90), glow.get_rect(), border_radius=12)
                screen.blit(glow, (head_x - 8, head_y - 8))
                pygame.draw.rect(screen, GREEN, (head_x - 8, head_y - 8, head_img.get_width() + 16, head_img.get_height() + 16), 3, border_radius=12)

            screen.blit(head_img, (head_x, head_y))

            color_block = pygame.Rect(cx - 28, head_y + head_img.get_height() + 12, 56, 24)
            pygame.draw.rect(screen, skin["color"], color_block, border_radius=6)
            pygame.draw.rect(screen, (180, 180, 180), color_block, 1, border_radius=6)

            name_surf = font_name.render(skin["name"], True, WHITE)
            screen.blit(name_surf, name_surf.get_rect(center=(cx, head_y + head_img.get_height() + 52)))

            dot_y   = head_y + head_img.get_height() + 82
            total_w = len(SKINS) * 26
            start_x = cx - total_w // 2 + 13
            for j in range(len(SKINS)):
                is_cur = (j == sel[i])
                r      = 8 if is_cur else 5
                col    = SKINS[j]["color"] if is_cur else GRAY
                pygame.draw.circle(screen, col, (start_x + j * 26, dot_y), r)
                if is_cur:
                    pygame.draw.circle(screen, WHITE, (start_x + j * 26, dot_y), r, 2)

            key_l = pygame.key.name(p["left"]).upper()
            key_r = pygame.key.name(p["right"]).upper()
            key_c = pygame.key.name(p["confirm"]).upper()

            if not ready[i]:
                hint_str  = f"[{key_l}] < SELECT > [{key_r}]   CONFIRM: [{key_c}]"
                hint_color = (160, 160, 160)
            else:
                hint_str  = f"READY!   Press [{key_c}] again to change"
                hint_color = GREEN

            hint = font_hint.render(hint_str, True, hint_color)
            screen.blit(hint, hint.get_rect(center=(cx, dot_y + 28)))

        if not all(ready):
            waiting_text = "Waiting for both players to confirm..."
            w_color      = (180, 180, 180)
        else:
            waiting_text = "Starting game!"
            w_color      = GREEN

        w_surf = font_label.render(waiting_text, True, w_color)
        screen.blit(w_surf, w_surf.get_rect(center=(W // 2, H - 36)))

        pygame.display.flip()