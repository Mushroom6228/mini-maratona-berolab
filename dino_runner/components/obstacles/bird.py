import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import random # Importa o módulo random para gerar números aleatórios.
from dino_runner.utils.constants import BIRD # Importa a constante BIRD (lista de imagens de pássaros).
from dino_runner.components.obstacles.obstacle import Obstacle # Importa a classe base Obstacle.

class Bird(Obstacle):
    def __init__(self):
        # Define as imagens do pássaro.
        # Se a constante BIRD (lista de imagens carregadas) não for vazia, usa-a.
        # Caso contrário, cria uma lista com uma superfície de placeholder magenta.
        bird_images = BIRD if BIRD else [pygame.Surface((30, 30), flags=pygame.SRCALPHA)]
        if not bird_images[0]: # Se o placeholder for vazio (caso BIRD seja vazio e o placeholder não tenha sido preenchido).
            bird_images[0].fill((255, 0, 255)) # Preenche o placeholder com a cor magenta.
        super().__init__(bird_images, 1) # Chama o construtor da classe base Obstacle, passando as imagens e o tipo (1 para pássaro).
        # Define a posição Y inicial aleatória do pássaro, escolhendo entre três alturas.
        self.rect.y = random.choice([250, 280, 310])
        self.index = 0 # Índice para controlar a animação do pássaro (batida de asas).
        # Inicializa a imagem a ser desenhada, usando a primeira imagem da animação.
        self.image_to_draw = self.image[self.index // 5] if self.image else bird_images[0]

    def update(self, game_speed, obstacles=None): # Atualiza o estado do pássaro a cada quadro.
        super().update(game_speed) # Chama o método update da classe base Obstacle para mover o pássaro.
        # Anima as asas do pássaro.
        # Se o índice atingir o final da animação (com base no número de imagens * 5 para desacelerar a animação).
        if self.image and self.index >= (len(self.image) * 5) -1:
            self.index = 0 # Reinicia o índice da animação.
        # Garante que self.image não esteja vazio antes de tentar acessar.
        if self.image:
            self.image_to_draw = self.image[self.index // 5] # Define a imagem atual a ser desenhada para a animação.
        else:
            # Fallback: Se as imagens não existirem, usa uma superfície de placeholder.
            self.image_to_draw = pygame.Surface((30, 30))
            self.image_to_draw.fill((255, 0, 255)) # Preenche o placeholder com magenta.
        self.index += 1 # Incrementa o índice da animação.

    def draw(self, screen): # Desenha o pássaro na tela.
        screen.blit(self.image_to_draw, self.rect) # Desenha a imagem atual do pássaro na sua posição.
