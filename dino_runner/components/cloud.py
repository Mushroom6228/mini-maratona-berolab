import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import random # Importa o módulo random para gerar números aleatórios.
# Importa constantes como a imagem da nuvem, largura/altura da tela e a posição do chão.
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_LEVEL_Y

class Cloud:
    def __init__(self):
        if CLOUD: # Verifica se a imagem da nuvem foi carregada com sucesso.
            self.image = CLOUD # Atribui a imagem da nuvem.
            self.rect = self.image.get_rect() # Obtém o retângulo que envolve a imagem da nuvem.
        else:
            # Fallback: Se a imagem da nuvem não foi carregada, cria uma superfície de placeholder.
            self.image = pygame.Surface((50, 20)) # Cria uma superfície vazia de 50x20 pixels.
            self.image.fill((200, 200, 200)) # Preenche a superfície com a cor cinza.
            self.rect = self.image.get_rect() # Obtém o retângulo do placeholder.
        # Define a posição X inicial da nuvem, fora da tela à direita, com uma variação.
        self.rect.x = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH * 2)
        # Define a posição Y inicial da nuvem, escolhendo aleatoriamente entre três alturas.
        self.rect.y = random.choice([70, 100, 130])

    def update(self, game_speed): # Atualiza o estado da nuvem a cada quadro.
        # Move a nuvem para a esquerda. A velocidade é uma fração da velocidade do jogo, garantindo que ela se mova mais lentamente.
        # 'max(1, ...)' garante que a nuvem sempre se mova pelo menos 1 pixel, mesmo em velocidades de jogo muito baixas.
        self.rect.x -= max(1, game_speed // 4)
        if self.rect.right < 0: # Se a nuvem saiu completamente da tela à esquerda.
            # Reposiciona a nuvem fora da tela à direita, com uma nova variação aleatória.
            self.rect.x = SCREEN_WIDTH + random.randint(200, 600)
            # Define uma nova posição Y aleatória para a nuvem.
            self.rect.y = random.choice([70, 100, 130])

    def draw(self, screen): # Desenha a nuvem na tela.
        screen.blit(self.image, self.rect) # Desenha a imagem da nuvem na sua posição atual.
