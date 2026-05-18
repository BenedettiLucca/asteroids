import pygame
import pygame.freetype
from constants import SCREEN_WIDTH,SCREEN_HEIGHT,ASTEROID_MIN_RADIUS,ASTEROID_KINDS,ASTEROID_SPAWN_RATE,ASTEROID_MAX_RADIUS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from starfield import StarField
from particles import ParticleSystem
from audio import AudioManager
from storage import load_highscore, save_highscore

def main():
  pygame.init()
  clock = pygame.time.Clock()
  dt = 0

  print('Starting asteroids!')
  print(f"Screen width: {SCREEN_WIDTH}")
  print(f"Screen height: {SCREEN_HEIGHT}")

  updatable = pygame.sprite.Group()
  drawable = pygame.sprite.Group()
  asteroids = pygame.sprite.Group()
  shots = pygame.sprite.Group()

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  my_font = pygame.freetype.SysFont('Ponderosa', 30)
  info_font = pygame.freetype.SysFont('Ponderosa', 24)

  Asteroid.containers = (asteroids, updatable, drawable)
  Player.containers = (updatable, drawable)
  AsteroidField.containers = (updatable)
  Shot.containers = (shots, updatable, drawable)

  high_score = load_highscore()

  game_over = False
  paused = False

  starfield = StarField(300)
  particle_system = ParticleSystem()
  audio_manager = AudioManager()

  AsteroidField()
  player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, particle_system, audio_manager)

  while (True):
    score_surface = my_font.render(str(player.score), (255,255,255), (0,0,0))
    lives_surface = info_font.render(f"Lives: {player.lives}", (255,255,255), (0,0,0))
    highscore_surface = info_font.render(f"High Score: {high_score}", (255,255,255), (0,0,0))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        if player.score > high_score:
          save_highscore(player.score)
        print(f"Final score: {player.score}")
        print(f"High score: {high_score}")
        return
      if event.type == pygame.KEYUP:
        player.reset_speed()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          paused = not paused

    if not paused:
      starfield.update(dt)
      particle_system.update(dt)

      updatable.update(dt)

      if not game_over:
        for item in asteroids:
          if item.check_collision(player):
            particle_system.create_explosion(player.position, num_particles=30, color=(255, 100, 100))
            if not player.take_damage():
              game_over = True
              if player.score > high_score:
                high_score = player.score
                save_highscore(high_score)

        for asteroid in asteroids:
          for shot in shots:
            if shot.check_collision(asteroid):
              particle_system.create_explosion(asteroid.position, num_particles=20)
              player.add_score(asteroid.get_score_value())
              asteroid.split()
              shot.kill()

    screen.fill("#000000")

    starfield.draw(screen)
    particle_system.draw(screen)

    for item in drawable:
      item.draw(screen)

    screen.blit(score_surface[0], (SCREEN_WIDTH/2, 50))
    screen.blit(lives_surface[0], (10, 10))
    screen.blit(highscore_surface[0], (SCREEN_WIDTH - 250, 10))

    if paused:
      pause_font = pygame.freetype.SysFont('Ponderosa', 48)
      pause_surface = pause_font.render("PAUSED", (255,255,0), (0,0,0))
      screen.blit(pause_surface[0], (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2))

    if game_over:
      game_over_font = pygame.freetype.SysFont('Ponderosa', 48)
      game_over_surface = game_over_font.render("GAME OVER", (255,0,0), (0,0,0))
      restart_surface = info_font.render("Press any key to restart", (255,255,255), (0,0,0))
      screen.blit(game_over_surface[0], (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 50))
      screen.blit(restart_surface[0], (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 10))

      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          return

    pygame.display.flip()
    dt = clock.tick(60) / 1000

if __name__ == "__main__":
  main()