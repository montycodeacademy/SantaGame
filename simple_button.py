import pygame

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
DARK_GREY = (128, 128, 128)
BLACK = (0, 0, 0)

class simple_button(object):
    def __init__(self, txt, location, action, bg = WHITE, fg = BLACK, size=(80,30), \
                 font_name="Segoe Print", font_size=10):
        self.color = bg
        self.bg = bg
        self.fg = fg
        self.size = size
        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center = [s//2 for s in self.size])
        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center =location)
        self.call_back_fn = action
        self.active = True

    def get_active(self):
        return self.active
    def set_active(self, flag):
        self.active = flag

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY

    def call_back(self):
        if self.active:
            self.call_back_fn()

    def draw(self, screen):
        if not self.active:
            self.bg = DARK_GREY
        else:
            self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

