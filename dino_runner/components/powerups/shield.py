<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
# Importa as constantes SHIELD (imagem do escudo) e SHIELD_TYPE (tipo do power-up).
from dino_runner.utils.constants import SHIELD, SHIELD_TYPE
from dino_runner.components.powerups.powerup import PowerUp # Importa a classe base PowerUp.

class Shield(PowerUp):
    def __init__(self):
        # Define a imagem a ser usada para o escudo.
        # Se a constante SHIELD (imagem carregada) não for None, usa-a.
        # Caso contrário, cria uma superfície de placeholder azul.
        image_to_use = SHIELD if SHIELD else pygame.Surface((30, 30), flags=pygame.SRCALPHA)
        if not SHIELD: # Se a imagem SHIELD não foi carregada.
            image_to_use.fill((0, 0, 255)) # Preenche o placeholder com a cor azul.
        self.type = SHIELD_TYPE # Define o tipo do power-up como SHIELD_TYPE.
        super().__init__(image_to_use, self.type) # Chama o construtor da classe base PowerUp.
        self.duration = 10 # Define a duração do power-up em segundos.

    def update(self, game_speed, player): # Atualiza o estado do escudo a cada quadro.
        # Move o escudo para a esquerda com a velocidade do jogo.
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width: # Se o escudo saiu completamente da tela à esquerda.
            pass # Nenhuma ação específica é necessária aqui, a remoção é tratada pelo PowerUpManager.

    def draw(self, screen): # Desenha o escudo na tela.
        screen.blit(self.image, self.rect) # Desenha a imagem do escudo na sua posição atual.
=======
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
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
