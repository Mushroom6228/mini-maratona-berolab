class PowerUp:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = 300
        self.start_time = 0
        self.duration = 5  # segundos

    def update(self, game_speed, player):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            player.has_shield = False
            player.has_hammer = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
