from abc import ABC, abstractmethod
import pygame

class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        try:
            self.surf = pygame.image.load(f'./asset/{name}.png').convert_alpha()
        except Exception as e:
            print(f"Erro ao carregar {name}.png: {e}")
            # Cria superfície de fallback
            self.surf = pygame.Surface((50,50))
            self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(topleft=position)
        self.vel = 0

    @abstractmethod
    def move(self):
        pass

    def draw(self, tela):
        tela.blit(self.surf, self.rect)
