import pygame
from pygame import Surface, Rect, font
from pygame.font import Font

from code.const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_GREEN, C_RED
from code.player import Player
from code.background import Background
from code.obstacle import Obstacle
from code.score import Score

class Level:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.bg1 = Background("Bg1", (0, 0))
        self.bg2 = Background("Bg1", (WIN_WIDTH, 0))
        self.obstacles = []
        self.spawn_timer = 30
        self.player = Player("Player", (100, WIN_HEIGHT // 2))
        self.score_manager = Score(window)

    def spawn_obstacles(self):
        import random
        x = WIN_WIDTH + 10
        if random.choice([True, False]):
            self.obstacles.append(Obstacle(x, "cloud"))
        else:
            self.obstacles.append(Obstacle(x, "fence"))

    def reset_game(self):
        self.player = Player("Player", (100, WIN_HEIGHT // 2))
        self.obstacles = []
        self.spawn_timer = 0
        self.bg1 = Background("Bg1", (0, 0))
        self.bg2 = Background("Bg1", (WIN_WIDTH, 0))

    def game_over_screen(self, player_score):
        pygame.mixer.music.stop()
        self.score_manager.save(player_score)

        font_large = pygame.font.SysFont("Lucida Sans Typewriter", 48)
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 28)
        game_over_text = font_large.render("GAME OVER", True, C_RED)
        score_text = font_small.render(f"Final Score: {player_score}", True, C_WHITE)
        play_again_text = font_small.render("Press ENTER to Play Again or ESC to Exit", True, C_WHITE)

        self.window.fill((135, 206, 235))
        self.bg1.draw(self.window)
        self.bg2.draw(self.window)
        self.window.blit(game_over_text, (WIN_WIDTH // 2 - game_over_text.get_width() // 2, WIN_HEIGHT // 3))
        self.window.blit(score_text, (WIN_WIDTH // 2 - score_text.get_width() // 2, WIN_HEIGHT // 2))
        self.window.blit(play_again_text, (WIN_WIDTH // 2 - play_again_text.get_width() // 2, WIN_HEIGHT // 1.5))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        return False

    def run(self, player_score=0):
        pygame.mixer.music.load('./asset/Game.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        running = True
        difficulty_level = 0
        difficulty_timer = 0
        font_score = font.SysFont("Arial", 28)

        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            # Aumenta dificuldade a cada 10 segundos (~600 frames)
            difficulty_timer += 1
            if difficulty_timer % 600 == 0:
                difficulty_level += 1

            self.bg1.move()
            self.bg2.move()
            self.player.move()

            # Game Over por sair da tela
            if self.player.is_dead(WIN_HEIGHT):
                restart = self.game_over_screen(player_score)
                if restart:
                    self.reset_game()
                    player_score = 0
                    pygame.mixer.music.play(-1)
                    continue
                else:
                    break

            self.spawn_timer += 1
            if self.spawn_timer >= max(20, 60 - difficulty_level):
                self.spawn_obstacles()
                self.spawn_timer = 0

            for obs in self.obstacles:
                obs.update()
                if obs.collide(self.player):
                    restart = self.game_over_screen(player_score)
                    if restart:
                        self.reset_game()
                        player_score = 0
                        pygame.mixer.music.play(-1)
                        break
                    else:
                        running = False
                        break
                if obs.passed(self.player.rect.x):
                    player_score += 1

            # Remove obstáculos fora da tela
            self.obstacles = [obs for obs in self.obstacles if (obs.top_rect and obs.top_rect.right > 0) or
                              (obs.bottom_rect and obs.bottom_rect.right > 0)]

            # --- Renderização ---
            self.window.fill((135, 206, 235))
            self.bg1.draw(self.window)
            self.bg2.draw(self.window)
            for obs in self.obstacles:
                obs.draw(self.window)
            self.player.draw(self.window)

            # Mostra High Score e Score atual
            high_score = self.score_manager.get_record()
            high_score_text = font_score.render(f"High Score: {high_score}", True, (255, 255, 0))
            self.window.blit(high_score_text, (20, 20))

            score_text = font_score.render(f"Score: {player_score}", True, (255, 255, 255))
            self.window.blit(score_text, (20, 50))

            pygame.display.flip()

        return True

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
