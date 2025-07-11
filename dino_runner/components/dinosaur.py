<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
# Importa constantes como imagens de corrida, pulo, abaixar, com escudo e martelo, e o tipo padrão.
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, RUNNING_SHIELD, JUMPING_SHIELD, DUCKING_SHIELD, RUNNING_HAMMER, JUMPING_HAMMER, DUCKING_HAMMER, DEFAULT_TYPE

class Dinosaur:
    X_POS = 80 # Posição X inicial do dinossauro na tela.
    Y_POS = 310 # Posição Y inicial do dinossauro quando correndo.
    Y_POS_DUCK = 340 # Posição Y do dinossauro quando abaixado.
    JUMP_VEL = 8.5 # Velocidade inicial do pulo do dinossauro.
    INVINCIBILITY_DURATION = 3000 # Duração da invencibilidade em milissegundos (3 segundos).
    BLINK_INTERVAL = 100 # Intervalo de tempo em milissegundos para o efeito de piscar.

    def __init__(self):
        self.type = DEFAULT_TYPE # Define o tipo inicial do dinossauro como padrão.
        if RUNNING: # Verifica se a lista de imagens de corrida não está vazia.
            self.image = RUNNING[0] # Define a imagem inicial do dinossauro como a primeira imagem de corrida.
        else:
            # Fallback: Se as imagens de corrida estiverem vazias, cria uma superfície de placeholder.
            self.image = pygame.Surface((50, 50)) # Cria uma superfície de 50x50 pixels.
            self.image.fill((255, 0, 0)) # Preenche a superfície com a cor vermelha.
        self.dino_rect = self.image.get_rect() # Obtém o retângulo que envolve a imagem do dinossauro.
        self.dino_rect.x = self.X_POS # Define a posição X do retângulo do dinossauro.
        self.dino_rect.y = self.Y_POS # Define a posição Y do retângulo do dinossauro.
        self.is_running = True # Flag para indicar se o dinossauro está correndo.
        self.is_jumping = False # Flag para indicar se o dinossauro está pulando.
        self.is_ducking = False # Flag para indicar se o dinossauro está abaixado.
        self.jump_vel = self.JUMP_VEL # Velocidade de pulo atual do dinossauro.
        self.step_index = 0 # Índice para controlar a animação de corrida/abaixar.
        self.has_shield = False # Flag para indicar se o dinossauro tem o power-up de escudo.
        self.has_hammer = False # Flag para indicar se o dinossauro tem o power-up de martelo.
        self.shield_time_up = 0 # Tempo em que o escudo irá expirar.
        self.hammer_time_up = 0 # Tempo em que o martelo irá expirar.
        self.is_invincible = False # Flag para indicar se o dinossauro está invencível.
        self.invincible_start_time = 0 # Tempo de início da invencibilidade.
        self.last_blink_time = 0 # Tempo da última vez que o dinossauro piscou (para efeito de invencibilidade/power-up).
        self.show_dino = True # Flag para controlar a visibilidade do dinossauro (para efeito de piscar).

    def update(self, user_input): # Método para atualizar o estado do dinossauro a cada quadro.
        current_time = pygame.time.get_ticks() # Obtém o tempo atual em milissegundos.
        if self.is_jumping: # Se o dinossauro estiver pulando.
            self.jump() # Chama o método de pulo.
        elif user_input[pygame.K_DOWN]: # Se a tecla "seta para baixo" estiver pressionada.
            self.is_ducking = True # Define o estado como abaixado.
            self.is_running = False # Define o estado como não correndo.
            self.duck() # Chama o método de abaixar.
        else: # Se nenhuma das condições acima for verdadeira (dinossauro está no chão e não abaixado).
            self.is_ducking = False # Define o estado como não abaixado.
            self.is_running = True # Define o estado como correndo.
            self.run() # Chama o método de corrida.
        if self.step_index >= 10: # Se o índice de passo atingir 10 (para animação de corrida/abaixar).
            self.step_index = 0 # Reinicia o índice de passo.
        if self.is_invincible: # Se o dinossauro estiver invencível.
            # Se o tempo de invencibilidade excedeu a duração.
            if current_time - self.invincible_start_time > self.INVINCIBILITY_DURATION:
                self.is_invincible = False # Desativa a invencibilidade.
                self.show_dino = True # Garante que o dinossauro esteja visível.
            # Se o tempo desde o último piscar excedeu o intervalo de piscar.
            elif current_time - self.last_blink_time > self.BLINK_INTERVAL:
                self.show_dino = not self.show_dino # Alterna a visibilidade do dinossauro (pisca).
                self.last_blink_time = current_time # Atualiza o tempo do último piscar.
        elif self.has_shield or self.has_hammer: # Se o dinossauro tiver escudo ou martelo.
            time_remaining = 0 # Inicializa o tempo restante do power-up.
            if self.has_shield: # Se tiver escudo.
                time_remaining = self.shield_time_up - current_time # Calcula o tempo restante do escudo.
            elif self.has_hammer: # Se tiver martelo.
                time_remaining = self.hammer_time_up - current_time # Calcula o tempo restante do martelo.
            # Se faltarem 3 segundos ou menos para o power-up acabar e ele ainda estiver ativo.
            if time_remaining <= 3000 and time_remaining > 0:
                # Se o tempo desde o último piscar excedeu o intervalo de piscar.
                if current_time - self.last_blink_time > self.BLINK_INTERVAL:
                    self.show_dino = not self.show_dino # Alterna a visibilidade do dinossauro (pisca).
                    self.last_blink_time = current_time # Atualiza o tempo do último piscar.
            else:
                self.show_dino = True # Garante que o dinossauro esteja visível se o power-up não estiver perto do fim.
        else:
            self.show_dino = True # Garante que o dinossauro esteja sempre visível se não estiver invencível ou com power-up acabando.
        if self.has_hammer: # Se o dinossauro tem o power-up de martelo.
            # Verifica se as listas de imagens de martelo não estão vazias.
            if RUNNING_HAMMER and JUMPING_HAMMER and DUCKING_HAMMER:
                if self.is_jumping: # Se estiver pulando.
                    self.image = JUMPING_HAMMER # Define a imagem de pulo com martelo.
                elif self.is_ducking: # Se estiver abaixado.
                    self.image = DUCKING_HAMMER[self.step_index // 5] # Define a imagem de abaixar com martelo (animada).
                else: # Se estiver correndo.
                    self.image = RUNNING_HAMMER[self.step_index // 5] # Define a imagem de corrida com martelo (animada).
            else:
                self.set_default_image() # Fallback: Define a imagem padrão se as imagens de martelo não existirem.
        elif self.has_shield: # Se o dinossauro tem o power-up de escudo.
            # Verifica se as listas de imagens de escudo não estão vazias.
            if RUNNING_SHIELD and JUMPING_SHIELD and DUCKING_SHIELD:
                if self.is_jumping: # Se estiver pulando.
                    self.image = JUMPING_SHIELD # Define a imagem de pulo com escudo.
                elif self.is_ducking: # Se estiver abaixado.
                    self.image = DUCKING_SHIELD[self.step_index // 5] # Define a imagem de abaixar com escudo (animada).
                else: # Se estiver correndo.
                    self.image = RUNNING_SHIELD[self.step_index // 5] # Define a imagem de corrida com escudo (animada).
            else:
                self.set_default_image() # Fallback: Define a imagem padrão se as imagens de escudo não existirem.
        else: # Se não tiver nenhum power-up ativo.
            self.set_default_image() # Define a imagem padrão do dinossauro.
        # Atualiza o retângulo de colisão do dinossauro com base na nova imagem e mantém a posição.
        self.dino_rect = self.image.get_rect(x=self.dino_rect.x, y=self.dino_rect.y)
        if self.is_ducking: # Se o dinossauro estiver abaixado.
            self.dino_rect.y = self.Y_POS_DUCK # Ajusta a posição Y para a posição de abaixar.
        else:
            if not self.is_jumping: # Se não estiver pulando.
                self.dino_rect.y = self.Y_POS # Garante que a posição Y esteja na posição de corrida.
=======
# dino_runner/components/dinosaur.py
import pygame
# Importa as constantes diretamente, pois resource_path já as carregou em constants.py
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, RUNNING_SHIELD, JUMPING_SHIELD, DUCKING_SHIELD, RUNNING_HAMMER, JUMPING_HAMMER, DUCKING_HAMMER, DEFAULT_TYPE

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    INVINCIBILITY_DURATION = 3000 # 3 segundos em milissegundos
    BLINK_INTERVAL = 100 # Intervalo de piscar em milissegundos

    def __init__(self):
        self.type = DEFAULT_TYPE
        # Garante que RUNNING não esteja vazio antes de acessar seus elementos
        if RUNNING:
            self.image = RUNNING[0]
        else:
            # Fallback se RUNNING estiver vazio (ex: imagem placeholder)
            print("Aviso: RUNNING está vazio. Usando uma imagem placeholder.")
            self.image = pygame.Surface((50, 50)) # Superfície placeholder
            self.image.fill((255, 0, 0)) # Placeholder quadrado vermelho

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.is_running = True
        self.is_jumping = False
        self.is_ducking = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0
        self.has_shield = False
        self.has_hammer = False
        self.shield_time_up = 0
        self.hammer_time_up = 0

        # Novos atributos para invencibilidade e piscar de power-up
        self.is_invincible = False
        self.invincible_start_time = 0
        self.last_blink_time = 0
        self.show_dino = True # Controla a visibilidade para o efeito de piscar

    def update(self, user_input):
        current_time = pygame.time.get_ticks()

        # Lógica de estado (correr, pular, agachar)
        if self.is_jumping:
            self.jump()
        elif user_input[pygame.K_DOWN]:
            self.is_ducking = True
            self.is_running = False
            self.duck()
        else:
            self.is_ducking = False
            self.is_running = True
            self.run()

        if self.step_index >= 10:
            self.step_index = 0

        # Lida com o piscar da invencibilidade e power-ups
        if self.is_invincible:
            if current_time - self.invincible_start_time > self.INVINCIBILITY_DURATION:
                self.is_invincible = False
                self.show_dino = True # Garante que o dinossauro esteja visível após a invencibilidade
            elif current_time - self.last_blink_time > self.BLINK_INTERVAL:
                self.show_dino = not self.show_dino # Alterna a visibilidade
                self.last_blink_time = current_time
        elif self.has_shield or self.has_hammer:
            # Verifica se faltam 3 segundos ou menos para o power-up acabar
            time_remaining = 0
            if self.has_shield:
                time_remaining = self.shield_time_up - current_time
            elif self.has_hammer:
                time_remaining = self.hammer_time_up - current_time
            
            if time_remaining <= 3000 and time_remaining > 0: # Se faltam 3 segundos ou menos e ainda não acabou
                if current_time - self.last_blink_time > self.BLINK_INTERVAL:
                    self.show_dino = not self.show_dino # Alterna a visibilidade
                    self.last_blink_time = current_time
            else:
                self.show_dino = True # Garante que o dinossauro esteja visível se o power-up não estiver perto de acabar
        else:
            self.show_dino = True # Sempre visível se não estiver invencível ou com power-up acabando

        # Atualiza a imagem com base nos power-ups e estado atual
        if self.has_hammer:
            # Garante que as imagens existam antes de tentar acessá-las
            if RUNNING_HAMMER and JUMPING_HAMMER and DUCKING_HAMMER:
                if self.is_jumping:
                    self.image = JUMPING_HAMMER
                elif self.is_ducking:
                    self.image = DUCKING_HAMMER[self.step_index // 5]
                else:
                    self.image = RUNNING_HAMMER[self.step_index // 5]
            else: # Fallback se as imagens do martelo não existirem
                self.set_default_image()
        elif self.has_shield:
            # Garante que as imagens existam antes de tentar acessá-las
            if RUNNING_SHIELD and JUMPING_SHIELD and DUCKING_SHIELD:
                if self.is_jumping:
                    self.image = JUMPING_SHIELD
                elif self.is_ducking:
                    self.image = DUCKING_SHIELD[self.step_index // 5]
                else:
                    self.image = RUNNING_SHIELD[self.step_index // 5]
            else: # Fallback se as imagens do escudo não existirem
                self.set_default_image()
        else:
            self.set_default_image()

        # Atualiza o retângulo de colisão com base na nova imagem
        self.dino_rect = self.image.get_rect(x=self.dino_rect.x, y=self.dino_rect.y)
        if self.is_ducking:
            self.dino_rect.y = self.Y_POS_DUCK # Ajusta a posição Y para agachamento
        else:
            # Se não estiver agachando, garante que esteja na posição de corrida/pulo
            if not self.is_jumping: # Só ajusta para Y_POS se não estiver pulando
                self.dino_rect.y = self.Y_POS

    def set_default_image(self):
        """Define a imagem padrão do dinossauro (sem power-ups)."""
        if self.is_jumping:
            self.image = JUMPING
        elif self.is_ducking:
            if DUCKING:
                self.image = DUCKING[self.step_index // 5]
            else:
                self.image = RUNNING[0] # Fallback
        else:
            if RUNNING:
                self.image = RUNNING[self.step_index // 5]
            else:
                self.image = pygame.Surface((50, 50)) # Placeholder
                self.image.fill((255, 0, 0))

    def run(self):
        self.step_index += 1

    def jump(self):
        if self.is_jumping:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.is_jumping = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = self.Y_POS # Garante que ele pouse no chão
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

    def set_default_image(self): # Define a imagem padrão do dinossauro (sem power-ups).
        if self.is_jumping: # Se estiver pulando.
            self.image = JUMPING # Define a imagem de pulo padrão.
        elif self.is_ducking: # Se estiver abaixado.
            if DUCKING: # Verifica se a lista de imagens de abaixar não está vazia.
                self.image = DUCKING[self.step_index // 5] # Define a imagem de abaixar padrão (animada).
            else:
                self.image = RUNNING[0] # Fallback: Usa a primeira imagem de corrida se as de abaixar não existirem.
        else: # Se estiver correndo.
            if RUNNING: # Verifica se a lista de imagens de corrida não está vazia.
                self.image = RUNNING[self.step_index // 5] # Define a imagem de corrida padrão (animada).
            else:
                self.image = pygame.Surface((50, 50)) # Fallback: Cria uma superfície de placeholder.
                self.image.fill((255, 0, 0)) # Preenche com vermelho.

<<<<<<< HEAD
    def run(self): # Método para a animação de corrida.
        self.step_index += 1 # Incrementa o índice de passo para a próxima imagem da animação.

    def jump(self): # Método para a lógica de pulo.
        if self.is_jumping: # Se o dinossauro estiver pulando.
            self.dino_rect.y -= self.jump_vel * 4 # Move o dinossauro para cima.
            self.jump_vel -= 0.8 # Diminui a velocidade de pulo (gravidade).
        if self.jump_vel < -self.JUMP_VEL: # Se a velocidade de pulo se tornou negativa e atingiu o limite inferior.
            self.is_jumping = False # Desativa o estado de pulo.
            self.jump_vel = self.JUMP_VEL # Reseta a velocidade de pulo para o valor inicial.
            self.dino_rect.y = self.Y_POS # Garante que o dinossauro pouse no chão.

    def start_jump(self): # Método para iniciar o pulo.
        if not self.is_jumping: # Só permite pular se o dinossauro não estiver pulando.
            self.is_jumping = True # Ativa o estado de pulo.
            self.is_running = False # Desativa o estado de corrida.
            self.is_ducking = False # Desativa o estado de abaixar.

    def duck(self): # Método para a animação de abaixar.
        self.step_index += 1 # Incrementa o índice de passo para a próxima imagem da animação.

    def draw(self, screen): # Método para desenhar o dinossauro na tela.
        if self.show_dino: # Só desenha o dinossauro se a flag 'show_dino' for True (para o efeito de piscar).
            screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y)) # Desenha a imagem do dinossauro na sua posição.

    def start_invincibility(self, current_time): # Método para ativar o estado de invencibilidade.
        self.is_invincible = True # Ativa a flag de invencibilidade.
        self.invincible_start_time = current_time # Registra o tempo de início da invencibilidade.
        self.last_blink_time = current_time # Reseta o temporizador do piscar.
        self.show_dino = False # Esconde o dinossauro para iniciar o efeito de piscar.
=======
    def duck(self):
        self.step_index += 1

    def draw(self, screen):
        if self.show_dino: # Só desenha se estiver visível (para o efeito de piscar)
            screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def start_invincibility(self, current_time):
        """Ativa o estado de invencibilidade para o dinossauro."""
        self.is_invincible = True
        self.invincible_start_time = current_time
        self.last_blink_time = current_time # Reseta o timer de piscar
        self.show_dino = False # Começa o piscar escondendo o dinossauro
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
