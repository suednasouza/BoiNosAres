import pygame
from code.entity import Entity
from code.const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        self.bg_images = [
            pygame.image.load('./asset/Bg1.png').convert_alpha(),
            pygame.image.load('./asset/Bg2.png').convert_alpha()
        ]

        self.bg_images = [pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT)) for bg in self.bg_images]

        self.rects = [
            self.bg_images[0].get_rect(topleft=(0, 0)),
            self.bg_images[1].get_rect(topleft=(0, WIN_HEIGHT - self.bg_images[1].get_height())),
            self.bg_images[1].get_rect(topleft=(WIN_WIDTH, WIN_HEIGHT - self.bg_images[1].get_height()))
        ]

    def move(self):
        self.rects[1].x -= ENTITY_SPEED["Bg2"]
        self.rects[2].x -= ENTITY_SPEED["Bg2"]

        if self.rects[1].right <= 0:
            self.rects[1].left = self.rects[2].right

        if self.rects[2].right <= 0:
            self.rects[2].left = self.rects[1].right

    def draw(self, screen):
        screen.blit(self.bg_images[0], self.rects[0])
        screen.blit(self.bg_images[1], self.rects[1])
        screen.blit(self.bg_images[1], self.rects[2])
