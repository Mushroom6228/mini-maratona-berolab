import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game_speed, player):
        if len(self.obstacles) == 0:
            if random.randint(0, 1):
                self.obstacles.append(Cactus())
            else:
                self.obstacles.append(Bird())
        for obstacle in self.obstacles[:]:
            obstacle.update(game_speed, self.obstacles)
            # Colisão precisa
            if player.dino_rect.colliderect(obstacle.rect):
                if player.has_shield or player.has_hammer:
                    self.obstacles.remove(obstacle)
                else:
                    return True  # Colidiu sem proteção
        return False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset(self):
        self.obstacles = []
