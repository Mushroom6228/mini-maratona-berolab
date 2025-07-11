import pygame # Importa a biblioteca Pygame, essencial para o desenvolvimento de jogos.
import os # Importa o módulo os para interagir com o sistema operacional, como manipulação de caminhos de arquivo.
from dino_runner.utils.resource_manager import resource_path # Importa a função 'resource_path' para carregar recursos de forma compatível com executáveis.

TITLE = "Chrome Dino Runner" # Define o título da janela do jogo.
SCREEN_HEIGHT = 600 # Define a altura da tela do jogo em pixels.
SCREEN_WIDTH = 1100 # Define a largura da tela do jogo em pixels.
FPS = 60 # Define a taxa de quadros por segundo (Frames Per Second) do jogo.
GROUND_LEVEL_Y = 404 # Define a coordenada Y do "chão" para o alinhamento de objetos.

# Inicializa todas as variáveis de ativos como None ou listas vazias.
# Isso evita erros de 'NameError' ou 'ImportError' caso os ativos não sejam carregados.
ICON = None # Variável para o ícone da janela do jogo.
RUNNING = [] # Lista para as imagens de animação do dinossauro correndo.
RUNNING_SHIELD = [] # Lista para as imagens de animação do dinossauro correndo com escudo.
RUNNING_HAMMER = [] # Lista para as imagens de animação do dinossauro correndo com martelo.
JUMPING = None # Variável para a imagem do dinossauro pulando.
JUMPING_SHIELD = None # Variável para a imagem do dinossauro pulando com escudo.
JUMPING_HAMMER = None # Variável para a imagem do dinossauro pulando com martelo.
DUCKING = [] # Lista para as imagens de animação do dinossauro abaixando.
DUCKING_SHIELD = [] # Lista para as imagens de animação do dinossauro abaixando com escudo.
DUCKING_HAMMER = [] # Lista para as imagens de animação do dinossauro abaixando com martelo.
SMALL_CACTUS = [] # Lista para as imagens de cactos pequenos.
LARGE_CACTUS = [] # Lista para as imagens de cactos grandes.
BIRD = [] # Lista para as imagens de animação do pássaro.
CLOUD = None # Variável para a imagem da nuvem.
SHIELD = None # Variável para a imagem do power-up de escudo.
HAMMER = None # Variável para a imagem do power-up de martelo.
BG = None # Variável para a imagem de fundo (pista).
HEART = None # Variável para a imagem do coração (vidas).
POWERUP_SOUND = None # Variável para o som de coleta de power-up.
POINT_SOUND = None # Variável para o som de ganho de pontos (a cada 100 pontos).

