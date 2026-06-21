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

  try:
    with open('highscore.txt', 'r') as f:
      high_score = int(f.read())
  except:
    high_score = 0

  # Multiplayer game state
  game_over = False
  paused = False
  multiplayer_mode = True  # Sempre modo multiplayer agora

  # Sistema Multiplayer
  players = []
  starfield = StarField(300)
  particle_system = ParticleSystem()
  audio_manager = AudioManager()

  AsteroidField()

  # Criar dois jogadores com cores diferentes
  player1 = Player(SCREEN_WIDTH/3, SCREEN_HEIGHT/2, particle_system, audio_manager, player_id=1, color="cyan")
  player2 = Player(2*SCREEN_WIDTH/3, SCREEN_HEIGHT/2, particle_system, audio_manager, player_id=2, color="yellow")

  players = [player1, player2]

  while (True):
    # Multiplayer HUD - calcular scores e vidas de todos os jogadores
    p1_score = players[0].score if len(players) > 0 else 0
    p2_score = players[1].score if len(players) > 1 else 0
    p1_lives = players[0].lives if len(players) > 0 else 0
    p2_lives = players[1].lives if len(players) > 1 else 0

    # Surfaces para HUD
    p1_score_surface = info_font.render(f"P1: {p1_score}", (0,255,255), (0,0,0))  # Cyan
    p2_score_surface = info_font.render(f"P2: {p2_score}", (255,255,0), (0,0,0))   # Yellow
    p1_lives_surface = info_font.render(f"Vidas: {p1_lives}", (0,255,255), (0,0,0))
    p2_lives_surface = info_font.render(f"Vidas: {p2_lives}", (255,255,0), (0,0,0))
    highscore_surface = info_font.render(f"High Score: {high_score}", (255,255,255), (0,0,0))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # Salvar high score geral (máximo entre jogadores)
        max_score = max([p.score for p in players] + [0])
        if max_score > high_score:
          with open('highscore.txt', 'w') as f:
            f.write(str(max_score))
        print(f"Final scores: {[p.score for p in players]}")
        print(f"High score: {high_score}")
        return
      if event.type == pygame.KEYUP:
        # Reset speed para todos os jogadores
        for player in players:
          player.reset_speed()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          paused = not paused

    if not paused:
      starfield.update(dt)
      particle_system.update(dt)

      updatable.update(dt)

      if not game_over:
        # Verificar colisões com todos os jogadores
        for player in players:
          for item in asteroids:
            if item.check_collision(player):
              particle_system.create_explosion(player.position, num_particles=30, color=(255, 100, 100))
              if not player.take_damage():
                # Jogador perdeu todas as vidas
                pass

        # Verificar game over (quando todos os jogadores estiverem sem vidas)
        alive_players = [p for p in players if p.is_alive()]
        if len(alive_players) == 0:
          game_over = True
          # Verificar high score
          max_score = max([p.score for p in players] + [0])
          if max_score > high_score:
            high_score = max_score
            with open('highscore.txt', 'w') as f:
              f.write(str(high_score))

        # Verificar colisões de tiros com asteroides
        for asteroid in asteroids:
          for shot in shots:
            if shot.check_collision(asteroid):
              particle_system.create_explosion(asteroid.position, num_particles=20)

              # Dar pontos ao jogador que fez o tiro
              if hasattr(shot, 'owner') and shot.owner in players:
                shot.owner.add_score(asteroid.get_score_value())

              asteroid.split()
              shot.kill()

    screen.fill("#000000")

    starfield.draw(screen)
    particle_system.draw(screen)

    # Desenhar todos os objetos (incluindo jogadores e tiros)
    for item in drawable:
      item.draw(screen)

    # Multiplayer HUD
    # P1 (canto superior esquerdo)
    screen.blit(p1_score_surface[0], (10, 10))
    screen.blit(p1_lives_surface[0], (10, 35))

    # P2 (canto superior direito)
    p2_score_rect = p2_score_surface[0].get_rect()
    p2_score_rect.topright = (SCREEN_WIDTH - 10, 10)
    screen.blit(p2_score_surface[0], p2_score_rect)

    p2_lives_rect = p2_lives_surface[0].get_rect()
    p2_lives_rect.topright = (SCREEN_WIDTH - 10, 35)
    screen.blit(p2_lives_surface[0], p2_lives_rect)

    # High score (centro superior)
    highscore_rect = highscore_surface[0].get_rect()
    highscore_rect.centerx = SCREEN_WIDTH // 2
    highscore_rect.top = 10
    screen.blit(highscore_surface[0], highscore_rect)

    if paused:
      pause_font = pygame.freetype.SysFont('Ponderosa', 48)
      pause_surface = pause_font.render("PAUSED", (255,255,0), (0,0,0))
      screen.blit(pause_surface[0], (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2))

    if game_over:
      game_over_font = pygame.freetype.SysFont('Ponderosa', 48)

      # Determinar o vencedor
      scores = [(i+1, p.score) for i, p in enumerate(players)]
      scores.sort(key=lambda x: x[1], reverse=True)
      winner_text = ""

      if len(scores) >= 2:
        if scores[0][1] > scores[1][1]:
          winner_text = f"JOGADOR {scores[0][0]} VENCEU!"
        elif scores[0][1] < scores[1][1]:
          winner_text = f"JOGADOR {scores[1][0]} VENCEU!"
        else:
          winner_text = "EMPATE!"

      game_over_surface = game_over_font.render("GAME OVER", (255,0,0), (0,0,0))
      if winner_text:
        winner_surface = game_over_font.render(winner_text, (255,255,0), (0,0,0))
      restart_surface = info_font.render("Press any key to restart", (255,255,255), (0,0,0))

      # Mostrar scores finais
      final_scores = []
      for i, player in enumerate(players):
        score_text = f"P{i+1}: {player.score} pontos"
        final_scores.append(info_font.render(score_text, player.color, (0,0,0)))

      screen.blit(game_over_surface[0], (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 100))
      if winner_text:
        screen.blit(winner_surface[0], (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 - 60))

      # Desenhar scores finais
      y_offset = SCREEN_HEIGHT/2 - 20
      for i, score_surface in enumerate(final_scores):
        score_rect = score_surface[0].get_rect()
        score_rect.centerx = SCREEN_WIDTH // 2
        score_rect.top = y_offset + (i * 30)
        screen.blit(score_surface[0], score_rect)

      screen.blit(restart_surface[0], (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 60))

      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          return

    pygame.display.flip()
    dt = clock.tick(60) / 1000

if __name__ == "__main__":
  main()