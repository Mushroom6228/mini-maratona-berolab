# dino_runner/components/powerups/powerup.py
import pygame
import random
from dino_runner.utils.constants import SCREEN_WIDTH

class PowerUp:
    def __init__(self, image, type):
        # Garante que a imagem não seja None antes de tentar usar get_rect()
        if image:
            self.image = image
            self.rect = self.image.get_rect()
        else:
            print(f"Aviso: Imagem de power-up inválida ou vazia para tipo {type}. Usando placeholder.")
            self.image = pygame.Surface((30, 30)) # Placeholder
            self.image.fill((0, 255, 255)) # Cor ciano para fácil identificação
            self.rect = self.image.get_rect()

        self.type = type
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(200, 300) # Altura aleatória para power-ups

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
