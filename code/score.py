import pygame
import os
from pygame import Surface


class Score:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)
        self.record_file = "record.txt"

        if not os.path.exists(self.record_file):
            with open(self.record_file, "w") as f:
                f.write("0")

    def get_record(self):
        with open(self.record_file, "r") as f:
            return int(f.read().strip())

    def save(self, player_score):
        record = self.get_record()
        if player_score > record:
            with open(self.record_file, "w") as f:
                f.write(str(player_score))

    def show(self):
        record = self.get_record()
        record_text = self.font.render(f"High Score: {record}", True, (255, 255, 255))
        self.screen.blit(record_text, (self.screen.get_width() // 2 - record_text.get_width() // 2, 250))
        pygame.display.flip()
