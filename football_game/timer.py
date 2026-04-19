import pygame

class Timer:
    def __init__(self, duration, font):
        self.duration = duration
        self.font = font
        self.start_ticks = 0
        self.time_left = duration

    def start_timer(self):
        self.start_ticks = pygame.time.get_ticks()

    def update_timer(self):
        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.time_left = max(0, self.duration - elapsed)

    def is_time_up(self):
        return self.time_left <= 0

    def draw_timer(self, screen):
        timer_text = self.font.render(f"{self.time_left}", True, (255,255,255))
        rect = timer_text.get_rect(center=(640, 100))
        screen.blit(timer_text, rect)