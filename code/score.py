import pygame
import os
from pygame import Surface

class Score:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.font = pygame.font.SysFont("Arial", 36)
        self.record_file = "record.txt"
        self.clock = pygame.time.Clock()

        # Create record.txt if it does not exist
        if not os.path.exists(self.record_file):
            with open(self.record_file, "w") as f:
                f.write("0")

    def get_record(self):
        with open(self.record_file, "r") as f:
            return int(f.read().strip())

    def save(self, player_score):
        record = self.get_record()
        if player_score[0] > record:
            with open(self.record_file, "w") as f:
                f.write(str(player_score[0]))

    def show(self):
        record = self.get_record()
        running = True
        while running:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False

            record_text = self.font.render(f"High Score: {record}", True, (255, 255, 255))
            msg_text = self.font.render("Press ENTER to return", True, (200, 200, 200))

            self.screen.blit(record_text, (self.screen.get_width() // 2 - record_text.get_width() // 2, 250))
            self.screen.blit(msg_text, (self.screen.get_width() // 2 - msg_text.get_width() // 2, 320))

            pygame.display.flip()
