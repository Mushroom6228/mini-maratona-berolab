# dino_runner/components/obstacles/obstacle.py
import pygame
from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle:
    def __init__(self, image, type):
        # Garante que a imagem seja uma lista e não esteja vazia
        if isinstance(image, list) and image:
            self.image = image
            self.rect = self.image[0].get_rect()
        elif not isinstance(image, list) and image is not None: # Se for uma única imagem (e não None)
            self.image = [image] # Converte para lista para consistência
            self.rect = image.get_rect()
        else: # Fallback para imagem vazia ou None
            print(f"Aviso: Imagem de obstáculo inválida ou vazia para tipo {type}. Usando placeholder.")
            self.image = [pygame.Surface((30, 30))] # Placeholder
            self.image[0].fill((255, 0, 255)) # Cor magenta para fácil identificação
            self.rect = self.image[0].get_rect()

        self.type = type
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles=None):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image[0], self.rect)
