import pygame
from constants import PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT

from circleshape import CircleShape
from constants import PLAYER_RADIUS
from shot import Shot
class Player(CircleShape):
  def __init__(self, x, y, particle_system=None, audio_manager=None, player_id=1, color="white"):
    super().__init__(x, y, PLAYER_RADIUS)
    self.rotation = 0
    self.shoot_timer = 0
    self.score = 0
    self.speed = PLAYER_SPEED
    self.invulnerable_timer = 0
    self.lives = 3
    self.thrusting = False
    self.particle_system = particle_system
    self.audio_manager = audio_manager
    self.player_id = player_id
    self.color = color
    self.controls = self.get_controls()

    # Definir nome do jogador
    if player_id == 1:
      self.name = "JOGADOR 1"
    else:
      self.name = "JOGADOR 2"

  def get_controls(self):
    """Retorna os controles específicos de cada jogador"""
    if self.player_id == 1:
      return {
        'forward': pygame.K_w,
        'backward': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d,
        'shoot': pygame.K_SPACE
      }
    else:
      return {
        'forward': pygame.K_UP,
        'backward': pygame.K_DOWN,
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'shoot': pygame.K_RCTRL
      }

  def is_alive(self):
    """Verifica se o jogador está vivo (ainda tem vidas)"""
    return self.lives > 0

  def draw(self, screen):
    if self.invulnerable_timer > 0:
      if int(self.invulnerable_timer * 10) % 2 == 0:
        pygame.draw.polygon(screen, self.color, self.triangle(), 2)
    else:
      pygame.draw.polygon(screen, self.color, self.triangle(), 2)

    # Draw player name above the ship (smaller font)
    if self.lives > 0:  # Only draw name if player is alive
      font = pygame.font.Font(None, 24)
      text = font.render(self.name, True, self.color)
      text_rect = text.get_rect(center=(self.position.x, self.position.y - 30))
      screen.blit(text, text_rect)
  
  # in the player class
  def triangle(self):
      forward = pygame.Vector2(0, 1).rotate(self.rotation)
      right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
      a = self.position + forward * self.radius
      b = self.position - forward * self.radius - right
      c = self.position - forward * self.radius + right
      return [a, b, c]

  def rotate(self, dt):
     self.rotation += PLAYER_TURN_SPEED * dt

  def update(self, dt):
    keys = pygame.key.get_pressed()
    self.thrusting = False

    # Usar controles específicos do jogador
    if keys[self.controls['left']]:
      self.rotate((-1)*dt)
    if keys[self.controls['right']]:
      self.rotate(dt)
    if keys[self.controls['backward']]:
      self.thrusting = True
      self.move((-1)*dt)
    if keys[self.controls['forward']]:
      self.thrusting = True
      self.move(dt)
    if keys[self.controls['shoot']]:
      self.shoot()

    self.shoot_timer -= dt
    self.invulnerable_timer -= dt
    self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

  def move(self, dt):
    forward = pygame.Vector2(0, 1).rotate(self.rotation)
    self.position += forward * self.speed * dt
    if (self.speed < 2000):
      self.speed *= 1.03

    if self.particle_system and self.thrusting:
      back = pygame.Vector2(0, 1).rotate(self.rotation + 180)
      thruster_pos = self.position + back * self.radius
      self.particle_system.create_thruster_flame(thruster_pos, back, 2)
  
  def shoot(self):
    if self.shoot_timer > 0:
      return
    velocity = pygame.Vector2(0, 1).rotate(self.rotation)
    Shot(self.position.x, self.position.y, velocity, owner=self)
    self.shoot_timer = PLAYER_SHOOT_COOLDOWN
    
  def add_score(self, points):
    self.score += points
    
  def reset_speed(self):
    self.speed = PLAYER_SPEED

  def take_damage(self):
    if self.invulnerable_timer > 0:
      return False

    self.lives -= 1
    if self.lives > 0:
      self.respawn()
      return True
    return False

  def respawn(self):
    self.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    self.velocity = pygame.Vector2(0, 0)
    self.rotation = 0
    self.invulnerable_timer = 3.0
    self.speed = PLAYER_SPEED