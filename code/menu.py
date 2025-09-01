import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WIN_WIDTH, WIN_HEIGHT, C_WHITE, C_YELLOW, C_GREEN


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(left=0, top=0)
        self.clock = pygame.time.Clock()

    def run(self):
        pygame.mixer.music.load('./asset/Menu.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        state = "menu"
        options = ["PLAY", "EXIT"]
        selected = 0

        while True:
            self.clock.tick(60)
            self.window.blit(self.surf, self.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "EXIT"

                if state == "menu":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            selected = (selected - 1) % len(options)
                        elif event.key == pygame.K_DOWN:
                            selected = (selected + 1) % len(options)
                        elif event.key == pygame.K_RETURN:
                            if options[selected] == "PLAY":
                                state = "instructions"
                            else:
                                return "EXIT"

                elif state == "instructions":
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        return "PLAY"

            if state == "menu":
                self.draw_text(60, "Boi nos Ares", C_WHITE, (WIN_WIDTH / 2, 70))

                for i, option in enumerate(options):
                    color = C_GREEN if i == selected else (255, 255, 255)
                    x = WIN_WIDTH // 2
                    y = WIN_HEIGHT // 2 + i * 60
                    self.draw_text(40, option, color, (x, y))

            elif state == "instructions":
                self.draw_text(40, "Press SPACE to fly", C_WHITE, (WIN_WIDTH//2, 130))
                self.draw_text(40, "The objective is to avoid obstacles", C_WHITE, (WIN_WIDTH//2, 220))
                self.draw_text(40, "(fences and clouds)", C_WHITE, (WIN_WIDTH//2, 270))
                self.draw_text(30, "Press SPACE or ENTER to start", C_YELLOW, (WIN_WIDTH//2, 450))

            pygame.display.flip()

    def draw_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
