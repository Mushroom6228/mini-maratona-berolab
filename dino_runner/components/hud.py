import pygame
from dino_runner.utils.constants import HEART

class HUD:
    def __init__(self, player, get_lives):
        self.player = player
        self.get_lives = get_lives  # Função para pegar vidas atuais

    def draw(self, screen):
        # Exibe vidas reais
        for i in range(self.get_lives()):
            screen.blit(HEART, (20 + 40 * i, 20))
