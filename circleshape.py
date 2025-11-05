import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def wrap_position(self, screen_width, screen_height):
        """Wrap position around screen edges"""
        if self.position.x > screen_width + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = screen_width + self.radius

        if self.position.y > screen_height + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = screen_height + self.radius
    
    def check_collision(self, target):
        distance = self.position.distance_to(target.position)
        if distance > self.radius + target.radius:
            return False
        return True