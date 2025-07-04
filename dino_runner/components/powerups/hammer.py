import pygame
from dino_runner.utils.constants import HAMMER
from dino_runner.components.powerups.power_up import PowerUp

class Hammer(PowerUp):
    def __init__(self):
        self.image = HAMMER
        self.type = "hammer"
        super().__init__(self.image, self.type)
        self.duration = 5  # segundos

    def update(self, game_speed, player):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            if hasattr(player, 'has_hammer'):
                player.has_hammer = False
        # Não fecha o jogo se pegar o martelo

    def draw(self, screen):
        screen.blit(self.image, self.rect)
