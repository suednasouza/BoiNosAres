import pygame
import random
from code.player import Player
from code.background import Background
from code.obstacle import Obstacle
from code.const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED

class Level:
    def __init__(self, screen, name: str, player_score: list):
        self.screen = screen
        self.name = name
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()

        # Player inicializado no meio da tela, ajustando altura
        temp_player = Player("Player", (50, 0))
        self.player = Player("Player", (50, WIN_HEIGHT//2 - temp_player.surf.get_height()//2))

        # Obstacles
        self.obstacles = []

        # Background (4 imagens lado a lado)
        self.backgrounds = [
            Background("Bg1", (0, 0)),
            Background("Bg2", (WIN_WIDTH, 0)),
            Background("Bg3", (WIN_WIDTH*2, 0)),
            Background("Bg4", (WIN_WIDTH*3, 0)),
        ]

        # Score
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 32)

        # High Score
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0

    def draw_scores(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255,255,255))
        current_score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))

        self.screen.blit(high_score_text, (10,10))
        self.screen.blit(current_score_text, (10,50))

    def run(self, player_score: list):
        pygame.mixer.music.load('./asset/Game.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            self.clock.tick(60)
            self.screen.fill((0,0,0))

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.jump()

            # Background
            for bg in self.backgrounds:
                bg.move()
                bg.draw(self.screen)

            # Player
            self.player.move()
            self.player.draw(self.screen)

            # Spawn de obstáculos fora da tela
            if not self.obstacles or \
               (self.obstacles[-1].top_rect and self.obstacles[-1].top_rect.x < self.width - 200) or \
               (self.obstacles[-1].bottom_rect and self.obstacles[-1].bottom_rect.x < self.width - 200):

                obstacle_type = random.choice(["fence","cloud"])
                self.obstacles.append(Obstacle(self.width + 100, obstacle_type=obstacle_type))

            # Atualiza obstáculos
            for obs in self.obstacles:
                obs.update()
                obs.draw(self.screen)

                if obs.collide(self.player):
                    running = False

                if obs.passed(self.player.rect.x):
                    self.score += 1

            # Remove obstáculos fora da tela
            self.obstacles = [
                obs for obs in self.obstacles
                if (obs.top_rect and obs.top_rect.x + obs.width > 0) or
                   (obs.bottom_rect and obs.bottom_rect.x + obs.width > 0)
            ]

            # Checa se player morreu
            if self.player.is_dead(WIN_HEIGHT):
                running = False

            # Desenha scores
            self.draw_scores()

            # Atualiza tela
            pygame.display.flip()

        # Salva score final
        player_score[0] = self.score
        return False
