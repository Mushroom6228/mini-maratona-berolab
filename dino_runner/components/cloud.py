# dino_runner/components/cloud.py
import pygame
import random
from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_LEVEL_Y

class Cloud:
    def __init__(self):
        # Ensure CLOUD is not None before trying to use get_rect()
        if CLOUD:
            self.image = CLOUD
            self.rect = self.image.get_rect()
        else:
            print("Warning: Cloud image missing. Using placeholder.")
            self.image = pygame.Surface((50, 20)) # Placeholder
            self.image.fill((200, 200, 200)) # Gray color for the cloud
            self.rect = self.image.get_rect()

        # Adjust initial X position so clouds are well spread out
        self.rect.x = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH * 2) # Spread clouds across 2 screens
        
        # New: Diversify Y position, ensuring it's above the ground level
        # Max Y position should be well above the ground, e.g., SCREEN_HEIGHT / 2 - some_offset
        # Min Y position can be closer to the top, e.g., 20
        # Let's set a range from 20 (near top) to GROUND_LEVEL_Y - self.rect.height - 50 (above ground, with some margin)
        max_y = GROUND_LEVEL_Y - self.rect.height - 50
        min_y = 20
        self.rect.y = random.randint(min_y, max_y)

    def update(self, game_speed):
        self.rect.x -= game_speed // 2 # Clouds move slower than the ground
        if self.rect.right < 0:
            # When the cloud goes off screen, it reappears on the right in a new position
            self.rect.x = SCREEN_WIDTH + random.randint(0, SCREEN_WIDTH * 2)
            
            # New: Diversify Y position upon reappearance
            max_y = GROUND_LEVEL_Y - self.rect.height - 50
            min_y = 20
            self.rect.y = random.randint(min_y, max_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
