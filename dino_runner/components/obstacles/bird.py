from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD
import random


class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.images = BIRD  # Garante que é uma lista
        # Altura aleatória entre 200 e 320 (variação real)
        self.rect.y = random.randint(200, 320)
        self.step_index = 0

    def draw(self, screen):
        screen.blit(self.images[self.step_index // 5], self.rect)
        self.step_index += 1

        if self.step_index >= 10:
            self.step_index = 0