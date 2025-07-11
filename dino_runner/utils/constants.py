# dino_runner/utils/constants.py
import pygame
import os
import sys
from dino_runner.utils.resource_manager import resource_path # Importa resource_path

# Global Constants
TITLE = "Chrome Dino Runner"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
FPS = 60

# Nível do chão para alinhar obstáculos (ajustado para a base do dinossauro)
GROUND_LEVEL_Y = 404 # Aprox. onde os pés do dinossauro estão quando correndo (310 + altura do dino ~94)

# Inicializa todas as variáveis de assets para None ou listas vazias
# para evitar NameError/ImportError antes do carregamento
ICON = None
RUNNING = []
RUNNING_SHIELD = []
RUNNING_HAMMER = []
JUMPING = None
JUMPING_SHIELD = None
JUMPING_HAMMER = None
DUCKING = []
DUCKING_SHIELD = []
DUCKING_HAMMER = []
SMALL_CACTUS = []
LARGE_CACTUS = []
BIRD = []
CLOUD = None
SHIELD = None
HAMMER = None
BG = None
HEART = None
POWERUP_SOUND = None # Variável para o som do power-up
POINT_SOUND = None # Variável para o som de 100 pontos

try:
    # Carregamento de Assets usando resource_path
    # O caminho relativo para resource_path deve ser a partir da raiz do pacote dino_runner
    # Ex: "dino_runner/assets/DinoWallpaper.png"
    
    # ICON
    icon_path = resource_path("dino_runner/assets/DinoWallpaper.png")
    print(f"DEBUG (constants.py): Carregando ICON de: {icon_path}") # Debug
    ICON = pygame.image.load(icon_path)

    # Dino
    RUNNING = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun1.png")),
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun2.png")),
    ]
    RUNNING_SHIELD = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun1Shield.png")),
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun2.png")),
    ]
    RUNNING_HAMMER = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1Hammer.png")),
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun2.png")),
    ]
    JUMPING = pygame.image.load(resource_path("dino_runner/assets/Dino/DinoJump.png"))
    JUMPING_SHIELD = pygame.image.load(resource_path("dino_runner/assets/Dino/DinoJumpShield.png"))
    JUMPING_HAMMER = pygame.image.load(resource_path("dino_runner/assets/Dino/DinoJumpHammer.png"))
    DUCKING = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1.png")),
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck2.png")),
    ]
    DUCKING_SHIELD = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1Shield.png")),
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck2.png")),
    ]
    DUCKING_HAMMER = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1Hammer.png")),
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck2.png")),
    ]

    # Cactus
    SMALL_CACTUS = [
        pygame.image.load(resource_path("dino_runner/assets/Cactus/SmallCactus1.png")),
        pygame.image.load(resource_path("dino_runner/assets/Cactus/SmallCactus2.png")),
        pygame.image.load(resource_path("dino_runner/assets/Cactus/SmallCactus3.png")),
    ]
    LARGE_CACTUS = [
        pygame.image.load(resource_path("dino_runner/assets/Cactus/LargeCactus1.png")),
        pygame.image.load(resource_path("dino_runner/assets/Cactus/LargeCactus2.png")),
        pygame.image.load(resource_path("dino_runner/assets/Cactus/LargeCactus3.png")),
    ]

    # Bird
    BIRD = [
        pygame.image.load(resource_path("dino_runner/assets/Bird/Bird1.png")),
        pygame.image.load(resource_path("dino_runner/assets/Bird/Bird2.png")),
    ]

    # Other (inclui Cloud, Shield, Hammer, Track, SmallHeart)
    CLOUD = pygame.image.load(resource_path('dino_runner/assets/Other/Cloud.png'))
    SHIELD = pygame.image.load(resource_path('dino_runner/assets/Other/shield.png'))
    HAMMER = pygame.image.load(resource_path('dino_runner/assets/Other/hammer.png'))
    BG = pygame.image.load(resource_path('dino_runner/assets/Other/Track.png'))
    HEART = pygame.image.load(resource_path('dino_runner/assets/Other/SmallHeart.png'))

    # Carrega os sons
    POWERUP_SOUND = pygame.mixer.Sound(resource_path('dino_runner/assets/Other/powerup.wav'))
    POINT_SOUND = pygame.mixer.Sound(resource_path('dino_runner/assets/Other/point.wav'))


except pygame.error as e:
    print(f"Erro ao carregar asset do Pygame: {e}. Certifique-se de que os arquivos existam e os caminhos estejam corretos.")
except FileNotFoundError as e:
    print(f"Arquivo de asset não encontrado: {e}. Certifique-se de que os arquivos existam e os caminhos estejam corretos.")

DEFAULT_TYPE = "default"
SHIELD_TYPE = "shield"
HAMMER_TYPE = "hammer"

# Cores da Fonte
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
