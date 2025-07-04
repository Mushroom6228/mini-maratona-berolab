from dino_runner.components.obstacles.obstacle import Obstacle
import random
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS

class Cactus(Obstacle):
    CACTUS = [
        (LARGE_CACTUS, 300),
        (SMALL_CACTUS, 325),
    ]

    def __init__(self):
        cactus_type = random.randint(0, 1)
        image, cactus_pos = self.CACTUS[cactus_type]
        self.type = random.randint(0, len(image)-1) if isinstance(image, list) else 0
        super().__init__(image, self.type)
        self.rect.y = cactus_pos