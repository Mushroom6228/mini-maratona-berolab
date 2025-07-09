import pygame
from dino_runner.utils.constants import HEART

class HUD:
    def __init__(self, get_lives):
        self.get_lives = get_lives  # Função para pegar vidas atuais

    def draw(self, screen):
        # Exibe vidas reais
        for i in range(self.get_lives()):
            screen.blit(HEART, (20 + 40 * i, 20))
