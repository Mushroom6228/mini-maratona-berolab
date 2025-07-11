import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
from dino_runner.utils.constants import HAMMER # Importa a constante HAMMER (imagem do martelo).
from dino_runner.components.powerups.powerup import PowerUp # Importa a classe base PowerUp.

class Hammer(PowerUp):
    def __init__(self):
        # Define a imagem a ser usada para o martelo.
        # Se a constante HAMMER (imagem carregada) não for None, usa-a.
        # Caso contrário, cria uma superfície de placeholder laranja.
        image_to_use = HAMMER if HAMMER else pygame.Surface((30, 30), flags=pygame.SRCALPHA)
        if not HAMMER: # Se a imagem HAMMER não foi carregada.
            image_to_use.fill((255, 165, 0)) # Preenche o placeholder com a cor laranja.
        self.type = "hammer" # Define o tipo do power-up como "hammer".
        super().__init__(image_to_use, self.type) # Chama o construtor da classe base PowerUp.
        self.duration = 10 # Define a duração do power-up em segundos.

    def update(self, game_speed, player): # Atualiza o estado do martelo a cada quadro.
        # Move o martelo para a esquerda com a velocidade do jogo.
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width: # Se o martelo saiu completamente da tela à esquerda.
            pass # Nenhuma ação específica é necessária aqui, a remoção é tratada pelo PowerUpManager.

    def draw(self, screen): # Desenha o martelo na tela.
        screen.blit(self.image, self.rect) # Desenha a imagem do martelo na sua posição atual.
