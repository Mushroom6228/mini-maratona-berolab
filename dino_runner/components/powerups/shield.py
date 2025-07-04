from dino_runner.components.powerups.power_up import PowerUp

class Shield(PowerUp):
    def __init__(self):
        from dino_runner.utils.constants import SHIELD, SHIELD_TYPE
        self.image = SHIELD
        self.type = SHIELD_TYPE
        super().__init__(self.image, self.type)
        self.duration = 5  # segundos

    def update(self, game_speed, player):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            if hasattr(player, 'has_shield'):
                player.has_shield = False
        # Não fecha o jogo se pegar o escudo

    def draw(self, screen):
        screen.blit(self.image, self.rect)