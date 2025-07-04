import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, RUNNING_SHIELD, JUMPING_SHIELD, DUCKING_SHIELD, RUNNING_HAMMER, JUMPING_HAMMER, DUCKING_HAMMER, DEFAULT_TYPE

class Dinosaur:
    X_POS = 80
    Y_POS = 310  # Volta ao valor original
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.is_running = True
        self.is_jumping = False
        self.is_ducking = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0
        self.has_shield = False
        self.has_hammer = False
        self.shield_time_up = 0
        self.hammer_time_up = 0

    def update(self, user_input):
        if self.is_jumping:
            self.jump()
        elif self.is_ducking:
            self.duck()
        else:
            self.run()

        # Pulo: só inicia se pressionar a tecla (não segurando)
        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.is_jumping:
            self.is_jumping = True
            self.is_running = False
            self.is_ducking = False
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not self.is_jumping:
            self.is_running = True
            self.is_ducking = False
            self.is_jumping = False

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        if self.has_hammer:
            self.image = RUNNING_HAMMER[self.step_index // 5]
        elif self.has_shield:
            self.image = RUNNING_SHIELD[self.step_index // 5]
        else:
            self.image = RUNNING[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        if self.has_hammer:
            self.image = JUMPING_HAMMER
        elif self.has_shield:
            self.image = JUMPING_SHIELD
        else:
            self.image = JUMPING
        if self.is_jumping:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.is_jumping = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = self.Y_POS

    def duck(self):
        if self.has_hammer:
            self.image = DUCKING_HAMMER[self.step_index // 5]
        elif self.has_shield:
            self.image = DUCKING_SHIELD[self.step_index // 5]
        else:
            self.image = DUCKING[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
