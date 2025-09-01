import pygame
from code.entity import Entity
from code.const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SPEED


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # Carregar as imagens de fundo
        self.bg_images = [
            pygame.image.load('./asset/Bg1.png').convert_alpha(),  # Céu (Fixo)
            pygame.image.load('./asset/Bg2.png').convert_alpha()  # Grama (Movimentando)
        ]

        # Redimensiona as imagens para o tamanho da tela
        self.bg_images = [pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT)) for bg in self.bg_images]

        # Define as posições das imagens de fundo
        self.rects = [
            self.bg_images[0].get_rect(topleft=(0, 0)),  # Bg1 (Céu) - Fixo
            self.bg_images[1].get_rect(topleft=(0, WIN_HEIGHT - self.bg_images[1].get_height())),  # Bg2 (Grama)
            self.bg_images[1].get_rect(topleft=(WIN_WIDTH, WIN_HEIGHT - self.bg_images[1].get_height()))
            # 2ª imagem de Bg2 (Grama)
        ]

    def move(self):
        # Movimenta o chão/grama (Bg2) mais rapidamente
        self.rects[1].x -= ENTITY_SPEED["Bg2"]
        self.rects[2].x -= ENTITY_SPEED["Bg2"]

        # Quando a primeira imagem do chão sair da tela, reposiciona
        if self.rects[1].right <= 0:
            self.rects[1].left = self.rects[2].right

        # Quando a segunda imagem do chão sair da tela, reposiciona
        if self.rects[2].right <= 0:
            self.rects[2].left = self.rects[1].right

    def draw(self, screen):
        # Desenha o céu (Bg1) fixo
        screen.blit(self.bg_images[0], self.rects[0])

        # Desenha as imagens do chão/grama (Bg2)
        screen.blit(self.bg_images[1], self.rects[1])
        screen.blit(self.bg_images[1], self.rects[2])
