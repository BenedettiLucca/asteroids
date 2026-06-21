import pygame

from circleshape import CircleShape
from constants import PLAYER_SHOOT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

SHOT_RADIUS = 5
SHOT_LIFETIME = 1.5

class Shot(CircleShape):
  def __init__(self, x, y, velocity, owner=None):
    super().__init__(x, y, SHOT_RADIUS)
    self.velocity = velocity * PLAYER_SHOOT_SPEED
    self.lifetime = 0
    self.owner = owner  # Referência ao jogador que atirou

  def draw(self, screen):
    # Cor do tiro baseada no dono
    if self.owner:
      if self.owner.player_id == 1:
        color = "cyan"
      else:
        color = "yellow"
    else:
      color = "white"
    pygame.draw.circle(screen, color, self.position, self.radius, 2)

  def update(self, dt):
    self.position += (self.velocity * dt)
    self.lifetime += dt

    if self.lifetime > SHOT_LIFETIME:
      self.kill()