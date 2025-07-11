# dino_runner/components/obstacles/bird.py
import pygame
import random
from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle # Importa a classe base Obstacle

# Classe Pássaro
class Bird(Obstacle):
    def __init__(self):
        # Garante que BIRD não esteja vazio
        bird_images = BIRD if BIRD else [pygame.Surface((30, 30), flags=pygame.SRCALPHA)] # Fallback
        if not bird_images[0]: # Se o placeholder for vazio, preenche
            bird_images[0].fill((255, 0, 255))

        super().__init__(bird_images, 1)
        self.rect.y = random.choice([250, 280, 310]) # Diferentes alturas para os pássaros
        self.index = 0
        # CORREÇÃO: Inicializa image_to_draw no __init__
        self.image_to_draw = self.image[self.index // 5] if self.image else bird_images[0]


    def update(self, game_speed, obstacles=None):
        super().update(game_speed)
        # Anima as asas do pássaro
        if self.image and self.index >= (len(self.image) * 5) -1: # Ajusta para o tamanho real da lista de imagens
            self.index = 0
        
        # Garante que self.image não esteja vazio antes de tentar acessar
        if self.image:
            self.image_to_draw = self.image[self.index // 5]
        else:
            self.image_to_draw = pygame.Surface((30, 30)) # Placeholder
            self.image_to_draw.fill((255, 0, 255))

        self.index += 1

    def draw(self, screen):
        screen.blit(self.image_to_draw, self.rect) # Usa image_to_draw
