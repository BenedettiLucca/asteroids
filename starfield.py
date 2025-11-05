import pygame
import random

from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Star(CircleShape):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.5, 2.0)
        self.twinkle_phase = random.uniform(0, 2 * 3.14159)

    def update(self, dt):
        self.twinkle_phase += self.twinkle_speed * dt

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, self.position, self.radius)

class StarField:
    def __init__(self, num_stars=200):
        self.stars = pygame.sprite.Group()
        self.updatable = pygame.sprite.Group()

        Star.containers = (self.stars, self.updatable)

        for _ in range(num_stars):
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            size = random.choice([1, 1, 1, 1, 2])
            Star(x, y, size)

    def update(self, dt):
        self.updatable.update(dt)

    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)