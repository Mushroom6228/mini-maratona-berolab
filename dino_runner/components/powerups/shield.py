# dino_runner/components/powerups/shield.py
import pygame
from dino_runner.utils.constants import SHIELD, SHIELD_TYPE # Importa SHIELD e SHIELD_TYPE de constants
from dino_runner.components.powerups.powerup import PowerUp # Importa PowerUp

class Shield(PowerUp):
    def __init__(self):
        # Garante que SHIELD não seja None antes de passar para o super()
        image_to_use = SHIELD if SHIELD else pygame.Surface((30, 30), flags=pygame.SRCALPHA)
        if not SHIELD:
            image_to_use.fill((0, 0, 255)) # Placeholder azul para escudo
            print("Aviso: Imagem SHIELD não carregada. Usando placeholder em shield.py.")

        self.type = SHIELD_TYPE
        super().__init__(image_to_use, self.type)
        self.duration = 10  # segundos (Ajustado para 10 segundos)

    def update(self, game_speed, player): # Adicionado 'player' para consistência com PowerUpManager
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            # A lógica de desativar o escudo é agora tratada no PowerUpManager
            # e no Dinosaur, então esta parte pode ser simplificada ou removida
            # se não houver outra lógica específica para o escudo aqui.
            # if hasattr(player, 'has_shield'):
            #     player.has_shield = False
            pass # Não faz nada aqui, pois o PowerUpManager lida com a remoção

    def draw(self, screen):
        screen.blit(self.image, self.rect)
