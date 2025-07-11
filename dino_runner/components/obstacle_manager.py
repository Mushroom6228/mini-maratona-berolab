# dino_runner/components/obstacle_manager.py
import pygame
import random
# Importa SCREEN_WIDTH e as novas constantes de cacto e pássaro
from dino_runner.utils.constants import SCREEN_WIDTH, LARGE_CACTUS, SMALL_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus # Importa Cactus
from dino_runner.components.obstacles.bird import Bird # Importa Bird
from dino_runner.components.obstacles.obstacle import Obstacle # Importa a classe base Obstacle

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 1500 # milissegundos

    def update(self, game_speed, player):
        self.add_obstacle()
        for obstacle in list(self.obstacles):
            obstacle.update(game_speed, player) # Passa o player para o update do obstáculo
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
            
            # Detecção de colisão
            # Cria um retângulo de colisão menor para o dinossauro
            # Reduz a largura em 20 pixels (10 de cada lado) e a altura em 10 pixels (5 de cima e 5 de baixo)
            collision_rect = player.dino_rect.inflate(-20, -10) 
            # Ajusta a posição do novo retângulo para que ele fique centralizado
            collision_rect.center = player.dino_rect.center

            if collision_rect.colliderect(obstacle.rect): # Usa o novo retângulo para colisão
                # Se o jogador tem escudo, martelo ou está invencível, o obstáculo é removido sem dano
                if player.has_shield or player.has_hammer or player.is_invincible:
                    self.obstacles.remove(obstacle)
                    return False # Não houve dano, obstáculo removido
                else:
                    return True # O jogador colidiu com um obstáculo, leva dano
        return False # Nenhuma colisão

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def add_obstacle(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_interval:
            obstacle_type = random.randint(0, 1)
            # Garante que as listas de imagens de cacto ou pássaro não estejam vazias
            if obstacle_type == 0 and (LARGE_CACTUS or SMALL_CACTUS): # Verifica se há cactos disponíveis
                self.obstacles.append(Cactus())
            elif obstacle_type == 1 and BIRD: # Verifica se há pássaros disponíveis
                self.obstacles.append(Bird())
            else:
                # Se as listas de imagens estiverem vazias, não adiciona obstáculo
                print("Aviso: Não foi possível adicionar obstáculo. Imagens de Cactos ou Pássaros ausentes.")
                
            self.last_spawn_time = now
            self.spawn_interval = random.randint(1000, 2500) # Varia o tempo de spawn

    def reset(self):
        """Reseta a lista de obstáculos para um novo jogo."""
        self.obstacles = []
        self.last_spawn_time = pygame.time.get_ticks() # Reseta o timer de spawn
