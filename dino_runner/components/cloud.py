import pygame
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH
import random

class Cloud:
    def __init__(self):
        self.clouds = []
        for _ in range(4):  # Mais nuvens
            self.clouds.append(self.create_cloud())

    def create_cloud(self):
        x = SCREEN_WIDTH + random.randint(0, 2000)
        y = random.randint(50, 200)
        return {'x': x, 'y': y, 'image': CLOUD, 'width': CLOUD.get_width()}

    def update(self, game_speed):
        for cloud in self.clouds:
            cloud['x'] -= game_speed // 2
            if cloud['x'] < -cloud['width']:
                cloud.update(self.create_cloud())

    def draw(self, screen):
        for cloud in self.clouds:
            screen.blit(cloud['image'], (cloud['x'], cloud['y']))
