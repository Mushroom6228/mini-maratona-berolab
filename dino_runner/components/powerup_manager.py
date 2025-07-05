import random
import pygame
import os
from dino_runner.components.powerups.shield import Shield
from dino_runner.components.powerups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.last_powerup_time = 0
        self.powerup_cooldown = 20000  # 20 segundos
        self.powerup_sound = None
        self.break_sound = None
        powerup_path = os.path.join('dino_runner', 'assets', 'Other', 'powerup.wav')
        break_path = os.path.join('dino_runner', 'assets', 'Other', 'break.wav')
        if os.path.exists(powerup_path):
            self.powerup_sound = pygame.mixer.Sound(powerup_path)
        if os.path.exists(break_path):
            self.break_sound = pygame.mixer.Sound(break_path)
            self.break_sound.set_volume(0.4)  # Volume reduzido

    def update(self, game_speed, player):
        now = pygame.time.get_ticks()
        # Só aparece se não houver obstáculos próximos
        can_spawn = True
        for obs in getattr(player, 'game', []).obstacle_manager.obstacles if hasattr(player, 'game') else []:
            # Powerup só aparece se estiver a pelo menos 600px de qualquer obstáculo
            if abs(obs.rect.x - player.dino_rect.x) < 600:
                can_spawn = False
                break
        if len(self.power_ups) == 0 and now - self.last_powerup_time > self.powerup_cooldown and can_spawn:
            # Garante que só UM tipo aparece a cada 30s, alternando
            if (now // self.powerup_cooldown) % 2 == 0:
                powerup = Shield()
            else:
                powerup = Hammer()
            powerup.rect.x = player.dino_rect.x + 1200  # Spawn ainda mais longe
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
                if self.powerup_sound:
                    self.powerup_sound.play()
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset(self):
        self.power_ups = []
        # Reinicia o timer para o momento atual, evitando spawn imediato
        self.last_powerup_time = pygame.time.get_ticks()
