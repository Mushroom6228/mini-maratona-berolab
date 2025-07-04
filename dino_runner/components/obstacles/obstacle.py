import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, type):
        super().__init__()
        self.image = image[type] if isinstance(image, list) else image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = 1100

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
