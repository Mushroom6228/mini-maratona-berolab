<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import random # Importa o módulo random para gerar números aleatórios.
# Importa constantes como tipos de power-ups e largura da tela.
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, SCREEN_WIDTH
# Importa as classes base de PowerUp, Hammer (Martelo) e Shield (Escudo).
=======
# dino_runner/components/powerups/powerup_manager.py
import pygame
import random
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, SCREEN_WIDTH
# Importa as classes PowerUp, Hammer e Shield
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
from dino_runner.components.powerups.powerup import PowerUp
from dino_runner.components.powerups.hammer import Hammer
from dino_runner.components.powerups.shield import Shield

class PowerUpManager:
<<<<<<< HEAD
    # O construtor recebe o som do power-up e o gerenciador de obstáculos (opcionalmente).
    def __init__(self, powerup_sound=None, obstacle_manager=None):
        self.power_ups = [] # Lista para armazenar os power-ups ativos na tela.
        self.last_spawn_time = pygame.time.get_ticks() # Registra o tempo do último spawn de power-up.
        self.spawn_interval = 20000 # Define o intervalo de tempo para o spawn de power-ups (20 segundos).
        self.powerup_sound = powerup_sound # Armazena o objeto de som do power-up.
        self.obstacle_manager = obstacle_manager # Armazena a referência para o gerenciador de obstáculos.
        self.MIN_DISTANCE_FROM_OBSTACLE = 200 # Distância mínima em pixels de um obstáculo para um power-up ser gerado.
=======
    def __init__(self, powerup_sound=None): # O __init__ aceita powerup_sound como parâmetro
        self.power_ups = []
        self.last_spawn_time = pygame.time.get_ticks()
        # Ajustado para 20 segundos (20000 milissegundos)
        self.spawn_interval = 20000 
        self.powerup_sound = powerup_sound # Armazena o objeto de som
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

    # Atualiza o estado dos power-ups a cada quadro.
    def update(self, game_speed, player):
<<<<<<< HEAD
        self.add_power_up() # Tenta adicionar um novo power-up.
        # Itera sobre uma cópia da lista para permitir a remoção de power-ups durante a iteração.
        for power_up in list(self.power_ups):
            power_up.update(game_speed) # Atualiza a posição do power-up (move para a esquerda).
            if power_up.rect.right < 0: # Se o power-up saiu completamente da tela.
                self.power_ups.remove(power_up) # Remove o power-up da lista.
            # Verifica a colisão entre o jogador e o power-up.
            if player.dino_rect.colliderect(power_up.rect):
                if power_up.type == SHIELD_TYPE: # Se o power-up for um escudo.
                    player.has_shield = True # Ativa o escudo para o jogador.
                    # Define o tempo em que o escudo irá expirar (10 segundos a partir de agora).
                    player.shield_time_up = pygame.time.get_ticks() + 10000
                elif power_up.type == HAMMER_TYPE: # Se o power-up for um martelo.
                    player.has_hammer = True # Ativa o martelo para o jogador.
                    # Define o tempo em que o martelo irá expirar (10 segundos a partir de agora).
                    player.hammer_time_up = pygame.time.get_ticks() + 10000
                if self.powerup_sound: # Se o som do power-up estiver carregado.
                    self.powerup_sound.play() # Toca o som do power-up.
                self.power_ups.remove(power_up) # Remove o power-up da tela após a coleta.
=======
        self.add_power_up()
        for power_up in list(self.power_ups):
            power_up.update(game_speed, player)
            if power_up.rect.right < 0:
                self.power_ups.remove(power_up)
            
            # Detecção de colisão
            if player.dino_rect.colliderect(power_up.rect):
                if power_up.type == SHIELD_TYPE:
                    player.has_shield = True
                    # Duração do power-up aumentada para 10 segundos (10000 milissegundos)
                    player.shield_time_up = pygame.time.get_ticks() + 10000 
                elif power_up.type == HAMMER_TYPE:
                    player.has_hammer = True
                    # Duração do power-up aumentada para 10 segundos (10000 milissegundos)
                    player.hammer_time_up = pygame.time.get_ticks() + 10000 
                
                # Toca o som do power-up
                if self.powerup_sound: # Verifica se o som existe antes de tentar tocar
                    self.powerup_sound.play()

                self.power_ups.remove(power_up)
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

    # Desenha todos os power-ups ativos na tela.
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen) # Desenha cada power-up individualmente.

<<<<<<< HEAD
    # Adiciona um novo power-up à tela, se o intervalo de spawn permitir.
    def add_power_up(self):
        now = pygame.time.get_ticks() # Obtém o tempo atual.
        if now - self.last_spawn_time > self.spawn_interval: # Se o intervalo de spawn passou.
            power_up_candidate = None # Inicializa o power-up candidato como None.
            # Escolhe aleatoriamente entre um escudo ou um martelo.
            power_up_choice = random.choice([SHIELD_TYPE, HAMMER_TYPE])
            
            if power_up_choice == SHIELD_TYPE: # Se a escolha for escudo.
                power_up_candidate = Shield() # Cria uma nova instância de Shield.
            elif power_up_choice == HAMMER_TYPE: # Se a escolha for martelo.
                power_up_candidate = Hammer() # Cria uma nova instância de Hammer.
            
            can_spawn = True # Flag para verificar se o power-up pode ser gerado.
            if power_up_candidate and self.obstacle_manager: # Se houver um candidato a power-up e um gerenciador de obstáculos.
                # Verifica se o power-up candidato está muito próximo de qualquer obstáculo existente.
                for obstacle in self.obstacle_manager.obstacles:
                    # Calcula a distância horizontal entre o power-up e o obstáculo.
                    distance = abs(power_up_candidate.rect.x - obstacle.rect.x)
                    # Se a distância for menor que a mínima permitida e o obstáculo ainda estiver na tela.
                    if distance < self.MIN_DISTANCE_FROM_OBSTACLE and obstacle.rect.x > 0:
                        can_spawn = False # Não pode gerar o power-up aqui.
                        break # Sai do loop de verificação de obstáculos.
            
            if can_spawn and power_up_candidate: # Se puder gerar e houver um power-up candidato.
                self.power_ups.append(power_up_candidate) # Adiciona o power-up à lista.
                self.last_spawn_time = now # Atualiza o tempo do último spawn.
                # Define um novo intervalo de spawn aleatório para o próximo power-up.
                self.spawn_interval = random.randint(15000, 25000)

    # Reseta o gerenciador de power-ups para um novo jogo.
    def reset(self):
        self.power_ups = [] # Limpa a lista de power-ups.
        self.last_spawn_time = pygame.time.get_ticks() # Reseta o temporizador do último spawn.
=======
    def add_power_up(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_interval:
            power_up_choice = random.choice([SHIELD_TYPE, HAMMER_TYPE])
            
            if power_up_choice == SHIELD_TYPE:
                self.power_ups.append(Shield())
            elif power_up_choice == HAMMER_TYPE:
                self.power_ups.append(Hammer())
            
            self.last_spawn_time = now
            # O intervalo de spawn aleatório agora será entre 15 e 25 segundos
            self.spawn_interval = random.randint(15000, 25000)

    def reset(self):
        self.power_ups = []
        self.last_spawn_time = pygame.time.get_ticks()
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
