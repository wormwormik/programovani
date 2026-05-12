import pygame
from projektSettings import *

# HRÁČ
# dash + tiny efekt

class Player:
    def __init__(self):
        self.rect = pygame.Rect(180, 350, PLAYER_SIZE, PLAYER_SIZE)

        self.dashing = False
        self.dash_distance = 0
        self.last_dash_time = -DASH_COOLDOWN

        self.tiny = False
        self.tiny_end_time = 0

    def set_tiny(self, current_time):

        # zmenšení hráče na krátkou dobu

        self.tiny = True
        self.tiny_end_time = current_time + TINY_DURATION

        center = self.rect.center
        self.rect.size = (TINY_SIZE, TINY_SIZE)
        self.rect.center = center

    def update_tiny(self, current_time):
        if self.tiny and current_time > self.tiny_end_time:
            self.tiny = False
            center = self.rect.center
            self.rect.size = (PLAYER_SIZE, PLAYER_SIZE)
            self.rect.center = center

    def move(self, keys, current_time, power_active, game_speed):
        self.update_tiny(current_time)

        speed = 5 + (game_speed - 5) * 0.4
        if power_active == "speed":
            speed = 8
        if self.tiny:
            speed += 2

        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        # DASH systém

        if keys[pygame.K_SPACE] and not self.dashing:
            if current_time - self.last_dash_time >= DASH_COOLDOWN:
                if left or right:
                    self.dashing = True
                    self.dash_distance = 0
                    self.last_dash_time = current_time

        if self.dashing:
            move = 0
            if left:
                move = -DASH_SPEED
            elif right:
                move = DASH_SPEED

            self.rect.x += move
            self.dash_distance += abs(move)

            if self.dash_distance >= WIDTH // 2:
                self.dashing = False
        else:
            if left:
                self.rect.x -= speed
            if right:
                self.rect.x += speed

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

    def draw(self, screen):
        pygame.draw.rect(screen, (0,255,0), self.rect)