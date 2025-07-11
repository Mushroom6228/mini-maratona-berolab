# dino_runner/game.py
import pygame
import os
from dino_runner.components.dinosaur import Dinosaur
# Try to import cv2 and numpy for the menu video
try:
    import cv2
    import numpy
except ImportError:
    cv2 = None
    numpy = None # Ensure numpy is also None if cv2 is not available

from dino_runner.components.obstacle_manager import ObstacleManager
from dino_runner.components.powerups.powerup_manager import PowerUpManager
from dino_runner.components.cloud import Cloud
from dino_runner.components.score import Score
from dino_runner.components.hud import HUD
# Import only necessary constants, as paths will be resolved by resource_path
from dino_runner.utils.constants import BG, ICON, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, POWERUP_SOUND
# Import draw_message_component and resource_path functions
from dino_runner.text_utils import draw_message_component
from dino_runner.utils.resource_manager import resource_path # Import resource_path

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chrome Dino Runner") # Título atualizado conforme seu constants.py
        # VERIFICAÇÃO CRÍTICA: Só tenta definir o ícone se ele foi carregado com sucesso
        if ICON:
            pygame.display.set_icon(ICON)
        else:
            print("Aviso: Não foi possível definir o ícone da janela. Imagem ICON não carregada ou inválida.")

        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.game_speed = 13
        self.base_game_speed = 13 # Armazena a velocidade inicial
        self.last_speedup_time = pygame.time.get_ticks()
        self.player = Dinosaur()
        self.player.game = self
        self.obstacle_manager = ObstacleManager()
        # Passa o som do power-up e o obstacle_manager para o PowerUpManager
        self.powerup_manager = PowerUpManager(POWERUP_SOUND, self.obstacle_manager)
        
        # Cria uma lista de nuvens para ter várias no cenário
        self.clouds = []
        for _ in range(7): # Adiciona 7 instâncias de nuvem
            self.clouds.append(Cloud())

        self.score = Score()
        self.lives = 3
        self.high_score = self.load_high_score()
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.day_night_interval = 40000 # 40 segundos
        self.day_night_transition = 5000 # 5 segundos
        self.day_night_progress = 0
        self.day_night_direction = 1
        self.in_transition = False
        self.transition_start = 0
        self.bg_x_pos = 0
        self.bg_y_pos = 380
        self.game_over = False

        self.hud = HUD(lambda: self.lives)

        # Carrega o vídeo do menu se o opencv estiver disponível
        self.video = None
        if cv2:
            # Caminho do vídeo usando resource_path
            video_path = resource_path('dino_runner/assets/Other/VideoMenu.mp4')
            print(f"DEBUG (game.py): Carregando vídeo de: {video_path}") # Debug
            if os.path.exists(video_path):
                self.video = cv2.VideoCapture(video_path)
            else:
                print(f"Aviso: Arquivo de vídeo não encontrado em '{video_path}'. O menu terá um fundo estático.")
        else:
            print("Aviso: opencv-python não está instalado. O vídeo do menu não será exibido. Instale com: pip install opencv-python numpy")

        self.jump_sound = None
        self.hit_sound = None
        self.hurt_sound = None
        # Caminhos dos sons usando resource_path. O caminho relativo é a partir de dino_runner/
        jump_path = resource_path('dino_runner/assets/Other/jump.wav')
        hit_path = resource_path('dino_runner/assets/Other/hit.wav')
        hurt_path = resource_path('dino_runner/assets/Other/hurt.wav')
        
        print(f"DEBUG (game.py): Carregando jump_sound de: {jump_path}") # Debug
        if os.path.exists(jump_path):
            self.jump_sound = pygame.mixer.Sound(jump_path)
        else:
            print(f"Aviso: Arquivo de som não encontrado: {jump_path}")
        
        print(f"DEBUG (game.py): Carregando hit_sound de: {hit_path}") # Debug
        if os.path.exists(hit_path):
            self.hit_sound = pygame.mixer.Sound(hit_path)
        else:
            print(f"Aviso: Arquivo de som não encontrado: {hit_path}")
        
        print(f"DEBUG (game.py): Carregando hurt_sound de: {hurt_path}") # Debug
        if os.path.exists(hurt_path):
            self.hurt_sound = pygame.mixer.Sound(hurt_path)
            self.hurt_sound.set_volume(1.0)
        else:
            print(f"Aviso: Arquivo de som não encontrado: {hurt_path}")

        # Removido: self.last_score_boost_time e self.score_boost_interval
        # A pontuação é agora totalmente gerenciada pelo objeto Score baseado no tempo.

    def load_high_score(self):
        """Carrega a pontuação máxima de um arquivo."""
        # Caminho para highscore.txt deve ser relativo à raiz do executável
        high_score_path = resource_path('highscore.txt')
        print(f"DEBUG (game.py): Carregando High Score de: {high_score_path}") # Debug
        if os.path.exists(high_score_path):
            with open(high_score_path, 'r') as f:
                try:
                    return int(f.read())
                except ValueError:
                    return 0
        return 0

    def save_high_score(self):
        """Salva a pontuação máxima atual em um arquivo."""
        # Caminho para highscore.txt deve ser relativo à raiz do executável
        high_score_path = resource_path('highscore.txt')
        print(f"DEBUG (game.py): Salvando High Score em: {high_score_path}") # Debug
        with open(high_score_path, 'w') as f:
            f.write(str(self.high_score))

    def execute(self):
        """Loop principal do jogo, lida com os estados do jogo (menu, jogando, game over)."""
        self.playing = False
        self.game_over = False
        while self.running:
            if not self.playing:
                if self.game_over:
                    self.show_game_over()
                else:
                    self.show_menu()
            else:
                self.run_game_loop()
        pygame.quit()

    def run_game_loop(self):
        """Executa a lógica principal do jogo quando o jogo está em andamento."""
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    if not self.player.is_jumping:
                        self.player.start_jump()
                        if self.jump_sound:
                            self.jump_sound.play()

            user_input = pygame.key.get_pressed()
            now = pygame.time.get_ticks()

            # Lógica para aumentar a velocidade do jogo a cada 5 segundos
            if now - self.last_speedup_time > 5000:
                self.game_speed += 0.5 # Aumenta a velocidade em 0.5
                self.last_speedup_time = now
            
            # Removido: Lógica de incremento de 100 pontos a cada 10 segundos
            # self.score.actual_points += 100 foi movido para o Score.update()
            # para ser gerenciado internamente e de forma suave.

            self.update_day_night()
            bg_color = self.get_day_night_color()
            self.screen.fill(bg_color)
            self.draw_background()
            
            # Atualiza e desenha todas as nuvens
            for cloud in self.clouds:
                cloud.update(self.game_speed)
                cloud.draw(self.screen)

            self.player.update(user_input)
            self.player.draw(self.screen)

            collision_detected = self.obstacle_manager.update(self.game_speed, self.player)
            if collision_detected:
                if not self.player.is_invincible:
                    if self.hit_sound:
                        self.hit_sound.play()
                    if self.hurt_sound:
                        self.hurt_sound.play()
                    self.lives -= 1
                    if self.lives > 0:
                        self.player.start_invincibility(pygame.time.get_ticks())
                    else:
                        self.playing = False
                        self.game_over = True

            if self.playing:
                self.obstacle_manager.draw(self.screen)
                self.powerup_manager.update(self.game_speed, self.player)
                self.powerup_manager.draw(self.screen)
                # O update do score agora recebe a velocidade do jogo para calcular os pontos.
                # Não precisa mais passar game_speed para o score, pois ele é baseado em tempo.
                self.score.update(is_night=not self.day) 
                self.score.draw(self.screen, is_night=not self.day)
                self.draw_high_score()
                self.hud.draw(self.screen)
                self.handle_powerup_timers()

            pygame.display.update()
            self.clock.tick(FPS)

    def reset_game(self):
        """Reseta todos os elementos do jogo para um novo jogo completo."""
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.score.reset()
        self.player = Dinosaur()
        self.player.game = self
        self.hud = HUD(lambda: self.lives)
        self.bg_x_pos = 0
        self.lives = 3
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.in_transition = False
        self.day_night_progress = 0
        self.day_night_direction = 1
        self.transition_start = 0
        self.game_speed = self.base_game_speed # Reseta a velocidade do jogo para a base
        self.last_speedup_time = pygame.time.get_ticks() # Reseta o timer de aumento de velocidade
        # Removido: self.last_score_boost_time = pygame.time.get_ticks()

        # Reseta as nuvens para posições iniciais espalhadas
        self.clouds = []
        for _ in range(7):
            self.clouds.append(Cloud())


    def draw_high_score(self):
        """Desenha a pontuação máxima na tela."""
        # Usa a função draw_message_component para desenhar a pontuação
        draw_message_component(
            f'High Score: {self.high_score}',
            self.screen,
            font_color=(200, 0, 0), # Sempre vermelho
            font_size=20, # Mantém 20 para consistência
            pos_x_center=SCREEN_WIDTH - 200, # Ajusta a posição X
            pos_y_center=18 # Ajusta a posição Y
        )
        if self.score.points > self.high_score:
            self.high_score = self.score.points

    def update_day_night(self):
        """Atualiza o ciclo dia/noite e a transição."""
        now = pygame.time.get_ticks()
        if not self.in_transition:
            if now - self.day_night_timer > self.day_night_interval:
                self.in_transition = True
                self.transition_start = now
            # Se não estiver em transição e for dia, avança o progresso para 0 (dia)
            # Se não estiver em transição e for noite, avança o progresso para 1 (noite)
            self.day_night_progress = 0 if self.day else 1
        else:
            progress = (now - self.transition_start) / self.day_night_transition
            if progress >= 1:
                self.day = not self.day
                self.day_night_timer = now
                self.in_transition = False
                self.day_night_progress = 1 if not self.day else 0
            else:
                # Corrige a direção da transição
                if self.day: # Transicionando de dia para noite (progress aumenta de 0 para 1)
                    self.day_night_progress = progress
                else: # Transicionando de noite para dia (progress diminui de 1 para 0)
                    self.day_night_progress = 1 - progress


    def get_day_night_color(self):
        """Retorna a cor de fundo atual baseada no ciclo dia/noite."""
        day_color = (255, 255, 255)
        night_color = (30, 30, 30)
        p = self.day_night_progress # 'p' já representa o progresso de 0 a 1
        return (
            int(day_color[0] * (1-p) + night_color[0] * p),
            int(day_color[1] * (1-p) + night_color[1] * p),
            int(day_color[2] * (1-p) + night_color[2] * p)
        )

    def handle_powerup_timers(self):
        """Gerencia a duração dos power-ups ativos."""
        current_time = pygame.time.get_ticks()
        if self.player.has_shield and current_time > self.player.shield_time_up:
            self.player.has_shield = False
        if self.player.has_hammer and current_time > self.player.hammer_time_up:
            self.player.has_hammer = False
            
    def show_menu(self):
        """Exibe o menu principal do jogo."""
        clock = pygame.time.Clock()
        color_anim = 0
        color_dir = 1
        button_rect = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+40, 200, 50)
        exit_rect = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+110, 200, 50)

        video_frame_surface = None
        frame_count = 0

        while not self.playing and self.running and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.playing = True
                        return
                    if exit_rect.collidepoint(event.pos):
                        self.running = False
                        return
            color_anim += color_dir
            if color_anim > 50 or color_anim < 0:
                color_dir *= -1
            title_color = (0, 200-color_anim, 0)

            if self.video:
                frame_count += 1
                if frame_count % 2 == 0: # Reproduz o vídeo mais lentamente
                    ret, frame = self.video.read()
                    if not ret:
                        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        ret, frame = self.video.read()
                    
                    if ret:
                        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        video_frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                
                if video_frame_surface:
                    self.screen.blit(video_frame_surface, (0, 0))
                else:
                    self.screen.fill((255, 255, 255))
            else:
                self.screen.fill((255, 255, 255))

            # Usa draw_message_component para renderizar o texto
            # Título principal "T-Rex 2.0"
            # Ajustado para que "2.0" fique mais à esquerda
            draw_message_component('T-Rex 2.0', self.screen, font_color=title_color, font_size=80, pos_x_center=SCREEN_WIDTH//2 - 50, pos_y_center=SCREEN_HEIGHT//2-100)
            
            # Subtítulo "Atualizado"
            draw_message_component('Atualizado', self.screen, font_color=(100, 100, 100), font_size=36, pos_y_center=SCREEN_HEIGHT//2-40)
            
            # Palavra "Free" ao lado do título (ajustado para ficar mais próximo)
            # A posição X é calculada a partir do centro da tela, adicionando um offset
            # que leva em conta a largura aproximada do título para posicionar 'Free' corretamente.
            # Mantido o ajuste anterior para "Free"
            draw_message_component('Free', self.screen, font_color=(255, 255, 0), font_size=36, pos_x_center=SCREEN_WIDTH//2 + 300, pos_y_center=SCREEN_HEIGHT//2-100 - 10)

            pygame.draw.rect(self.screen, (0, 200, 0), button_rect, border_radius=10)
            draw_message_component('Entrar', self.screen, font_color=(255,255,255), font_size=40, pos_x_center=button_rect.centerx, pos_y_center=button_rect.centery)

            pygame.draw.rect(self.screen, (200, 0, 0), exit_rect, border_radius=10)
            draw_message_component('Sair', self.screen, font_color=(255,255,255), font_size=40, pos_x_center=exit_rect.centerx, pos_y_center=exit_rect.centery)
            
            pygame.display.update()
            clock.tick(60)

    def show_game_over(self):
        """
        Exibe a tela de Game Over, pausando o jogo no momento da morte.
        Mostra a cena exata da morte, o dinossauro morto e as opções de reset.
        """
        bg_color = self.get_day_night_color()
        self.screen.fill(bg_color)
        self.draw_background()
        
        # Desenha todas as nuvens na tela de Game Over
        for cloud in self.clouds:
            cloud.draw(self.screen)

        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.score.draw(self.screen, is_night=not self.day)
        self.draw_high_score()
        self.hud.draw(self.screen)

        dino_dead_img = None
        game_over_img = None
        reset_img = None
        try:
            dino_dead_img = pygame.image.load(resource_path('dino_runner/assets/Dino/DinoDead.png'))
            game_over_img = pygame.image.load(resource_path('dino_runner/assets/Other/GameOver.png'))
            reset_img = pygame.image.load(resource_path('dino_runner/assets/Other/Reset.png'))
        except FileNotFoundError:
            print("Aviso: 'DinoDead.png', 'GameOver.png' ou 'Reset.png' imagens não encontradas. Usando placeholders.")
            dino_dead_img = pygame.Surface((50, 50))
            dino_dead_img.fill((100, 0, 0)) # Placeholder para dino morto
            game_over_img = pygame.Surface((200, 50))
            game_over_img.fill((255, 0, 0))
            reset_img = pygame.Surface((100, 30))
            reset_img.fill((0, 255, 0))
        except pygame.error as e:
            print(f"Erro ao carregar imagens de Game Over: {e}. Usando placeholders.")
            dino_dead_img = pygame.Surface((50, 50))
            dino_dead_img.fill((100, 0, 0))
            game_over_img = pygame.Surface((200, 50))
            game_over_img.fill((255, 0, 0))
            reset_img = pygame.Surface((100, 30))
            reset_img.fill((0, 255, 0))


        if dino_dead_img: # Só desenha se a imagem foi carregada ou placeholder criado
            dino_rect = self.player.dino_rect.copy()
            self.screen.blit(dino_dead_img, (dino_rect.x, dino_rect.y))

        if game_over_img and reset_img:
            game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            reset_rect = reset_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(game_over_img, game_over_rect)
            self.screen.blit(reset_img, reset_rect)
        
        pygame.display.update()

        waiting = True
        reset_time = pygame.time.get_ticks()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    self.running = False
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect.collidepoint(event.pos) and pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score()
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    if pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score()
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False

    def draw_background(self):
        """Desenha o fundo rolante."""
        image_width = BG.get_width()
        self.bg_y_pos = 380
        self.screen.blit(BG, (self.bg_x_pos, self.bg_y_pos))
        self.screen.blit(BG, (self.bg_x_pos + image_width, self.bg_y_pos))
        self.bg_x_pos -= self.game_speed
        if self.bg_x_pos <= -image_width:
            self.bg_x_pos = 0
