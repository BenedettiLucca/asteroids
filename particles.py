import pygame
import random
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Particle(CircleShape):
    def __init__(self, x, y, velocity, lifetime, color):
        super().__init__(x, y, random.randint(2, 4))
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        alpha = max(0, int(255 * (self.lifetime / self.max_lifetime)))
        color = self.color[:3]
        surface = pygame.Surface((self.radius * 2, self.radius * 2))
        surface.set_alpha(alpha)
        surface.fill((0, 0, 0))
        pygame.draw.circle(surface, color, (self.radius, self.radius), self.radius)
        screen.blit(surface, (self.position.x - self.radius, self.position.y - self.radius))

class ParticleSystem:
    def __init__(self):
        self.particles = pygame.sprite.Group()
        self.updatable = pygame.sprite.Group()

        Particle.containers = (self.particles, self.updatable)

    def update(self, dt):
        self.updatable.update(dt)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def create_explosion(self, position, num_particles=15, color=(255, 200, 100)):
        for _ in range(num_particles):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 200)
            velocity = pygame.Vector2(1, 0).rotate(angle) * speed
            lifetime = random.uniform(0.5, 1.5)
            Particle(position.x, position.y, velocity, lifetime, color)

    def create_thruster_flame(self, position, direction, num_particles=3):
        for _ in range(num_particles):
            spread = random.uniform(-30, 30)
            velocity = direction.rotate(spread) * random.uniform(100, 150)
            lifetime = random.uniform(0.2, 0.5)
            color = (random.randint(200, 255), random.randint(100, 150), 50)
            Particle(position.x, position.y, velocity, lifetime, color)