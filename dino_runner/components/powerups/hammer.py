<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
from dino_runner.utils.constants import HAMMER # Importa a constante HAMMER (imagem do martelo).
from dino_runner.components.powerups.powerup import PowerUp # Importa a classe base PowerUp.

class Hammer(PowerUp):
    def __init__(self):
        # Define a imagem a ser usada para o martelo.
        # Se a constante HAMMER (imagem carregada) não for None, usa-a.
        # Caso contrário, cria uma superfície de placeholder laranja.
        image_to_use = HAMMER if HAMMER else pygame.Surface((30, 30), flags=pygame.SRCALPHA)
        if not HAMMER: # Se a imagem HAMMER não foi carregada.
            image_to_use.fill((255, 165, 0)) # Preenche o placeholder com a cor laranja.
        self.type = "hammer" # Define o tipo do power-up como "hammer".
        super().__init__(image_to_use, self.type) # Chama o construtor da classe base PowerUp.
        self.duration = 10 # Define a duração do power-up em segundos.

    def update(self, game_speed, player): # Atualiza o estado do martelo a cada quadro.
        # Move o martelo para a esquerda com a velocidade do jogo.
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width: # Se o martelo saiu completamente da tela à esquerda.
            pass # Nenhuma ação específica é necessária aqui, a remoção é tratada pelo PowerUpManager.
=======
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
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

    def draw(self, screen): # Desenha o martelo na tela.
        screen.blit(self.image, self.rect) # Desenha a imagem do martelo na sua posição atual.
