<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
from dino_runner.utils.constants import SCREEN_WIDTH # Importa a constante SCREEN_WIDTH (largura da tela).

class Obstacle:
    # O construtor recebe a imagem do obstáculo e o tipo do obstáculo.
    def __init__(self, image, type):
        # Verifica se a imagem fornecida é uma lista e não está vazia.
        if isinstance(image, list) and image:
            self.image = image # Atribui a lista de imagens ao obstáculo.
            self.rect = self.image[0].get_rect() # Obtém o retângulo da primeira imagem da lista.
        # Verifica se a imagem não é uma lista, mas é um objeto de imagem válido (não None).
        elif not isinstance(image, list) and image is not None:
            self.image = [image] # Converte a imagem única em uma lista para consistência.
            self.rect = image.get_rect() # Obtém o retângulo da imagem.
        else:
            # Fallback: Se a imagem for inválida ou vazia, cria uma superfície de placeholder magenta.
            self.image = [pygame.Surface((30, 30))] # Cria uma lista com uma superfície vazia de 30x30 pixels.
            self.image[0].fill((255, 0, 255)) # Preenche a superfície com a cor magenta.
            self.rect = self.image[0].get_rect() # Obtém o retângulo do placeholder.
        self.type = type # Define o tipo do obstáculo (ex: 0 para cacto, 1 para pássaro).
        self.rect.x = SCREEN_WIDTH # Define a posição X inicial do obstáculo, fora da tela à direita.

    # Atualiza o estado do obstáculo a cada quadro.
    # O parâmetro 'obstacles' não é usado nesta classe base, mas é mantido para compatibilidade com subclasses.
    def update(self, game_speed, obstacles=None):
        self.rect.x -= game_speed # Move o obstáculo para a esquerda com a velocidade do jogo.
=======
# dino_runner/components/obstacles/obstacle.py
import pygame
from dino_runner.utils.constants import SCREEN_WIDTH

class Obstacle:
    def __init__(self, image, type):
        # Garante que a imagem seja uma lista e não esteja vazia
        if isinstance(image, list) and image:
            self.image = image
            self.rect = self.image[0].get_rect()
        elif not isinstance(image, list) and image is not None: # Se for uma única imagem (e não None)
            self.image = [image] # Converte para lista para consistência
            self.rect = image.get_rect()
        else: # Fallback para imagem vazia ou None
            print(f"Aviso: Imagem de obstáculo inválida ou vazia para tipo {type}. Usando placeholder.")
            self.image = [pygame.Surface((30, 30))] # Placeholder
            self.image[0].fill((255, 0, 255)) # Cor magenta para fácil identificação
            self.rect = self.image[0].get_rect()

        self.type = type
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles=None):
        self.rect.x -= game_speed
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

    # Desenha o obstáculo na tela.
    def draw(self, screen):
<<<<<<< HEAD
        screen.blit(self.image[0], self.rect) # Desenha a primeira imagem da lista do obstáculo na sua posição atual.
=======
        screen.blit(self.image[0], self.rect)
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
