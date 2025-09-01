from code.entity import Entity
import pygame


class Player(Entity):
    base_surf = None

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        if not Player.base_surf:
            Player.base_surf = pygame.transform.scale(self.surf, (80, 60))
        self.surf = Player.base_surf
        self.rect = self.surf.get_rect(topleft=position)
        self.vel = 0
        self.gravity = 0.5
        self.jump_power = -8

    def move(self):
        self.vel += self.gravity
        self.rect.y += self.vel

    def jump(self):
        self.vel = self.jump_power

    def is_dead(self, screen_height):
        # player morre apenas se sair da tela
        return self.rect.top < 0 or self.rect.bottom > screen_height
