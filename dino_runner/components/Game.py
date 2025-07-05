# dino_runner/game.py
import pygame
import os
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacle_manager import ObstacleManager
from dino_runner.components.powerup_manager import PowerUpManager
from dino_runner.components.cloud import Cloud
from dino_runner.components.score import Score
from dino_runner.components.hud import HUD
from dino_runner.utils.constants import BG, ICON, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMG_DIR

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini Jogo Dino")
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.game_speed = 13  # Velocidade inicial um pouco maior
        self.base_game_speed = 13  # Valor inicial para reset
        self.last_speedup_time = pygame.time.get_ticks()
        self.player = Dinosaur()
        self.player.game = self  # Garante referência para o dinossauro
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.cloud = Cloud()
        self.score = Score()
        self.lives = 3
        self.high_score = self.load_high_score()
        # Ciclo Dia/Noite: 1 min dia, 1 min noite, transição rápida (5s)
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.day_night_interval = 40000  # 40 segundos
        self.day_night_transition = 5000  # 5 segundos
        self.day_night_progress = 0  # 0=dia, 1=noite
        self.day_night_direction = 1
        self.in_transition = False
        self.transition_start = 0
        # Ajuste para alinhar o chão do cenário com o pé do dinossauro
        # O valor 380 foi testado para alinhar o chão do PNG com o dinossauro
        self.bg_x_pos = 0
        self.bg_y_pos = 380
        self.game_over = False

        # Define get_lives como um método da instância para passar para HUD
        def get_lives_func():
            return self.lives
        self.hud = HUD(self.player, get_lives_func)

        self.jump_sound = None
        self.hit_sound = None
        self.hurt_sound = None
        jump_path = os.path.join('dino_runner', 'assets', 'Other', 'jump.wav')
        hit_path = os.path.join('dino_runner', 'assets', 'Other', 'hit.wav')
        hurt_path = os.path.join('dino_runner', 'assets', 'Other', 'hurt.wav')
        if os.path.exists(jump_path):
            self.jump_sound = pygame.mixer.Sound(jump_path)
        if os.path.exists(hit_path):
            self.hit_sound = pygame.mixer.Sound(hit_path)
        if os.path.exists(hurt_path):
            self.hurt_sound = pygame.mixer.Sound(hurt_path)
            self.hurt_sound.set_volume(1.0)  # Garante volume máximo

    def load_high_score(self):
        """Carrega a pontuação máxima de um arquivo."""
        if os.path.exists('highscore.txt'):
            with open('highscore.txt', 'r') as f:
                try:
                    return int(f.read())
                except ValueError:
                    return 0 # Lida com o caso em que o arquivo está vazio ou contém algo que não é um número
        return 0

    def save_high_score(self):
        """Salva a pontuação máxima atual em um arquivo."""
        with open('highscore.txt', 'w') as f:
            f.write(str(self.high_score))

    def execute(self):
        """Loop principal do jogo, lida com os estados do jogo (menu, jogando, game over)."""
        self.playing = False # Começa com o menu
        self.game_over = False # Garante que game_over seja falso no início
        while self.running:
            if not self.playing:
                if self.game_over:
                    self.show_game_over() # Isso lidará com o reset ou saída
                else:
                    self.show_menu() # Isso lidará com o início do jogo ou saída
            else:
                self.run_game_loop() # Isso definirá playing=False se for game over ou sair
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
            # Aumenta a velocidade do jogo: +0.5 a cada 10 segundos
            if now - self.last_speedup_time > 10000:
                self.game_speed += 0.5
                self.last_speedup_time = now

            self.update_day_night()
            bg_color = self.get_day_night_color()
            self.screen.fill(bg_color)
            self.draw_background()
            self.cloud.update(self.game_speed)
            self.cloud.draw(self.screen)

            # Atualiza e desenha o dinossauro
            self.player.update(user_input)
            self.player.draw(self.screen)

            # Atualiza obstáculos e verifica colisões
            collision_detected = self.obstacle_manager.update(self.game_speed, self.player)
            if collision_detected:
                if not self.player.is_invincible: # Só leva dano se não estiver invencível
                    if self.hit_sound:
                        self.hit_sound.play()
                    if self.hurt_sound:  # Toca o som de dano sempre que perder um coração
                        print('DEBUG: Tocando hurt.wav')
                        self.hurt_sound.play()
                    self.lives -= 1
                    if self.lives > 0:
                        self.player.start_invincibility(pygame.time.get_ticks()) # Inicia invencibilidade
                        # O jogo continua, sem resetar a posição do dinossauro ou a rodada.
                    else:
                        # Vidas são 0, é game over
                        self.playing = False
                        self.game_over = True
                        # O loop sairá naturalmente após esta iteração

            # Desenha obstáculos, power-ups, pontuação e HUD se o jogo ainda estiver em andamento
            if self.playing: # Verifica novamente se o jogo ainda está jogando (pode ter mudado após colisão)
                self.obstacle_manager.draw(self.screen)
                self.powerup_manager.update(self.game_speed, self.player)
                self.powerup_manager.draw(self.screen)
                self.score.update(is_night=not self.day)
                self.score.draw(self.screen, is_night=not self.day)
                self.draw_high_score()
                self.hud.draw(self.screen)
                self.handle_powerup_timers()

            pygame.display.update()
            self.clock.tick(FPS)

    def reset_round(self):
        """Reseta elementos do jogo para uma nova rodada após um acerto (mas não game over).
        NOTA: Esta função não é mais chamada em caso de acerto com vidas restantes,
        apenas o estado de invencibilidade é ativado. Ela pode ser usada para
        outros resets se necessário."""
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.player = Dinosaur()
        self.player.game = self  # Garante referência para o dinossauro
        self.hud = HUD(self.player, lambda: self.lives) # Usa lambda para obter as vidas atuais
        # Pontuação e vidas não são resetadas em um reset de rodada

    def reset_game(self):
        """Reseta todos os elementos do jogo para um novo jogo completo."""
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.score.reset()
        self.player = Dinosaur()
        self.player.game = self  # Garante referência para o dinossauro
        self.hud = HUD(self.player, lambda: self.lives) # Usa lambda para obter as vidas atuais
        self.bg_x_pos = 0
        self.lives = 3
        # Reseta ciclo dia/noite
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.in_transition = False
        self.day_night_progress = 0
        self.day_night_direction = 1
        self.transition_start = 0
        # Reseta velocidade base
        self.game_speed = self.base_game_speed
        self.last_speedup_time = pygame.time.get_ticks()

    def draw_high_score(self):
        """Desenha a pontuação máxima na tela."""
        font = pygame.font.Font(None, 28)
        text = font.render(f'High Score: {self.high_score}', True, (200, 0, 0))  # Sempre vermelho
        self.screen.blit(text, (SCREEN_WIDTH - 220, 10))
        if self.score.points > self.high_score:
            self.high_score = self.score.points

    def update_day_night(self):
        """Atualiza o ciclo dia/noite e a transição."""
        now = pygame.time.get_ticks()
        if not self.in_transition:
            if now - self.day_night_timer > self.day_night_interval:
                self.in_transition = True
                self.transition_start = now
        else:
            progress = (now - self.transition_start) / self.day_night_transition
            if progress >= 1:
                self.day = not self.day
                self.day_night_timer = now
                self.in_transition = False
                # Corrigido: se acabou de virar noite, progresso é 1; se acabou de virar dia, progresso é 0
                self.day_night_progress = 1 if not self.day else 0
            else:
                # Corrige a direção da transição
                if self.day: # Transicionando de dia para noite
                    self.day_night_progress = progress
                else: # Transicionando de noite para dia
                    self.day_night_progress = 1 - progress

    def get_day_night_color(self):
        """Retorna a cor de fundo atual baseada no ciclo dia/noite."""
        day_color = (255, 255, 255)
        night_color = (30, 30, 30)
        p = self.day_night_progress if self.in_transition else (0 if self.day else 1)
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
            # A imagem do dinossauro será atualizada pelo método update() do próprio dinossauro
        if self.player.has_hammer and current_time > self.player.hammer_time_up:
            self.player.has_hammer = False
            # A imagem do dinossauro será atualizada pelo método update() do próprio dinossauro
            
    def show_menu(self):
        """Exibe o menu principal do jogo."""
        anim_font = pygame.font.Font(None, 80)
        sub_font = pygame.font.Font(None, 36)
        free_font = pygame.font.Font(None, 36)
        button_font = pygame.font.Font(None, 40)
        clock = pygame.time.Clock()
        color_anim = 0
        color_dir = 1
        button_rect = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+40, 200, 50)
        exit_rect = pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+110, 200, 50)
        while not self.playing and self.running and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.playing = True
                        return
                    if exit_rect.collidepoint(event.pos):
                        self.running = False
                        return
            # Animação do título
            color_anim += color_dir
            if color_anim > 50 or color_anim < 0:
                color_dir *= -1
            title_color = (0, 200-color_anim, 0)
            self.screen.fill((255, 255, 255))
            title = anim_font.render('T-Rex 2.0', True, title_color)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100))
            self.screen.blit(title, title_rect)
            # Subtítulo
            subtitle = sub_font.render('Atualizado', True, (100, 100, 100))
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-40))
            self.screen.blit(subtitle, subtitle_rect)
            # Texto "Free"
            free = free_font.render('Free', True, (255, 255, 0))
            self.screen.blit(free, (title_rect.right+10, title_rect.top+10))
            # Botão "Entrar"
            pygame.draw.rect(self.screen, (0, 200, 0), button_rect, border_radius=10)
            entrar = button_font.render('Entrar', True, (255,255,255))
            self.screen.blit(entrar, (button_rect.x + (button_rect.width - entrar.get_width()) // 2, button_rect.y + (button_rect.height - entrar.get_height()) // 2))
            # Botão "Sair"
            pygame.draw.rect(self.screen, (200, 0, 0), exit_rect, border_radius=10)
            sair = button_font.render('Sair', True, (255,255,255))
            self.screen.blit(sair, (exit_rect.x + (exit_rect.width - sair.get_width()) // 2, exit_rect.y + (exit_rect.height - sair.get_height()) // 2))
            # High Score
            self.draw_high_score()
            pygame.display.update()
            clock.tick(60)

    def show_game_over(self):
        """
        Exibe a tela de Game Over, pausando o jogo no momento da morte.
        Mostra a cena exata da morte, o dinossauro morto e as opções de reset.
        """
        # Redesenha toda a cena do momento da morte
        bg_color = self.get_day_night_color()
        self.screen.fill(bg_color)
        self.draw_background()
        self.cloud.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.score.draw(self.screen, is_night=not self.day)
        self.draw_high_score()
        self.hud.draw(self.screen)

        # Desenha o dinossauro morto na posição exata da morte
        dino_dead_img = pygame.image.load(os.path.join(IMG_DIR, 'Dino', 'DinoDead.png'))
        dino_rect = self.player.dino_rect.copy() # Usa o rect do dinossauro no momento da morte
        self.screen.blit(dino_dead_img, (dino_rect.x, dino_rect.y))

        # Sobrepõe as imagens de Game Over e Reset
        game_over_img = pygame.image.load(os.path.join(IMG_DIR, 'Other', 'GameOver.png'))
        reset_img = pygame.image.load(os.path.join(IMG_DIR, 'Other', 'Reset.png'))
        game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        reset_rect = reset_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(game_over_img, game_over_rect)
        self.screen.blit(reset_img, reset_rect)
        
        pygame.display.update() # Atualiza a tela para mostrar a cena de game over

        waiting = True
        reset_time = pygame.time.get_ticks()  # Marca o tempo de exibição
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score() # Salva a pontuação máxima antes de sair
                    self.running = False
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Adiciona um pequeno atraso para evitar cliques acidentais logo após a morte
                    if reset_rect.collidepoint(event.pos) and pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score() # Salva a pontuação máxima antes de resetar
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    # Permite entrada de teclado para resetar também
                    if pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score() # Salva a pontuação máxima antes de resetar
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False

    def draw_background(self):
        """Desenha o fundo rolante."""
        image_width = BG.get_width()
        # Ajuste para alinhar o chão do cenário com o pé do dinossauro
        self.bg_y_pos = 380  # Ajuste conforme necessário para seu PNG
        self.screen.blit(BG, (self.bg_x_pos, self.bg_y_pos))
        self.screen.blit(BG, (self.bg_x_pos + image_width, self.bg_y_pos))
        self.bg_x_pos -= self.game_speed
        if self.bg_x_pos <= -image_width:
            self.bg_x_pos = 0
