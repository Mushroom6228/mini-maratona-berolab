import pygame
from dino_runner.utils.text_utils import draw_message_component
import os
from dino_runner.utils.constants import IMG_DIR

class Score:
    def __init__(self):
        self.points = 0
        self._accum = 0.0
        self.font_color = (0, 0, 0)
        self.font_size = 22
        self.flash = False
        self.flash_timer = 0
        # Carrega som de checkpoint se existir
        self.checkpoint_sound = None
        self.point_sound = None
        score_path = os.path.join(IMG_DIR, 'Other', 'score.wav')
        point_path = os.path.join(IMG_DIR, 'Other', 'point.wav')
        if os.path.exists(score_path):
            self.checkpoint_sound = pygame.mixer.Sound(score_path)
        if os.path.exists(point_path):
            self.point_sound = pygame.mixer.Sound(point_path)

    def update(self, is_night=False):
        # 100 pontos em 10 segundos = 10 pontos por segundo
        # Com FPS = 60, a cada frame: 10/60 = 0.1666...
        self._accum += 0.1666  # Aproximadamente 10 pontos por segundo em 60 FPS
        if self._accum >= 1:
            self.points += int(self._accum)
            self._accum -= int(self._accum)
        # Pisca e toca som a cada 100 pontos
        if self.points > 0 and self.points % 100 == 0:
            if not self.flash:
                self.flash = True
                self.flash_timer = pygame.time.get_ticks()
                if self.point_sound:
                    self.point_sound.play()
        if self.flash and pygame.time.get_ticks() - self.flash_timer > 300:
            self.flash = False

    def draw(self, screen, is_night=False):
        # Pisca invertendo as cores, e inverte cor de acordo com o ciclo
        if is_night:
            base_color = (255,255,255)
            flash_color = (0,0,0)
        else:
            base_color = (0,0,0)
            flash_color = (255,255,255)
        color = flash_color if self.flash else base_color
        from dino_runner.utils.text_utils import FONT_STYLE
        font = pygame.font.Font(FONT_STYLE, 20)
        text = font.render(f"Score: {self.points}", True, color)
        text_rect = text.get_rect()
        text_rect.topright = (1020, 60)
        screen.blit(text, text_rect)

    def reset(self):
        self.points = 0
        self._accum = 0.0
        self.flash = False
        self.flash_timer = 0
