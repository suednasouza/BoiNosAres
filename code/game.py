import sys
import pygame

from code.menu import Menu
from code.level import Level
from code.score import Score

from code.const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Boi nos Ares 🐂✈️")

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == "PLAY":
                player_score = [0]  # apenas um jogador
                level = Level(self.window, "Level1", player_score)
                level_return = level.run(player_score)

                if level_return:  # se ganhou / passou
                    score.save(player_score)

            elif menu_return == "SCORE":
                score.show()

            elif menu_return == "EXIT":
                pygame.quit()
                sys.exit()
