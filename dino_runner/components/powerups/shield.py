import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
# Importa as constantes SHIELD (imagem do escudo) e SHIELD_TYPE (tipo do power-up).
from dino_runner.utils.constants import SHIELD, SHIELD_TYPE
from dino_runner.components.powerups.powerup import PowerUp # Importa a classe base PowerUp.

class Shield(PowerUp):
    def __init__(self):
        # Define a imagem a ser usada para o escudo.
        # Se a constante SHIELD (imagem carregada) não for None, usa-a.
        # Caso contrário, cria uma superfície de placeholder azul.
        image_to_use = SHIELD if SHIELD is not None else pygame.Surface((30, 30), flags=pygame.SRCALPHA)
        if SHIELD is None: # Se a imagem SHIELD não foi carregada.
            image_to_use.fill((0, 0, 255)) # Preenche o placeholder com a cor azul.
        self.type = SHIELD_TYPE # Define o tipo do power-up como SHIELD_TYPE.
        super().__init__(image_to_use, self.type) # Chama o construtor da classe base PowerUp.
        self.duration = 10 # Define a duração do power-up em segundos.

    def update(self, game_speed): # Atualiza o estado do escudo a cada quadro.
        # Move o escudo para a esquerda com a velocidade do jogo.
        self.rect.x -= game_speed

    def draw(self, screen): # Desenha o escudo na tela.
        screen.blit(self.image, self.rect) # Desenha a imagem do escudo na sua posição atual.
