import pygame

class Menu:
    def __init__(self, screen, font_big, font_mid):
        self.screen = screen
        self.font_big = font_big
        self.font_mid = font_mid

        self.options = ["Play", "Stats"]
        self.selected = 0

        self.start_game = False
        self.show_stats = False

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

    def draw(self):
        self.screen.fill((0, 0, 0))

        title = self.font_big.render("SKE vs CPE", True, (255,255,255))
        self.screen.blit(title, (450, 150))

        for i, option in enumerate(self.options):
            color = (255,255,0) if i == self.selected else (200,200,200)
            text = self.font_mid.render(option, True, color)

            rect = text.get_rect(center=(640, 350 + i*80))
            self.screen.blit(text, rect)