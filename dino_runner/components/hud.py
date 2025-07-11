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
        lives = self.get_lives_func() # Obtém o número atual de vidas chamando a função passada no construtor.
        if self.heart_image: # Se a imagem do coração estiver disponível.
            for i in range(lives): # Itera para desenhar um coração para cada vida.
                # Desenha a imagem do coração na tela, posicionando-a com um pequeno espaçamento.
                screen.blit(self.heart_image, (10 + i * 35, 10))
        else:
            # Se a imagem do coração não estiver disponível, desenha o número de vidas como texto.
            lives_text = self.font.render(f'Lives: {lives}', True, (0, 0, 0)) # Renderiza o texto "Lives: X" em preto.
            screen.blit(lives_text, (10, 10)) # Desenha o texto na tela.
