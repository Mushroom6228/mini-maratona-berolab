import pygame
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH
import random

class Cloud:
    def __init__(self):
        self.clouds = []
        last_x = SCREEN_WIDTH
        for _ in range(10):  # Bem mais nuvens
            cloud = self.create_cloud(last_x)
            self.clouds.append(cloud)
            last_x = cloud['x'] + cloud['width'] + random.randint(120, 300)

    def create_cloud(self, min_x=None):
        # min_x: posição mínima para garantir espaçamento
        if min_x is None:
            min_x = SCREEN_WIDTH
        x = min_x + random.randint(120, 300)
        y = random.randint(50, 200)
        return {'x': x, 'y': y, 'image': CLOUD, 'width': CLOUD.get_width()}

    def update(self, game_speed):
        for i, cloud in enumerate(self.clouds):
            cloud['x'] -= game_speed // 2
            if cloud['x'] < -cloud['width']:
                # Reposiciona a nuvem após a última nuvem da lista, garantindo distância
                last_cloud = max(self.clouds, key=lambda c: c['x'])
                new_cloud = self.create_cloud(last_cloud['x'] + last_cloud['width'])
                self.clouds[i] = new_cloud

    def draw(self, screen):
        for cloud in self.clouds:
            screen.blit(cloud['image'], (cloud['x'], cloud['y']))
