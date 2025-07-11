<<<<<<< HEAD
import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import random # Importa o módulo random para gerar números aleatórios.
# Importa constantes como a largura da tela, listas de imagens de cactos (grandes e pequenos) e a posição do chão.
from dino_runner.utils.constants import SCREEN_WIDTH, LARGE_CACTUS, SMALL_CACTUS, GROUND_LEVEL_Y
from dino_runner.components.obstacles.obstacle import Obstacle # Importa a classe base Obstacle.
=======
# dino_runner/components/obstacles/cactus.py
import pygame
import random
# Importa LARGE_CACTUS, SMALL_CACTUS e a nova constante GROUND_LEVEL_Y
from dino_runner.utils.constants import SCREEN_WIDTH, LARGE_CACTUS, SMALL_CACTUS, GROUND_LEVEL_Y
from dino_runner.components.obstacles.obstacle import Obstacle # Importa a classe base Obstacle
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82

# Classe Cactus
class Cactus(Obstacle):
    def __init__(self):
<<<<<<< HEAD
        # Escolhe aleatoriamente entre um cacto grande ou um cacto pequeno.
        if random.randint(0, 1) == 0:
            # Se a escolha for 0, tenta usar a lista de cactos grandes. Se estiver vazia, usa a de cactos pequenos como fallback.
            cactus_source_list = LARGE_CACTUS if LARGE_CACTUS else SMALL_CACTUS
        else:
            # Se a escolha for 1, tenta usar a lista de cactos pequenos. Se estiver vazia, usa a de cactos grandes como fallback.
            cactus_source_list = SMALL_CACTUS if SMALL_CACTUS else LARGE_CACTUS
        
        if not cactus_source_list: # Se, após os fallbacks, a lista de origem ainda estiver vazia (nenhuma imagem de cacto carregada).
            # Cria uma superfície de placeholder magenta como imagem selecionada.
            selected_image = pygame.Surface((30, 30), flags=pygame.SRCALPHA)
            selected_image.fill((255, 0, 255)) # Preenche o placeholder com a cor magenta.
        else:
            # Escolhe UMA imagem (objeto Surface) aleatoriamente da lista de cactos selecionada.
            selected_image = random.choice(cactus_source_list)
        
        # Chama o construtor da classe base Obstacle, passando a imagem selecionada e o tipo (0 para cacto).
        # O construtor de Obstacle irá garantir que 'selected_image' seja tratado como uma lista.
        super().__init__(selected_image, 0)
        
        # Ajusta a posição Y do retângulo do cacto para que sua base esteja alinhada com o nível do chão.
=======
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
>>>>>>> be73f1d8742b9414b87a1ef857da4e48644b5e82
        self.rect.y = GROUND_LEVEL_Y - self.rect.height
