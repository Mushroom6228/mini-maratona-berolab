# dino_runner/components/obstacles/cactus.py
import pygame
import random
# Importa LARGE_CACTUS, SMALL_CACTUS e a nova constante GROUND_LEVEL_Y
from dino_runner.utils.constants import SCREEN_WIDTH, LARGE_CACTUS, SMALL_CACTUS, GROUND_LEVEL_Y
from dino_runner.components.obstacles.obstacle import Obstacle # Importa a classe base Obstacle

# Classe Cactus
class Cactus(Obstacle):
    def __init__(self):
        # Escolhe entre cactos grandes ou pequenos
        # Garante que as listas LARGE_CACTUS e SMALL_CACTUS não estejam vazias
        if random.randint(0, 1) == 0:
            # Se LARGE_CACTUS for uma lista vazia, usa SMALL_CACTUS como fallback
            cactus_source_list = LARGE_CACTUS if LARGE_CACTUS else SMALL_CACTUS
        else:
            # Se SMALL_CACTUS for uma lista vazia, usa LARGE_CACTUS como fallback
            cactus_source_list = SMALL_CACTUS if SMALL_CACTUS else LARGE_CACTUS
        
        # Se após o fallback a lista de origem ainda estiver vazia (nenhuma imagem de cacto carregada)
        if not cactus_source_list:
            print("Aviso: Nenhuma imagem de cacto disponível. Usando placeholder genérico.")
            selected_image = pygame.Surface((30, 30), flags=pygame.SRCALPHA)
            selected_image.fill((255, 0, 255)) # Cor magenta para placeholder
        else:
            # Escolhe UMA imagem (objeto Surface) aleatoriamente da lista selecionada
            selected_image = random.choice(cactus_source_list)

        # Passa a única imagem selecionada para o construtor da classe Obstacle.
        # O construtor de Obstacle irá envolvê-la em uma lista se for uma única imagem.
        super().__init__(selected_image, 0)
        
        # CORREÇÃO: Ajusta a posição Y para alinhar a base do cacto com o nível do chão
        self.rect.y = GROUND_LEVEL_Y - self.rect.height
