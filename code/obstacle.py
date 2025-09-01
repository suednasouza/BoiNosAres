import pygame
import random
from code.const import OBSTACLE1, OBSTACLE2, WIN_HEIGHT

class Obstacle:
    def __init__(self, x, obstacle_type="fence", width=100, gap=150):
        self.type = obstacle_type
        self.width = width
        self.speed = 5

        if self.type == "fence":
            self.image = pygame.image.load(OBSTACLE1).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, random.randint(100, 300)))
            self.height = self.image.get_height()
            self.top_rect = None
            self.bottom_rect = pygame.Rect(x, WIN_HEIGHT - self.height, self.width, self.height)

        elif self.type == "cloud":
            cloud_width = random.randint(100, 200)
            self.image = pygame.image.load(OBSTACLE2).convert_alpha()
            self.image = pygame.transform.scale(self.image, (cloud_width, 150))
            self.top_rect = pygame.Rect(x, 0, cloud_width, self.image.get_height())
            self.bottom_rect = None

    def update(self):
        if self.top_rect:
            self.top_rect.x -= self.speed
        if self.bottom_rect:
            self.bottom_rect.x -= self.speed

    def draw(self, screen):
        if self.top_rect:
            screen.blit(self.image, self.top_rect)
        if self.bottom_rect:
            screen.blit(self.image, self.bottom_rect)

    def collide(self, player):
        collide_top = self.top_rect and player.rect.colliderect(self.top_rect)
        collide_bottom = self.bottom_rect and player.rect.colliderect(self.bottom_rect)
        return collide_top or collide_bottom

    def passed(self, player_x):
        x_pos = self.top_rect.x if self.top_rect else self.bottom_rect.x
        return player_x > x_pos + self.width
