import pygame
import os
import random
from dino_runner.components.dinosaur import Dinosaur
# Tenta importar as bibliotecas cv2 (OpenCV) e numpy para o vídeo do menu.
# Se não estiverem instaladas, as variáveis cv2 e numpy serão None.
try:
    import cv2
    import numpy
except ImportError:
    cv2 = None
    numpy = None
from dino_runner.components.obstacle_manager import ObstacleManager
from dino_runner.components.powerups.powerup_manager import PowerUpManager
from dino_runner.components.cloud import Cloud
from dino_runner.components.score import Score
from dino_runner.components.hud import HUD
# Importa constantes globais do módulo constants.
from dino_runner.utils.constants import BG, ICON, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, POWERUP_SOUND
# Importa a função para desenhar mensagens na tela.
from dino_runner.text_utils import draw_message_component
# Importa a função para gerenciar caminhos de recursos (imagens, sons).
from dino_runner.utils.resource_manager import resource_path

class Game:
    def __init__(self):
        pygame.init() # Inicializa todos os módulos Pygame.
        pygame.mixer.init() # Inicializa o mixer de áudio do Pygame.
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Configura a tela do jogo.
        pygame.display.set_caption("Chrome Dino Runner") # Define o título da janela do jogo.
        # Verifica se o ícone foi carregado com sucesso antes de tentar defini-lo.
        if ICON:
            pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock() # Cria um objeto Clock para controlar a taxa de quadros.
        self.running = True # Flag para controlar se o jogo principal está rodando.
        self.playing = False # Flag para controlar se o jogo está em andamento (não no menu ou game over).
        self.game_speed = 13 # Velocidade inicial do jogo.
        self.base_game_speed = 13 # Armazena a velocidade inicial para resetar.
        self.last_speedup_time = pygame.time.get_ticks() # Tempo do último aumento de velocidade.
        self.player = Dinosaur() # Cria uma instância do dinossauro.
        self.player.game = self # Passa a referência do jogo para o dinossauro.
        self.obstacle_manager = ObstacleManager() # Cria um gerenciador de obstáculos.
        # Cria um gerenciador de power-ups, passando o som e o gerenciador de obstáculos.
        self.powerup_manager = PowerUpManager(POWERUP_SOUND, self.obstacle_manager)
        self.clouds = [] # Lista para armazenar as nuvens.
        min_cloud_distance = 150 # Distância mínima entre as nuvens para evitar sobreposição.
        # Adiciona 7 nuvens ao cenário, garantindo que não se sobreponham inicialmente.
        for _ in range(7):
            new_cloud = Cloud()
            attempts = 0
            while any(abs(new_cloud.rect.x - c.rect.x) < min_cloud_distance for c in self.clouds) and attempts < 10:
                new_cloud = Cloud()
                attempts += 1
            self.clouds.append(new_cloud)
        self.score = Score() # Cria uma instância do placar.
        self.lives = 3 # Número de vidas do jogador.
        self.high_score = self.load_high_score() # Carrega a pontuação máxima.
        self.day = True # Flag que indica se é dia (True) ou noite (False).
        self.day_night_timer = pygame.time.get_ticks() # Tempo do último ciclo dia/noite.
        self.day_night_interval = 40000 # Duração de um ciclo dia/noite (40 segundos).
        self.day_night_transition = 5000 # Duração da transição entre dia e noite (5 segundos).
        self.day_night_progress = 0 # Progresso da transição (0 para dia, 1 para noite).
        self.day_night_direction = 1 # Direção da transição (não usado diretamente, mas pode ser para fade in/out).
        self.in_transition = False # Flag que indica se uma transição dia/noite está em andamento.
        self.transition_start = 0 # Tempo de início da transição.
        self.bg_x_pos = 0 # Posição X do fundo para rolagem.
        self.bg_y_pos = 380 # Posição Y do fundo.
        self.game_over = False # Flag para controlar o estado de game over.
        self.hud = HUD(lambda: self.lives) # Cria o HUD (interface do usuário), passando uma função para obter as vidas.
        self.video = None # Variável para armazenar o objeto de vídeo do menu.
        # Tenta carregar o vídeo do menu se o cv2 estiver disponível.
        if cv2:
            video_path = resource_path('dino_runner/assets/Other/VideoMenu.mp4')
            if os.path.exists(video_path):
                self.video = cv2.VideoCapture(video_path)
        self.jump_sound = None # Variável para o som de pulo.
        self.hurt_sound = None # Variável para o som de dano.
        # Define os caminhos dos arquivos de som usando resource_path.
        jump_path = resource_path('dino_runner/assets/Other/jump.wav')
        hurt_path = resource_path('dino_runner/assets/Other/hurt.wav')
        # Carrega o som de pulo se o arquivo existir.
        if os.path.exists(jump_path):
            self.jump_sound = pygame.mixer.Sound(jump_path)
        # Carrega o som de dano e define seu volume se o arquivo existir.
        if os.path.exists(hurt_path):
            self.hurt_sound = pygame.mixer.Sound(hurt_path)
            self.hurt_sound.set_volume(1.0)
        self.upgrade_sound = None # Variável para o som de upgrade.
        # Define o caminho do arquivo de som de upgrade.
        upgrade_path = resource_path(os.path.join('dino_runner', 'assets', 'Other', 'upgrade.wav'))
        # Carrega o som de upgrade e define seu volume se o arquivo existir.
        if os.path.exists(upgrade_path):
            try:
                self.upgrade_sound = pygame.mixer.Sound(upgrade_path)
                self.upgrade_sound.set_volume(1.0)
            except Exception:
                self.upgrade_sound = None # Define como None em caso de erro.

    def load_high_score(self):
        """Carrega a pontuação máxima de um arquivo."""
        high_score_path = resource_path('highscore.txt') # Obtém o caminho do arquivo de pontuação.
        if os.path.exists(high_score_path): # Verifica se o arquivo existe.
            with open(high_score_path, 'r') as f: # Abre o arquivo para leitura.
                try:
                    return int(f.read()) # Tenta ler e converter a pontuação para inteiro.
                except ValueError:
                    return 0 # Retorna 0 se o arquivo estiver vazio ou contiver dados inválidos.
        return 0 # Retorna 0 se o arquivo não existir.

    def save_high_score(self):
        """Salva a pontuação máxima atual em um arquivo."""
        high_score_path = resource_path('highscore.txt') # Obtém o caminho do arquivo de pontuação.
        with open(high_score_path, 'w') as f: # Abre o arquivo para escrita (sobrescreve se existir).
            f.write(str(self.high_score)) # Escreve a pontuação máxima como string.

    def execute(self):
        """Loop principal do jogo, lida com os estados do jogo (menu, jogando, game over)."""
        self.playing = False # Define o estado inicial como não jogando.
        self.game_over = False # Define o estado inicial como não game over.
        while self.running: # Loop principal que mantém a janela do jogo aberta.
            if not self.playing: # Se o jogo não estiver em andamento.
                if self.game_over: # Se for game over, mostra a tela de game over.
                    self.show_game_over()
                else: # Caso contrário, mostra o menu.
                    self.show_menu()
            else: # Se o jogo estiver em andamento, executa o loop do jogo.
                self.run_game_loop()
        pygame.quit() # Encerra todos os módulos Pygame ao sair do loop principal.

    def run_game_loop(self):
        """Executa a lógica principal do jogo quando o jogo está em andamento."""
        min_cloud_distance = 150 # Distância mínima entre as nuvens ao reaparecer.
        while self.playing: # Loop enquanto o jogo está ativo.
            for event in pygame.event.get(): # Processa eventos (mouse, teclado, fechar janela).
                if event.type == pygame.QUIT: # Se o usuário fechar a janela.
                    self.playing = False # Para o loop de jogo.
                    self.running = False # Para o loop principal do jogo.
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    # Se uma tecla de pulo for pressionada e o jogador não estiver pulando.
                    if not self.player.is_jumping:
                        self.player.start_jump() # Inicia o pulo do dinossauro.
                        if self.jump_sound: # Toca o som de pulo, se disponível.
                            self.jump_sound.play()
            user_input = pygame.key.get_pressed() # Obtém o estado de todas as teclas pressionadas.
            now = pygame.time.get_ticks() # Obtém o tempo atual em milissegundos.
            # Lógica para aumentar a velocidade do jogo a cada 5 segundos.
            if now - self.last_speedup_time > 5000:
                self.game_speed += 0.5 # Aumenta a velocidade em 0.5.
                self.last_speedup_time = now # Atualiza o tempo do último aumento de velocidade.
            self.update_day_night() # Atualiza o ciclo dia/noite.
            bg_color = self.get_day_night_color() # Obtém a cor de fundo atual.
            self.screen.fill(bg_color) # Preenche a tela com a cor de fundo.
            self.draw_background() # Desenha o fundo rolante.
            # Atualiza e desenha todas as nuvens.
            for idx, cloud in enumerate(self.clouds):
                cloud.update(self.game_speed) # Atualiza a posição da nuvem.
                if cloud.rect.right < 0: # Se a nuvem saiu da tela à esquerda.
                    attempts = 0
                    while True: # Tenta reposicionar a nuvem para evitar sobreposição.
                        cloud.rect.x = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH * 2) # Reposiciona à direita.
                        max_y = 404 - cloud.rect.height - 50 # Define o limite Y máximo.
                        min_y = 20 # Define o limite Y mínimo.
                        cloud.rect.y = random.randint(min_y, max_y) # Define uma nova posição Y aleatória.
                        too_close = False
                        for j, other in enumerate(self.clouds): # Verifica a distância de outras nuvens.
                            if j != idx and abs(cloud.rect.x - other.rect.x) < min_cloud_distance:
                                too_close = True
                                break
                        if not too_close or attempts > 10: # Se não estiver muito perto ou tentou muitas vezes.
                            break
                        attempts += 1
                cloud.draw(self.screen) # Desenha a nuvem na tela.
            self.player.update(user_input) # Atualiza o estado do dinossauro com base na entrada do usuário.
            self.player.draw(self.screen) # Desenha o dinossauro na tela.
            # Atualiza os obstáculos e verifica colisões com o jogador.
            collision_detected = self.obstacle_manager.update(self.game_speed, self.player)
            if collision_detected: # Se uma colisão foi detectada.
                if not self.player.is_invincible: # Se o jogador não estiver invencível.
                    if self.hurt_sound: # Toca o som de dano, se disponível.
                        self.hurt_sound.play()
                    self.lives -= 1 # Diminui uma vida.
                    if self.lives > 0: # Se ainda tiver vidas.
                        self.player.start_invincibility(pygame.time.get_ticks()) # Inicia a invencibilidade.
                    else: # Se não tiver mais vidas.
                        self.playing = False # Para o jogo.
                        self.game_over = True # Define o estado de game over.
            if self.playing: # Se o jogo ainda estiver em andamento.
                self.obstacle_manager.draw(self.screen) # Desenha os obstáculos.
                self.powerup_manager.update(self.game_speed, self.player) # Atualiza os power-ups.
                self.powerup_manager.draw(self.screen) # Desenha os power-ups.
                self.score.update(is_night=not self.day) # Atualiza a pontuação (passa se é noite para cor).
                self.score.draw(self.screen, is_night=not self.day) # Desenha a pontuação.
                self.draw_high_score() # Desenha a pontuação máxima.
                self.hud.draw(self.screen) # Desenha o HUD.
                self.handle_powerup_timers() # Gerencia os temporizadores dos power-ups.
            pygame.display.update() # Atualiza toda a tela.
            self.clock.tick(FPS) # Limita a taxa de quadros (FPS).

    def reset_game(self):
        """Reseta todos os elementos do jogo para um novo jogo completo."""
        self.obstacle_manager.reset() # Reseta os obstáculos.
        self.powerup_manager.reset() # Reseta os power-ups.
        self.score.reset() # Reseta a pontuação.
        self.player = Dinosaur() # Cria uma nova instância do dinossauro.
        self.player.game = self # Associa o dinossauro ao jogo.
        self.hud = HUD(lambda: self.lives) # Cria um novo HUD.
        self.bg_x_pos = 0 # Reseta a posição do fundo.
        self.lives = 3 # Reseta as vidas.
        self.day = True # Define o estado inicial como dia.
        self.day_night_timer = pygame.time.get_ticks() # Reseta o temporizador dia/noite.
        self.in_transition = False # Reseta o estado de transição.
        self.day_night_progress = 0 # Reseta o progresso da transição.
        self.day_night_direction = 1 # Reseta a direção da transição.
        self.transition_start = 0 # Reseta o início da transição.
        self.game_speed = self.base_game_speed # Reseta a velocidade do jogo para a base.
        self.last_speedup_time = pygame.time.get_ticks() # Reseta o temporizador de aumento de velocidade.
        self.clouds = [] # Limpa a lista de nuvens.
        for _ in range(7): # Adiciona novas nuvens.
            self.clouds.append(Cloud())

    def draw_high_score(self):
        """Desenha a pontuação máxima na tela."""
        draw_message_component(
            f'High Score: {self.high_score}', # Texto da pontuação máxima.
            self.screen, # Superfície para desenhar.
            font_color=(200, 0, 0), # Cor da fonte (vermelho).
            font_size=20, # Tamanho da fonte.
            pos_x_center=SCREEN_WIDTH - 200, # Posição X centralizada.
            pos_y_center=18 # Posição Y centralizada.
        )
        if self.score.points > self.high_score: # Se a pontuação atual for maior que a máxima.
            self.high_score = self.score.points # Atualiza a pontuação máxima.

    def update_day_night(self):
        """Atualiza o ciclo dia/noite e a transição."""
        now = pygame.time.get_ticks() # Tempo atual.
        if not self.in_transition: # Se não estiver em transição.
            if now - self.day_night_timer > self.day_night_interval: # Se o intervalo de dia/noite passou.
                self.in_transition = True # Inicia a transição.
                self.transition_start = now # Registra o tempo de início da transição.
            self.day_night_progress = 0 if self.day else 1 # Define o progresso inicial da transição.
        else: # Se estiver em transição.
            progress = (now - self.transition_start) / self.day_night_transition # Calcula o progresso da transição (0 a 1).
            if progress >= 1: # Se a transição terminou.
                self.day = not self.day # Alterna entre dia e noite.
                self.day_night_timer = now # Reinicia o temporizador dia/noite.
                self.in_transition = False # Termina a transição.
                self.day_night_progress = 1 if not self.day else 0 # Define o progresso final.
            else: # Se a transição ainda estiver em andamento.
                if self.day: # Transicionando de dia para noite (progresso aumenta).
                    self.day_night_progress = progress
                else: # Transicionando de noite para dia (progresso diminui).
                    self.day_night_progress = 1 - progress

    def get_day_night_color(self):
        """Retorna a cor de fundo atual baseada no ciclo dia/noite."""
        day_color = (255, 255, 255) # Cor do dia (branco).
        night_color = (30, 30, 30) # Cor da noite (cinza escuro).
        p = self.day_night_progress # Progresso da transição (0 a 1).
        # Calcula a cor interpolada entre dia e noite.
        return (
            int(day_color[0] * (1-p) + night_color[0] * p),
            int(day_color[1] * (1-p) + night_color[1] * p),
            int(day_color[2] * (1-p) + night_color[2] * p)
        )

    def handle_powerup_timers(self):
        """Gerencia a duração dos power-ups ativos."""
        current_time = pygame.time.get_ticks() # Tempo atual.
        if self.player.has_shield and current_time > self.player.shield_time_up: # Se o escudo estiver ativo e o tempo acabou.
            self.player.has_shield = False # Desativa o escudo.
        if self.player.has_hammer and current_time > self.player.hammer_time_up: # Se o martelo estiver ativo e o tempo acabou.
            self.player.has_hammer = False # Desativa o martelo.

    def show_menu(self):
        """Exibe o menu principal do jogo."""
        clock = pygame.time.Clock() # Cria um Clock para o menu.
        color_anim = 0 # Variável para animação de cor do título.
        color_dir = 1 # Direção da animação de cor.
        # Define os retângulos dos botões "Entrar" e "Sair".
        button_rect = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+40, 200, 50)
        exit_rect = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+110, 200, 50)
        video_frame_surface = None # Superfície para o frame do vídeo.
        frame_count = 0 # Contador de frames para o vídeo.
        while not self.playing and self.running and not self.game_over: # Loop enquanto o menu está ativo.
            for event in pygame.event.get(): # Processa eventos.
                if event.type == pygame.QUIT: # Se o usuário fechar a janela.
                    self.running = False # Para o jogo.
                    return
                if event.type == pygame.MOUSEBUTTONDOWN: # Se um botão do mouse for clicado.
                    if button_rect.collidepoint(event.pos): # Se clicou no botão "Entrar".
                        self.reset_game() # Reseta o jogo.
                        self.playing = True # Inicia o jogo.
                        return
                    if exit_rect.collidepoint(event.pos): # Se clicou no botão "Sair".
                        self.running = False # Para o jogo.
                        return
            color_anim += color_dir # Atualiza a animação de cor.
            if color_anim > 50 or color_anim < 0: # Inverte a direção da animação.
                color_dir *= -1
            title_color = (0, 200-color_anim, 0) # Define a cor do título animada.
            if self.video: # Se o vídeo do menu estiver carregado.
                frame_count += 1
                if frame_count % 2 == 0: # Reproduz o vídeo mais lentamente.
                    ret, frame = self.video.read() # Lê um frame do vídeo.
                    if not ret: # Se o frame não foi lido (fim do vídeo).
                        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0) # Reinicia o vídeo.
                        ret, frame = self.video.read() # Lê o primeiro frame novamente.
                    if ret: # Se o frame foi lido com sucesso.
                        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Redimensiona o frame.
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converte o formato de cor.
                        video_frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1)) # Cria uma superfície Pygame.
                if video_frame_surface: # Se a superfície do frame existe.
                    self.screen.blit(video_frame_surface, (0, 0)) # Desenha o frame na tela.
                else: # Se não há frame do vídeo, preenche com branco.
                    self.screen.fill((255, 255, 255))
            else: # Se o vídeo não foi carregado, preenche com branco.
                self.screen.fill((255, 255, 255))
            # Desenha os textos do menu usando draw_message_component.
            draw_message_component('T-Rex 2.0', self.screen, font_color=title_color, font_size=80, pos_x_center=SCREEN_WIDTH//2 - 50, pos_y_center=SCREEN_HEIGHT//2-100)
            draw_message_component('Atualizado', self.screen, font_color=(100, 100, 100), font_size=36, pos_y_center=SCREEN_HEIGHT//2-40)
            draw_message_component('Free', self.screen, font_color=(255, 255, 0), font_size=36, pos_x_center=SCREEN_WIDTH//2 + 300, pos_y_center=SCREEN_HEIGHT//2-100 - 10)
            # Desenha os botões e seus textos.
            pygame.draw.rect(self.screen, (0, 200, 0), button_rect, border_radius=10)
            draw_message_component('Entrar', self.screen, font_color=(255,255,255), font_size=40, pos_x_center=button_rect.centerx, pos_y_center=button_rect.centery)
            pygame.draw.rect(self.screen, (200, 0, 0), exit_rect, border_radius=10)
            draw_message_component('Sair', self.screen, font_color=(255,255,255), font_size=40, pos_x_center=exit_rect.centerx, pos_y_center=exit_rect.centery)
            pygame.display.update() # Atualiza a tela do menu.
            clock.tick(60) # Limita a taxa de quadros do menu.

    def show_game_over(self):
        """
        Exibe a tela de Game Over, pausando o jogo no momento da morte.
        Mostra a cena exata da morte, o dinossauro morto e as opções de reset.
        """
        bg_color = self.get_day_night_color() # Obtém a cor de fundo atual.
        self.screen.fill(bg_color) # Preenche a tela com a cor de fundo.
        self.draw_background() # Desenha o fundo.
        for cloud in self.clouds: # Desenha as nuvens.
            cloud.draw(self.screen)
        self.obstacle_manager.draw(self.screen) # Desenha os obstáculos.
        self.powerup_manager.draw(self.screen) # Desenha os power-ups.
        self.score.draw(self.screen, is_night=not self.day) # Desenha a pontuação.
        self.draw_high_score() # Desenha a pontuação máxima.
        self.hud.draw(self.screen) # Desenha o HUD.
        dino_dead_img = None # Variável para a imagem do dinossauro morto.
        game_over_img = None # Variável para a imagem "Game Over".
        reset_img = None # Variável para a imagem "Reset".
        try:
            # Tenta carregar as imagens de Game Over.
            dino_dead_img = pygame.image.load(resource_path('dino_runner/assets/Dino/DinoDead.png'))
            game_over_img = pygame.image.load(resource_path('dino_runner/assets/Other/GameOver.png'))
            reset_img = pygame.image.load(resource_path('dino_runner/assets/Other/Reset.png'))
        except FileNotFoundError:
            # Fallback para superfícies de placeholder em caso de arquivo não encontrado.
            dino_dead_img = pygame.Surface((50, 50))
            dino_dead_img.fill((100, 0, 0))
            game_over_img = pygame.Surface((200, 50))
            game_over_img.fill((255, 0, 0))
            reset_img = pygame.Surface((100, 30))
            reset_img.fill((0, 255, 0))
        except pygame.error:
            # Fallback para superfícies de placeholder em caso de erro de carregamento do Pygame.
            dino_dead_img = pygame.Surface((50, 50))
            dino_dead_img.fill((100, 0, 0))
            game_over_img = pygame.Surface((200, 50))
            game_over_img.fill((255, 0, 0))
            reset_img = pygame.Surface((100, 30))
            reset_img.fill((0, 255, 0))
        if dino_dead_img: # Se a imagem do dinossauro morto foi carregada.
            dino_rect = self.player.dino_rect.copy() # Copia o retângulo de colisão do dinossauro.
            self.screen.blit(dino_dead_img, (dino_rect.x, dino_rect.y)) # Desenha o dinossauro morto.
        if game_over_img and reset_img: # Se as imagens de Game Over e Reset foram carregadas.
            # Obtém os retângulos das imagens centralizados na tela.
            game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            reset_rect = reset_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(game_over_img, game_over_rect) # Desenha a imagem "Game Over".
            self.screen.blit(reset_img, reset_rect) # Desenha a imagem "Reset".
        pygame.display.update() # Atualiza a tela.
        waiting = True # Flag para manter a tela de Game Over.
        reset_time = pygame.time.get_ticks() # Tempo para evitar cliques acidentais.
        while waiting: # Loop enquanto espera por uma ação do usuário.
            for event in pygame.event.get(): # Processa eventos.
                if event.type == pygame.QUIT: # Se o usuário fechar a janela.
                    self.save_high_score() # Salva a pontuação máxima.
                    self.running = False # Para o jogo.
                    waiting = False # Sai do loop de espera.
                if event.type == pygame.MOUSEBUTTONDOWN: # Se o mouse for clicado.
                    # Se clicou no botão de reset e passou um tempo mínimo.
                    if reset_rect.collidepoint(event.pos) and pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score() # Salva a pontuação máxima.
                        self.reset_game() # Reseta o jogo.
                        self.game_over = False # Sai do estado de game over.
                        self.playing = True # Inicia o jogo.
                        waiting = False # Sai do loop de espera.
                if event.type == pygame.KEYDOWN: # Se uma tecla for pressionada.
                    # Se qualquer tecla for pressionada e passou um tempo mínimo.
                    if pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score() # Salva a pontuação máxima.
                        self.reset_game() # Reseta o jogo.
                        self.game_over = False # Sai do estado de game over.
                        self.playing = True # Inicia o jogo.
                        waiting = False # Sai do loop de espera.

    def draw_background(self):
        """Desenha o fundo rolante."""
        image_width = BG.get_width() # Obtém a largura da imagem de fundo.
        self.bg_y_pos = 380 # Posição Y do fundo.
        self.screen.blit(BG, (self.bg_x_pos, self.bg_y_pos)) # Desenha a primeira imagem de fundo.
        self.screen.blit(BG, (self.bg_x_pos + image_width, self.bg_y_pos)) # Desenha a segunda imagem de fundo (para rolagem contínua).
        self.bg_x_pos -= self.game_speed # Move o fundo para a esquerda.
        if self.bg_x_pos <= -image_width: # Se a primeira imagem saiu completamente da tela.
            self.bg_x_pos = 0 # Reinicia a posição X do fundo.
