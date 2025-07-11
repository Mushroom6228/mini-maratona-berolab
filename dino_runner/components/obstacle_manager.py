<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame para desenvolvimento de jogos.
import random # Importa o módulo random para geração de números aleatórios.
import os # Importa o módulo os para interagir com o sistema operacional (caminhos de arquivo).
# Importa constantes como largura da tela e tipos de cactos e pássaros.
from dino_runner.utils.constants import SCREEN_WIDTH, LARGE_CACTUS, SMALL_CACTUS, BIRD
# Importa as classes específicas de obstáculos: Cactus e Bird.
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
# Importa a classe base Obstacle.
from dino_runner.components.obstacles.obstacle import Obstacle
# Importa a função para gerenciar caminhos de recursos.
from dino_runner.utils.resource_manager import resource_path

class ObstacleManager:
    def __init__(self):
        self.obstacles = [] # Lista para armazenar os obstáculos ativos na tela.
        self.last_spawn_time = pygame.time.get_ticks() # Registra o tempo do último spawn de obstáculo.
        self.spawn_interval = 1500 # Define o intervalo de tempo padrão para o spawn de obstáculos (1.5 segundos).
        # Define o caminho para o arquivo de som de quebra (quando o martelo atinge um obstáculo).
        break_path = resource_path('dino_runner/assets/Other/break.wav')
        if os.path.exists(break_path): # Verifica se o arquivo de som de quebra existe.
            self.break_sound = pygame.mixer.Sound(break_path) # Carrega o som de quebra.
            self.break_sound.set_volume(0.2) # Define o volume do som de quebra para 20%.
        else:
            self.break_sound = None # Se o arquivo não existir, define o som como None.
        # Define o caminho para o arquivo de som de dano (quando o dinossauro colide sem proteção).
        hurt_path = resource_path('dino_runner/assets/Other/hurt.wav')
        if os.path.exists(hurt_path): # Verifica se o arquivo de som de dano existe.
            self.hurt_sound = pygame.mixer.Sound(hurt_path) # Carrega o som de dano.
            self.hurt_sound.set_volume(1.0) # Define o volume do som de dano para 100%.
        else:
            self.hurt_sound = None # Se o arquivo não existir, define o som como None.

    def update(self, game_speed, player): # Atualiza o estado dos obstáculos a cada quadro.
        self.add_obstacle() # Tenta adicionar um novo obstáculo.
        # Itera sobre uma cópia da lista para permitir a remoção de obstáculos durante a iteração.
        for obstacle in list(self.obstacles):
            obstacle.update(game_speed, player) # Atualiza a posição do obstáculo (move para a esquerda).
            if obstacle.rect.right < 0: # Se o obstáculo saiu completamente da tela.
                self.obstacles.remove(obstacle) # Remove o obstáculo da lista.
            # Cria um retângulo de colisão menor para o dinossauro para colisões mais precisas.
            collision_rect = player.dino_rect.inflate(-28, -14)
            collision_rect.center = player.dino_rect.center # Centraliza o novo retângulo.
            if collision_rect.colliderect(obstacle.rect): # Verifica a colisão entre o dinossauro e o obstáculo.
                if player.has_shield or player.has_hammer: # Se o jogador tem escudo ou martelo.
                    self.obstacles.remove(obstacle) # Remove o obstáculo (ele é "quebrado").
                    if self.break_sound: # Se o som de quebra estiver carregado.
                        self.break_sound.play() # Toca o som de quebra.
                    return False # Retorna False, indicando que não houve dano ao jogador.
                elif player.is_invincible: # Se o jogador está invencível.
                    self.obstacles.remove(obstacle) # Remove o obstáculo.
                    return False # Retorna False, indicando que não houve dano ao jogador.
                else: # Se o jogador não tem proteção e não está invencível.
                    return True # Retorna True, indicando que o jogador sofreu dano.
        return False # Retorna False se nenhuma colisão com dano foi detectada.

    def draw(self, screen): # Desenha todos os obstáculos ativos na tela.
=======
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
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
        for obstacle in self.obstacles:
            obstacle.draw(screen) # Desenha cada obstáculo individualmente.

<<<<<<< HEAD
    def add_obstacle(self): # Adiciona um novo obstáculo à tela, se o intervalo de spawn permitir.
        now = pygame.time.get_ticks() # Obtém o tempo atual.
        if now - self.last_spawn_time > self.spawn_interval: # Se o intervalo de spawn passou.
            obstacle_type = random.randint(0, 1) # Escolhe aleatoriamente o tipo de obstáculo (0 para cacto, 1 para pássaro).
            # Se o tipo for cacto e houver imagens de cactos disponíveis.
            if obstacle_type == 0 and (LARGE_CACTUS or SMALL_CACTUS):
                self.obstacles.append(Cactus()) # Adiciona um novo cacto à lista.
            # Se o tipo for pássaro e houver imagens de pássaros disponíveis.
            elif obstacle_type == 1 and BIRD:
                self.obstacles.append(Bird()) # Adiciona um novo pássaro à lista.
            self.last_spawn_time = now # Atualiza o tempo do último spawn.
            # Define um novo intervalo de spawn aleatório para o próximo obstáculo.
            self.spawn_interval = random.randint(1000, 2500)

    def reset(self): # Reseta o gerenciador de obstáculos para um novo jogo.
        self.obstacles = [] # Limpa a lista de obstáculos.
        self.last_spawn_time = pygame.time.get_ticks() # Reseta o temporizador do último spawn.
=======
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
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
