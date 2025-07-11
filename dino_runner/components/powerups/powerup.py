import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import random # Importa o módulo random para gerar números aleatórios.
from dino_runner.utils.constants import SCREEN_WIDTH # Importa a constante SCREEN_WIDTH (largura da tela).

class PowerUp:
    # O construtor recebe a imagem do power-up e o tipo do power-up.
    def __init__(self, image, type):
        if image: # Verifica se uma imagem foi fornecida.
            self.image = image # Atribui a imagem fornecida ao power-up.
            self.rect = self.image.get_rect() # Obtém o retângulo que envolve a imagem do power-up.
        else:
            # Fallback: Se nenhuma imagem for fornecida, cria uma superfície de placeholder ciano.
            self.image = pygame.Surface((30, 30)) # Cria uma superfície vazia de 30x30 pixels.
            self.image.fill((0, 255, 255)) # Preenche a superfície com a cor ciano.
            self.rect = self.image.get_rect() # Obtém o retângulo do placeholder.
        self.type = type # Define o tipo do power-up (ex: "shield", "hammer").
        self.rect.x = SCREEN_WIDTH # Define a posição X inicial do power-up, fora da tela à direita.
        self.rect.y = random.randint(200, 300) # Define a posição Y inicial aleatória do power-up, em uma altura razoável.

    # Atualiza o estado do power-up a cada quadro.
    def update(self, game_speed):
        self.rect.x -= game_speed # Move o power-up para a esquerda com a velocidade do jogo.

    # Desenha o power-up na tela.
    def draw(self, screen):
        screen.blit(self.image, self.rect) # Desenha a imagem do power-up na sua posição atual.
