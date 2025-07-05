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
                    # Toca o som de quebrar se disponível (corrigido para garantir que só toca se colidir COM powerup)
                    if hasattr(player, 'game') and hasattr(player.game, 'powerup_manager') and hasattr(player.game.powerup_manager, 'break_sound'):
                        if player.game.powerup_manager.break_sound:
                            player.game.powerup_manager.break_sound.play()
                    self.obstacles.remove(obstacle)
                    return False  # Garante que não perde vida ao quebrar com powerup
                else:
                    return True  # Colidiu sem proteção
        return False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset(self):
        self.obstacles = []
