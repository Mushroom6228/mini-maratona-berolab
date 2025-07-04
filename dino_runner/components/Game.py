import pygame
import os
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacle_manager import ObstacleManager
from dino_runner.components.powerup_manager import PowerUpManager
from dino_runner.components.cloud import Cloud
from dino_runner.components.score import Score
from dino_runner.components.hud import HUD
from dino_runner.utils.constants import BG, ICON, SCREEN_WIDTH, SCREEN_HEIGHT, FPS

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
        self.game_speed = 15  # Mais lento
        self.base_game_speed = 15  # Valor inicial para reset
        self.last_speedup_time = pygame.time.get_ticks()
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.cloud = Cloud()
        self.score = Score()
        self.lives = 3
        self.high_score = self.load_high_score()
        # Dia/noite: 1 min de dia, 1 min de noite, transição rápida (5s)
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.day_night_interval = 60000  # 1 minuto
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

        def get_lives():
            return self.lives
        self.get_lives = get_lives
        self.hud = HUD(self.player, self.get_lives)

        self.jump_sound = None
        self.hit_sound = None
        self.die_sound = None
        jump_path = os.path.join('dino_runner', 'assets', 'Other', 'jump.wav')
        hit_path = os.path.join('dino_runner', 'assets', 'Other', 'hit.wav')
        die_path = os.path.join('dino_runner', 'assets', 'Other', 'die.wav')
        if os.path.exists(jump_path):
            self.jump_sound = pygame.mixer.Sound(jump_path)
        if os.path.exists(hit_path):
            self.hit_sound = pygame.mixer.Sound(hit_path)
        if os.path.exists(die_path):
            self.die_sound = pygame.mixer.Sound(die_path)

    def load_high_score(self):
        if os.path.exists('highscore.txt'):
            with open('highscore.txt', 'r') as f:
                return int(f.read())
        return 0

    def save_high_score(self):
        with open('highscore.txt', 'w') as f:
            f.write(str(self.high_score))

    def execute(self):
        self.playing = True
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
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                # Permite pular com espaço OU seta para cima
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()
                        if self.jump_sound:
                            self.jump_sound.play()
            user_input = pygame.key.get_pressed()
            if user_input[pygame.K_SPACE] or user_input[pygame.K_UP]:
                self.player.jump()
                if self.jump_sound:
                    self.jump_sound.play()
            # Aumenta a velocidade base a cada 10 segundos
            now = pygame.time.get_ticks()
            if now - self.last_speedup_time > 10000:
                self.game_speed += 1  # Aumenta suavemente
                self.last_speedup_time = now
            self.update_day_night()
            bg_color = self.get_day_night_color()
            self.screen.fill(bg_color)
            self.draw_background()
            self.cloud.update(self.game_speed)
            self.cloud.draw(self.screen)
            self.player.update(user_input)
            self.player.draw(self.screen)
            if self.obstacle_manager.update(self.game_speed, self.player):
                if self.hit_sound:
                    self.hit_sound.play()
                if self.die_sound:
                    self.die_sound.play()
                self.lives -= 1
                if self.lives > 0:
                    self.reset_round()
                    continue
                else:
                    self.playing = False
                    self.game_over = True
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
        self.reset_game()
        self.save_high_score()

    def reset_round(self):
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.player = Dinosaur()
        self.hud = HUD(self.player, self.get_lives)
        # Não reseta score nem vidas

    def reset_game(self):
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.score.reset()
        self.player = Dinosaur()
        self.hud = HUD(self.player, self.get_lives)
        self.bg_x_pos = 0
        self.lives = 3
        # Reset ciclo de dia/noite
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.in_transition = False
        self.day_night_progress = 0
        self.day_night_direction = 1
        self.transition_start = 0
        # Reset velocidade base
        self.game_speed = self.base_game_speed
        self.last_speedup_time = pygame.time.get_ticks()

    def draw_high_score(self):
        font = pygame.font.Font(None, 28)
        text = font.render(f'High Score: {self.high_score}', True, (200, 0, 0) if self.day else (255, 255, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 220, 10))
        if self.score.points > self.high_score:
            self.high_score = self.score.points

    def update_day_night(self):
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
                self.day_night_progress = 1 if self.day else 0
            else:
                # Corrige a direção da transição
                if self.day:
                    self.day_night_progress = progress  # Dia para noite
                else:
                    self.day_night_progress = 1 - progress  # Noite para dia

    def get_day_night_color(self):
        day_color = (255, 255, 255)
        night_color = (30, 30, 30)
        p = self.day_night_progress if self.in_transition else (0 if self.day else 1)
        return (
            int(day_color[0] * (1-p) + night_color[0] * p),
            int(day_color[1] * (1-p) + night_color[1] * p),
            int(day_color[2] * (1-p) + night_color[2] * p)
        )

    def handle_powerup_timers(self):
        current_time = pygame.time.get_ticks()
        if self.player.has_shield and current_time > self.player.shield_time_up:
            self.player.has_shield = False
        if self.player.has_hammer and current_time > self.player.hammer_time_up:
            self.player.has_hammer = False

    def show_menu(self):
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
            # Texto Free
            free = free_font.render('Free', True, (255, 255, 0))
            self.screen.blit(free, (title_rect.right+10, title_rect.top+10))
            # Botão Entrar
            pygame.draw.rect(self.screen, (0, 200, 0), button_rect, border_radius=10)
            entrar = button_font.render('Entrar', True, (255,255,255))
            self.screen.blit(entrar, (button_rect.x+50, button_rect.y+8))
            # Botão Sair
            pygame.draw.rect(self.screen, (200, 0, 0), exit_rect, border_radius=10)
            sair = button_font.render('Sair', True, (255,255,255))
            self.screen.blit(sair, (exit_rect.x+65, exit_rect.y+8))
            # High Score
            self.draw_high_score()
            pygame.display.update()
            clock.tick(60)

    def show_game_over(self):
        from dino_runner.utils.constants import IMG_DIR
        game_over_img = pygame.image.load(os.path.join(IMG_DIR, 'Other', 'GameOver.png'))
        reset_img = pygame.image.load(os.path.join(IMG_DIR, 'Other', 'Reset.png'))
        game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        reset_rect = reset_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.fill((255, 255, 255))
        self.screen.blit(game_over_img, game_over_rect)
        self.screen.blit(reset_img, reset_rect)
        self.draw_high_score()
        pygame.display.update()
        waiting = True
        reset_time = pygame.time.get_ticks()  # Marca o tempo de exibição
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect.collidepoint(event.pos) and pygame.time.get_ticks() - reset_time > 500:
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    if pygame.time.get_ticks() - reset_time > 500:
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False

    def draw_background(self):
        image_width = BG.get_width()
        # Ajuste para alinhar o chão do cenário com o pé do dinossauro
        self.bg_y_pos = 380  # Ajuste conforme necessário para seu PNG
        self.screen.blit(BG, (self.bg_x_pos, self.bg_y_pos))
        self.screen.blit(BG, (self.bg_x_pos + image_width, self.bg_y_pos))
        self.bg_x_pos -= self.game_speed
        if self.bg_x_pos <= -image_width:
            self.bg_x_pos = 0
