import pygame
import random
from projektSettings import *

# PADÁJÍCÍ BLOK

class FallingBlock:
    def __init__(self, y_start=0):
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - BLOCK_SIZE),
            y_start,
            BLOCK_SIZE,
            BLOCK_SIZE
        )

        # plynulý pohyb
        
        self.y_float = float(self.rect.y)

    def reset(self, y_start=0):
        self.rect.x = random.randint(0, WIDTH - BLOCK_SIZE)
        self.rect.y = y_start
        self.y_float = float(y_start)

    def update(self, speed):
        self.y_float += speed
        self.rect.y = int(self.y_float)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)