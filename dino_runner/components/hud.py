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

    def draw(self, screen):
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
