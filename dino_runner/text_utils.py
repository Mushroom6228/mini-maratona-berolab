<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame para desenvolvimento de jogos.
import os # Importa o módulo os para interagir com o sistema operacional (caminhos de arquivo).
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH # Importa constantes de altura e largura da tela.
from dino_runner.utils.resource_manager import resource_path # Importa a função para gerenciar caminhos de recursos.

FONT_COLOR = (0, 0, 0) # Define a cor padrão da fonte como preto (RGB).
FONT_SIZE = 20 # Define o tamanho padrão da fonte.
FONT_STYLE = resource_path('dino_runner/assets/Font/joystix monospace.otf') # Define o caminho para o arquivo da fonte usando resource_path.


def draw_message_component(
    message, # O texto da mensagem a ser exibida.
    screen, # A superfície da tela onde a mensagem será desenhada.
    font_color=FONT_COLOR, # A cor da fonte (usa a cor padrão se não for especificada).
    font_size=FONT_SIZE, # O tamanho da fonte (usa o tamanho padrão se não for especificado).
    pos_y_center=SCREEN_HEIGHT // 2, # A posição Y central da mensagem (usa o centro da tela se não for especificada).
    pos_x_center=SCREEN_WIDTH // 2 # A posição X central da mensagem (usa o centro da tela se não for especificada).
):
    try:
        font = pygame.font.Font(FONT_STYLE, font_size) # Tenta carregar a fonte personalizada com o tamanho especificado.
    except FileNotFoundError: # Se o arquivo da fonte não for encontrado.
        font = pygame.font.Font(None, font_size) # Usa a fonte padrão do Pygame como fallback.
    except pygame.error: # Se ocorrer um erro específico do Pygame ao carregar a fonte.
        font = pygame.font.Font(None, font_size) # Usa a fonte padrão do Pygame como fallback.
    text = font.render(message, True, font_color) # Renderiza o texto na superfície, com antialiasing (True) e a cor da fonte.
    text_rect = text.get_rect() # Obtém o retângulo que envolve a superfície do texto.
    text_rect.center = (pos_x_center, pos_y_center) # Centraliza o retângulo do texto nas posições X e Y especificadas.
    screen.blit(text, text_rect) # Desenha a superfície do texto na tela na posição do retângulo.
=======
# dino_runner/utils/text_utils.py
import pygame
import os
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from dino_runner.utils.resource_manager import resource_path # Importa resource_path

FONT_COLOR = (0, 0, 0)
FONT_SIZE = 20 # Ajustado para o mesmo tamanho do high score
# O caminho da fonte agora usa resource_path
FONT_STYLE = resource_path('dino_runner/assets/Font/joystix monospace.otf')

print(f"DEBUG (text_utils.py): FONT_STYLE definido como: {FONT_STYLE}") # Debug


def draw_message_component(
    message,
    screen,
    font_color=FONT_COLOR,
    font_size=FONT_SIZE, # Usa o FONT_SIZE padrão (20)
    pos_y_center=SCREEN_HEIGHT // 2,
    pos_x_center=SCREEN_WIDTH // 2
):
    # Tenta carregar a fonte. Se falhar, usa a fonte padrão do Pygame.
    try:
        font = pygame.font.Font(FONT_STYLE, font_size)
    except FileNotFoundError:
        print(f"Aviso: Fonte '{FONT_STYLE}' não encontrada. Usando fonte padrão do Pygame.")
        font = pygame.font.Font(None, font_size) # Fallback para fonte padrão
    except pygame.error as e:
        print(f"Erro ao carregar fonte '{FONT_STYLE}': {e}. Usando fonte padrão do Pygame.")
        font = pygame.font.Font(None, font_size) # Fallback para fonte padrão
    
    text = font.render(message, True, font_color)
    text_rect = text.get_rect()
    text_rect.center = (pos_x_center, pos_y_center)
    screen.blit(text, text_rect)
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