try:
    # Carregamento de ativos usando a função 'resource_path'.
    # O caminho relativo para 'resource_path' deve ser a partir da raiz do pacote 'dino_runner'.
    
    # Ícone da janela
    icon_path = resource_path("dino_runner/assets/DinoWallpaper.png")
    ICON = pygame.image.load(icon_path) # Carrega a imagem para o ícone.

    # Imagens do Dinossauro
    RUNNING = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun1.png")), # Carrega a primeira imagem do dinossauro correndo.
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun2.png")), # Carrega a segunda imagem do dinossauro correndo.
    ]
    RUNNING_SHIELD = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun1Shield.png")), # Carrega a primeira imagem do dinossauro correndo com escudo.
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun2.png")), # Carrega a segunda imagem do dinossauro correndo com escudo.
    ]
    RUNNING_HAMMER = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1Hammer.png")), # Carrega a primeira imagem do dinossauro correndo com martelo.
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoRun2.png")), # Carrega a segunda imagem do dinossauro correndo com martelo.
    ]
    JUMPING = pygame.image.load(resource_path("dino_runner/assets/Dino/DinoJump.png")) # Carrega a imagem do dinossauro pulando.
    JUMPING_SHIELD = pygame.image.load(resource_path("dino_runner/assets/Dino/DinoJumpShield.png")) # Carrega a imagem do dinossauro pulando com escudo.
    JUMPING_HAMMER = pygame.image.load(resource_path("dino_runner/assets/Dino/DinoJumpHammer.png")) # Carrega a imagem do dinossauro pulando com martelo.
    DUCKING = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1.png")), # Carrega a primeira imagem do dinossauro abaixando.
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck2.png")), # Carrega a segunda imagem do dinossauro abaixando.
    ]
    DUCKING_SHIELD = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1Shield.png")), # Carrega a primeira imagem do dinossauro abaixando com escudo.
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck2.png")), # Carrega a segunda imagem do dinossauro abaixando com escudo.
    ]
    DUCKING_HAMMER = [
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck1Hammer.png")), # Carrega a primeira imagem do dinossauro abaixando com martelo.
        pygame.image.load(resource_path("dino_runner/assets/Dino/DinoDuck2.png")), # Carrega a segunda imagem do dinossauro abaixando com martelo.
    ]

    # Imagens de Cactos
    SMALL_CACTUS = [
        pygame.image.load(resource_path("dino_runner/assets/Cactus/SmallCactus1.png")), # Carrega a primeira imagem de cacto pequeno.
        pygame.image.load(resource_path("dino_runner/assets/Cactus/SmallCactus2.png")), # Carrega a segunda imagem de cacto pequeno.
        pygame.image.load(resource_path("dino_runner/assets/Cactus/SmallCactus3.png")), # Carrega a terceira imagem de cacto pequeno.
    ]
    LARGE_CACTUS = [
        pygame.image.load(resource_path("dino_runner/assets/Cactus/LargeCactus1.png")), # Carrega a primeira imagem de cacto grande.
        pygame.image.load(resource_path("dino_runner/assets/Cactus/LargeCactus2.png")), # Carrega a segunda imagem de cacto grande.
        pygame.image.load(resource_path("dino_runner/assets/Cactus/LargeCactus3.png")), # Carrega a terceira imagem de cacto grande.
    ]

    # Imagens de Pássaros
    BIRD = [
        pygame.image.load(resource_path("dino_runner/assets/Bird/Bird1.png")), # Carrega a primeira imagem do pássaro.
        pygame.image.load(resource_path("dino_runner/assets/Bird/Bird2.png")), # Carrega a segunda imagem do pássaro.
    ]

    # Outras Imagens e Sons
    CLOUD = pygame.image.load(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'Cloud.png'))) # Carrega a imagem da nuvem.
    SHIELD = pygame.image.load(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'shield.png'))) # Carrega a imagem do escudo.
    HAMMER = pygame.image.load(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'hammer.png'))) # Carrega a imagem do martelo.
    BG = pygame.image.load(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'Track.png'))) # Carrega a imagem de fundo da pista.
    HEART = pygame.image.load(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'SmallHeart.png'))) # Carrega a imagem do coração.
    POWERUP_SOUND = pygame.mixer.Sound(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'upgrade.wav'))) # Carrega o som de power-up.
    POINT_SOUND = pygame.mixer.Sound(resource_path(os.path.join('dino_runner', 'assets', 'Other', 'point.wav'))) # Carrega o som de ponto.
    POINT_SOUND.set_volume(0.7) # Define o volume do som de ponto para 70%.

except pygame.error as e: # Captura erros específicos do Pygame durante o carregamento de ativos.
    pass # Ignora o erro, permitindo que o programa continue (com ativos None).
except FileNotFoundError as e: # Captura erros de arquivo não encontrado.
    pass # Ignora o erro, permitindo que o programa continue (com ativos None).

DEFAULT_TYPE = "default" # Define uma constante para o tipo de dinossauro padrão.
SHIELD_TYPE = "shield" # Define uma constante para o tipo de power-up de escudo.
HAMMER_TYPE = "hammer" # Define uma constante para o tipo de power-up de martelo.

# Cores da Fonte (RGB)
BLACK = (0, 0, 0) # Define a cor preta.
WHITE = (255, 255, 255) # Define a cor branca.
