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

    def start_jump(self):
        # Inicia o pulo apenas se não estiver pulando
        if not self.is_jumping:
            self.is_jumping = True
            self.is_running = False
            self.is_ducking = False

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
