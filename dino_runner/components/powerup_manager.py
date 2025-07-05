import random
import pygame
from dino_runner.components.powerups.shield import Shield
from dino_runner.components.powerups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.last_powerup_time = 0
        self.powerup_cooldown = 30000  # 30 segundos

    def update(self, game_speed, player):
        now = pygame.time.get_ticks()
        # Só aparece se não houver obstáculos próximos
        can_spawn = True
        for obs in getattr(player, 'game', []).obstacle_manager.obstacles if hasattr(player, 'game') else []:
            if abs(obs.rect.x - player.dino_rect.x) < 400:
                can_spawn = False
                break
        if len(self.power_ups) == 0 and now - self.last_powerup_time > self.powerup_cooldown and can_spawn:
            if random.randint(0, 1):
                powerup = Shield()
            else:
                powerup = Hammer()
            powerup.rect.x = player.dino_rect.x + 900  # Spawn mais longe
            self.power_ups.append(powerup)
            self.last_powerup_time = now
        for power_up in self.power_ups:
            power_up.update(game_speed, player)
            if player.dino_rect.colliderect(power_up.rect):
                if power_up.type == "shield":
                    player.has_shield = True
                    player.shield_time_up = pygame.time.get_ticks() + 8000  # 8 segundos
                elif power_up.type == "hammer":
                    player.has_hammer = True
                    player.hammer_time_up = pygame.time.get_ticks() + 8000  # 8 segundos
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset(self):
        self.power_ups = []
        # Reinicia o timer para o momento atual
        self.last_powerup_time = pygame.time.get_ticks()
