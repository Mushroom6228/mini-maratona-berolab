# dino_runner/components/powerups/hammer.py
import pygame
from dino_runner.utils.constants import HAMMER # Importa HAMMER de constants
from dino_runner.components.powerups.powerup import PowerUp # Importa PowerUp

class Hammer(PowerUp):
    def __init__(self):
        # Garante que HAMMER não seja None antes de passar para o super()
        image_to_use = HAMMER if HAMMER else pygame.Surface((30, 30), flags=pygame.SRCALPHA)
        if not HAMMER:
            image_to_use.fill((255, 165, 0)) # Placeholder laranja para martelo
            print("Aviso: Imagem HAMMER não carregada. Usando placeholder em hammer.py.")

        self.type = "hammer"
        super().__init__(image_to_use, self.type)
        self.duration = 10  # segundos (Ajustado para 10 segundos)

    def update(self, game_speed, player): # Adicionado 'player' para consistência com PowerUpManager
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # A lógica de desativar o martelo é agora tratada no PowerUpManager
            # e no Dinosaur, então esta parte pode ser simplificada ou removida
            # se não houver outra lógica específica para o martelo aqui.
            # if hasattr(player, 'has_hammer'):
            #     player.has_hammer = False
            pass # Não faz nada aqui, pois o PowerUpManager lida com a remoção

    def draw(self, screen):
        screen.blit(self.image, self.rect)
