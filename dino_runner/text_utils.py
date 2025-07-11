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
