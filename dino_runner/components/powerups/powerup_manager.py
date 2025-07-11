# dino_runner/components/powerups/powerup_manager.py
import pygame
import random
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, SCREEN_WIDTH
# Importa as classes PowerUp, Hammer e Shield
from dino_runner.components.powerups.powerup import PowerUp
from dino_runner.components.powerups.hammer import Hammer
from dino_runner.components.powerups.shield import Shield

class PowerUpManager:
    def __init__(self, powerup_sound=None, obstacle_manager=None): # Adiciona obstacle_manager ao init
        self.power_ups = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 20000 # milissegundos
        self.powerup_sound = powerup_sound # Armazena o objeto de som
        self.obstacle_manager = obstacle_manager # Armazena o obstacle_manager
        self.MIN_DISTANCE_FROM_OBSTACLE = 200 # Distância mínima em pixels

    def update(self, game_speed, player):
        self.add_power_up()
        for power_up in list(self.power_ups):
            power_up.update(game_speed, player)
            if power_up.rect.right < 0:
                self.power_ups.remove(power_up)
            
            # Detecção de colisão
            if player.dino_rect.colliderect(power_up.rect):
                if power_up.type == SHIELD_TYPE:
                    player.has_shield = True
                    player.shield_time_up = pygame.time.get_ticks() + 10000 # 10 segundos
                elif power_up.type == HAMMER_TYPE:
                    player.has_hammer = True
                    player.hammer_time_up = pygame.time.get_ticks() + 10000 # 10 segundos
                
                # Toca o som do power-up
                if self.powerup_sound: # Verifica se o som existe antes de tentar tocar
                    self.powerup_sound.play()

                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def add_power_up(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_interval:
            # Tenta gerar um power-up
            power_up_candidate = None
            power_up_choice = random.choice([SHIELD_TYPE, HAMMER_TYPE])
            
            if power_up_choice == SHIELD_TYPE:
                power_up_candidate = Shield()
            elif power_up_choice == HAMMER_TYPE:
                power_up_candidate = Hammer()
            
            # Verifica se o power-up candidato está muito perto de algum obstáculo
            can_spawn = True
            if power_up_candidate and self.obstacle_manager:
                for obstacle in self.obstacle_manager.obstacles:
                    # Calcula a distância horizontal entre o power-up e o obstáculo
                    distance = abs(power_up_candidate.rect.x - obstacle.rect.x)
                    # Verifica se estão muito próximos e se o obstáculo ainda está na tela
                    if distance < self.MIN_DISTANCE_FROM_OBSTACLE and obstacle.rect.x > 0:
                        can_spawn = False
                        break
            
            if can_spawn and power_up_candidate:
                self.power_ups.append(power_up_candidate)
                self.last_spawn_time = now
                self.spawn_interval = random.randint(15000, 25000) # Varia o tempo de spawn

    def reset(self):
        self.power_ups = []
        self.last_spawn_time = pygame.time.get_ticks()
