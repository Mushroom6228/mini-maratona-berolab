<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
from dino_runner.utils.constants import SCREEN_WIDTH, HEART # Importa constantes como a largura da tela e a imagem do coração (vidas).

class HUD:
    # O construtor recebe uma função para obter o número atual de vidas do jogador.
    def __init__(self, get_lives_func):
        self.get_lives_func = get_lives_func # Armazena a função para acessar as vidas.
        try:
            self.font = pygame.font.Font(None, 28) # Tenta carregar a fonte padrão do Pygame com tamanho 28.
        except pygame.error: # Se ocorrer um erro ao carregar a fonte padrão.
            self.font = pygame.font.SysFont("Arial", 28) # Usa uma fonte de sistema como fallback (Arial).
=======
# dino_runner/components/hud.py
import pygame
from dino_runner.utils.constants import SCREEN_WIDTH, HEART # Importa HEART

class HUD:
    def __init__(self, get_lives_func):
        self.get_lives_func = get_lives_func
        try:
            self.font = pygame.font.Font(None, 28)
        except pygame.error:
            print("Aviso: Fonte padrão do Pygame não encontrada. Usando fonte genérica.")
            self.font = pygame.font.SysFont("Arial", 28)

        self.heart_image = HEART # Usa a imagem HEART importada de constants.py
        if self.heart_image:
            self.heart_image = pygame.transform.scale(self.heart_image, (30, 30)) # Redimensiona o coração para 30x30
        else:
            print("Aviso: Imagem do coração (HEART) não carregada. Usando placeholder.")
            self.heart_image = pygame.Surface((30, 30)) # Placeholder de 30x30
            self.heart_image.fill((255, 0, 0)) # Cor vermelha para placeholder
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

        self.heart_image = HEART # Atribui a imagem do coração importada das constantes.
        if self.heart_image: # Verifica se a imagem do coração foi carregada com sucesso.
            # Redimensiona a imagem do coração para 30x30 pixels.
            self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        else:
            # Se a imagem do coração não foi carregada, cria uma superfície de placeholder vermelha.
            self.heart_image = pygame.Surface((30, 30)) # Cria uma superfície vazia de 30x30.
            self.heart_image.fill((255, 0, 0)) # Preenche a superfície com a cor vermelha.

    # Desenha os elementos do HUD na tela.
    def draw(self, screen):
<<<<<<< HEAD
        lives = self.get_lives_func() # Obtém o número atual de vidas chamando a função passada no construtor.
        if self.heart_image: # Se a imagem do coração estiver disponível.
            for i in range(lives): # Itera para desenhar um coração para cada vida.
                # Desenha a imagem do coração na tela, posicionando-a com um pequeno espaçamento.
                screen.blit(self.heart_image, (10 + i * 35, 10))
        else:
            # Se a imagem do coração não estiver disponível, desenha o número de vidas como texto.
            lives_text = self.font.render(f'Lives: {lives}', True, (0, 0, 0)) # Renderiza o texto "Lives: X" em preto.
            screen.blit(lives_text, (10, 10)) # Desenha o texto na tela.
=======
        lives = self.get_lives_func()
        if self.heart_image:
            for i in range(lives):
                screen.blit(self.heart_image, (10 + i * 35, 10)) # Ajusta a posição para o novo tamanho
        else:
            # Fallback textual se a imagem do coração não carregar
            lives_text = self.font.render(f'Lives: {lives}', True, (0, 0, 0))
            screen.blit(lives_text, (10, 10))

        # O status dos power-ups é desenhado diretamente no dinossauro ou em outro lugar,
        # então não é necessário aqui no HUD (a menos que você queira um indicador textual).
        # Se quiser adicionar, precisará passar o objeto player para o HUD.
        # Por enquanto, removido para simplificar com base na sua estrutura de código.
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
