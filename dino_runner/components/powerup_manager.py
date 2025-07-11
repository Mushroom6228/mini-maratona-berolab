import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import random # Importa o módulo random para gerar números aleatórios.
# Importa constantes como tipos de power-ups e largura da tela.
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, SCREEN_WIDTH
# Importa as classes base de PowerUp, Hammer (Martelo) e Shield (Escudo).
from dino_runner.components.powerups.powerup import PowerUp
from dino_runner.components.powerups.hammer import Hammer
from dino_runner.components.powerups.shield import Shield

class PowerUpManager:
    # O construtor recebe o som do power-up e o gerenciador de obstáculos (opcionalmente).
    def __init__(self, powerup_sound=None, obstacle_manager=None):
        self.power_ups = [] # Lista para armazenar os power-ups ativos na tela.
        self.last_spawn_time = pygame.time.get_ticks() # Registra o tempo do último spawn de power-up.
        self.spawn_interval = 20000 # Define o intervalo de tempo para o spawn de power-ups (20 segundos).
        self.powerup_sound = powerup_sound # Armazena o objeto de som do power-up.
        self.obstacle_manager = obstacle_manager # Armazena a referência para o gerenciador de obstáculos.
        self.MIN_DISTANCE_FROM_OBSTACLE = 200 # Distância mínima em pixels de um obstáculo para um power-up ser gerado.

    # Atualiza o estado dos power-ups a cada quadro.
    def update(self, game_speed, player):
        self.add_power_up() # Tenta adicionar um novo power-up.
        # Itera sobre uma cópia da lista para permitir a remoção de power-ups durante a iteração.
        for power_up in list(self.power_ups):
            power_up.update(game_speed, player) # Atualiza a posição do power-up (move para a esquerda).
            if power_up.rect.right < 0: # Se o power-up saiu completamente da tela.
                self.power_ups.remove(power_up) # Remove o power-up da lista.
            # Verifica a colisão entre o jogador e o power-up.
            if player.dino_rect.colliderect(power_up.rect):
                game = getattr(player, 'game', None) # Obtém a instância do jogo a partir do jogador, se existir.
                if power_up.type == SHIELD_TYPE: # Se o power-up for um escudo.
                    player.has_shield = True # Ativa o escudo para o jogador.
                    # Define o tempo em que o escudo irá expirar (10 segundos a partir de agora).
                    player.shield_time_up = pygame.time.get_ticks() + 10000
                    # Toca o som de upgrade se disponível no objeto game, caso contrário, toca o som powerup_sound.
                    if game and hasattr(game, 'upgrade_sound') and game.upgrade_sound:
                        game.upgrade_sound.play()
                    elif self.powerup_sound:
                        self.powerup_sound.play()
                elif power_up.type == HAMMER_TYPE: # Se o power-up for um martelo.
                    player.has_hammer = True # Ativa o martelo para o jogador.
                    # Define o tempo em que o martelo irá expirar (10 segundos a partir de agora).
                    player.hammer_time_up = pygame.time.get_ticks() + 10000
                    # Toca o som de upgrade se disponível no objeto game, caso contrário, toca o som powerup_sound.
                    if game and hasattr(game, 'upgrade_sound') and game.upgrade_sound:
                        game.upgrade_sound.play()
                    elif self.powerup_sound:
                        self.powerup_sound.play()
                self.power_ups.remove(power_up) # Remove o power-up da tela após a coleta.

    # Desenha todos os power-ups ativos na tela.
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen) # Desenha cada power-up individualmente.

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
