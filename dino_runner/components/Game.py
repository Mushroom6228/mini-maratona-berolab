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
        self.game_speed = 15  # Slower initial speed
        self.base_game_speed = 15  # Initial value for reset
        self.last_speedup_time = pygame.time.get_ticks()
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.cloud = Cloud()
        self.score = Score()
        self.lives = 3
        self.high_score = self.load_high_score()
        # Day/night cycle: 1 min day, 1 min night, fast transition (5s)
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.day_night_interval = 60000  # 1 minute
        self.day_night_transition = 5000  # 5 seconds
        self.day_night_progress = 0  # 0=day, 1=night
        self.day_night_direction = 1
        self.in_transition = False
        self.transition_start = 0
        # Adjustment to align the ground with the dinosaur's feet
        # The value 380 was tested to align the PNG ground with the dinosaur
        self.bg_x_pos = 0
        self.bg_y_pos = 380
        self.game_over = False

        # Define get_lives as an instance method to pass to HUD
        def get_lives_func():
            return self.lives
        self.hud = HUD(self.player, get_lives_func)

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
        """Loads the high score from a file."""
        if os.path.exists('highscore.txt'):
            with open('highscore.txt', 'r') as f:
                try:
                    return int(f.read())
                except ValueError:
                    return 0 # Handle case where file is empty or contains non-integer
        return 0

    def save_high_score(self):
        """Saves the current high score to a file."""
        with open('highscore.txt', 'w') as f:
            f.write(str(self.high_score))

    def execute(self):
        """Main game loop, handles game states (menu, playing, game over)."""
        self.playing = False # Start with menu
        self.game_over = False # Ensure game_over is false on initial start
        while self.running:
            if not self.playing:
                if self.game_over:
                    self.show_game_over() # This will handle resetting or quitting
                else:
                    self.show_menu() # This will handle starting the game or quitting
            else:
                self.run_game_loop() # This will set playing=False if game over or quit
        pygame.quit()

    def run_game_loop(self):
        """Runs the main game logic when the game is playing."""
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
            # Increase game speed gradually
            if now - self.last_speedup_time > 5000:
                self.game_speed += 1
                self.last_speedup_time = now

            self.update_day_night()
            bg_color = self.get_day_night_color()
            self.screen.fill(bg_color)
            self.draw_background()
            self.cloud.update(self.game_speed)
            self.cloud.draw(self.screen)

            # Only draw the animated dinosaur while playing
            if self.playing: # Check self.playing again in case it changed due to collision
                self.player.update(user_input)
                self.player.draw(self.screen)

            # Update obstacles and check for collisions
            if self.obstacle_manager.update(self.game_speed, self.player):
                if self.hit_sound:
                    self.hit_sound.play()
                self.lives -= 1
                if self.lives > 0:
                    self.reset_round()
                    continue # Skip remaining drawing/updating for this frame to avoid visual glitches
                else:
                    # Pause the game immediately, without redrawing the animated dinosaur
                    if self.die_sound: # Play die sound only on final death
                        self.die_sound.play()
                    self.playing = False
                    self.game_over = True
                    # The loop will naturally exit after this iteration

            # Only draw obstacles, powerups, score, and HUD if game is still playing
            if self.playing:
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
        """Resets game elements for a new round after a hit (but not game over)."""
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.player = Dinosaur()
        # Re-initialize HUD with the new player and current lives
        self.hud = HUD(self.player, lambda: self.lives) # Use lambda to get current lives
        # Score and lives are not reset in a round reset

    def reset_game(self):
        """Resets all game elements for a completely new game."""
        self.obstacle_manager.reset()
        self.powerup_manager.reset()
        self.score.reset()
        self.player = Dinosaur()
        self.hud = HUD(self.player, lambda: self.lives) # Use lambda to get current lives
        self.bg_x_pos = 0
        self.lives = 3
        # Reset day/night cycle
        self.day = True
        self.day_night_timer = pygame.time.get_ticks()
        self.in_transition = False
        self.day_night_progress = 0
        self.day_night_direction = 1
        self.transition_start = 0
        # Reset base speed
        self.game_speed = self.base_game_speed
        self.last_speedup_time = pygame.time.get_ticks()

    def draw_high_score(self):
        """Draws the high score on the screen."""
        font = pygame.font.Font(None, 28)
        text = font.render(f'High Score: {self.high_score}', True, (200, 0, 0) if self.day else (255, 255, 0))
        self.screen.blit(text, (SCREEN_WIDTH - 220, 10))
        if self.score.points > self.high_score:
            self.high_score = self.score.points

    def update_day_night(self):
        """Updates the day/night cycle and transition."""
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
                # Corrected: if it just became night, progress is 1; if it just became day, progress is 0
                self.day_night_progress = 1 if not self.day else 0
            else:
                # Correct the transition direction
                if self.day: # Transitioning from day to night
                    self.day_night_progress = progress
                else: # Transitioning from night to day
                    self.day_night_progress = 1 - progress

    def get_day_night_color(self):
        """Returns the current background color based on day/night cycle."""
        day_color = (255, 255, 255)
        night_color = (30, 30, 30)
        p = self.day_night_progress if self.in_transition else (0 if self.day else 1)
        return (
            int(day_color[0] * (1-p) + night_color[0] * p),
            int(day_color[1] * (1-p) + night_color[1] * p),
            int(day_color[2] * (1-p) + night_color[2] * p)
        )

    def handle_powerup_timers(self):
        """Manages the duration of active power-ups."""
        current_time = pygame.time.get_ticks()
        if self.player.has_shield and current_time > self.player.shield_time_up:
            self.player.has_shield = False
            self.player.image = self.player.running_img[0] # Corrected: Changed 'run_img' to 'running_img'
        if self.player.has_hammer and current_time > self.player.hammer_time_up:
            self.player.has_hammer = False
            # No specific image change for hammer, but good to note if there was one

    def show_menu(self):
        """Displays the game's main menu."""
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
            # Title animation
            color_anim += color_dir
            if color_anim > 50 or color_anim < 0:
                color_dir *= -1
            title_color = (0, 200-color_anim, 0)
            self.screen.fill((255, 255, 255))
            title = anim_font.render('T-Rex 2.0', True, title_color)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100))
            self.screen.blit(title, title_rect)
            # Subtitle
            subtitle = sub_font.render('Atualizado', True, (100, 100, 100))
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-40))
            self.screen.blit(subtitle, subtitle_rect)
            # "Free" text
            free = free_font.render('Free', True, (255, 255, 0))
            self.screen.blit(free, (title_rect.right+10, title_rect.top+10))
            # "Entrar" button
            pygame.draw.rect(self.screen, (0, 200, 0), button_rect, border_radius=10)
            entrar = button_font.render('Entrar', True, (255,255,255))
            self.screen.blit(entrar, (button_rect.x + (button_rect.width - entrar.get_width()) // 2, button_rect.y + (button_rect.height - entrar.get_height()) // 2))
            # "Sair" button
            pygame.draw.rect(self.screen, (200, 0, 0), exit_rect, border_radius=10)
            sair = button_font.render('Sair', True, (255,255,255))
            self.screen.blit(sair, (exit_rect.x + (exit_rect.width - sair.get_width()) // 2, exit_rect.y + (exit_rect.height - sair.get_height()) // 2))
            # High Score
            self.draw_high_score()
            pygame.display.update()
            clock.tick(60)

    def show_game_over(self):
        """
        Displays the game over screen, pausing the game at the moment of death.
        Shows the exact scene of death, the dead dinosaur, and reset options.
        """
        # Redraw the entire scene from the moment of death
        bg_color = self.get_day_night_color()
        self.screen.fill(bg_color)
        self.draw_background()
        self.cloud.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.score.draw(self.screen, is_night=not self.day)
        self.draw_high_score()
        self.hud.draw(self.screen)

        # Draw the dead dinosaur at its exact position of death
        dino_dead_img = pygame.image.load(os.path.join(IMG_DIR, 'Dino', 'DinoDead.png'))
        dino_rect = self.player.dino_rect.copy() # Use the dinosaur's rect at the moment of death
        self.screen.blit(dino_dead_img, (dino_rect.x, dino_rect.y))

        # Overlay Game Over and Reset images
        game_over_img = pygame.image.load(os.path.join(IMG_DIR, 'Other', 'GameOver.png'))
        reset_img = pygame.image.load(os.path.join(IMG_DIR, 'Other', 'Reset.png'))
        game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        reset_rect = reset_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(game_over_img, game_over_rect)
        self.screen.blit(reset_img, reset_rect)
        
        pygame.display.update() # Update the display to show the game over scene

        waiting = True
        reset_time = pygame.time.get_ticks()  # Mark the display time
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score() # Save high score before quitting
                    self.running = False
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Add a small delay to prevent accidental clicks right after death
                    if reset_rect.collidepoint(event.pos) and pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score() # Save high score before resetting
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    # Allow keyboard input to reset as well
                    if pygame.time.get_ticks() - reset_time > 500:
                        self.save_high_score() # Save high score before resetting
                        self.reset_game()
                        self.game_over = False
                        self.playing = True
                        waiting = False

    def draw_background(self):
        """Draws the scrolling background."""
        image_width = BG.get_width()
        # Adjustment to align the ground with the dinosaur's feet
        self.bg_y_pos = 380  # Adjust as needed for your PNG
        self.screen.blit(BG, (self.bg_x_pos, self.bg_y_pos))
        self.screen.blit(BG, (self.bg_x_pos + image_width, self.bg_y_pos))
        self.bg_x_pos -= self.game_speed
        if self.bg_x_pos <= -image_width:
            self.bg_x_pos = 0
