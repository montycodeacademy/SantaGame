import pygame
from pygame.locals import *
import sys
from simple_button import *

class control_panel(object):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, pause_button, resume_button, help_button, redraw_screen_cb):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.score_font = pygame.font.SysFont("comicsansms", 30)
        self.status_font = pygame.font.SysFont("comicsansms", 15)
        self.help_font = pygame.font.SysFont("comicsansms", 15)
        self.help_font.set_bold(True)
        self.backGround = pygame.image.load("png/background.png")
        self.background_music = pygame.mixer.Sound("sounds/background.wav")
        self.help_text = "Hit H - For Help"
        self.display_help = "Esc-Quit, P-Pause, H-Toggle"
        self.help_flag = True
        self.score = 0
        self.pause_btn = pause_button
        self.resume_btn = resume_button
        self.help_btn = help_button
        self.paused = False
        self.redraw_screen_fn = redraw_screen_cb

    def start_game(self):
        self.background_music.play(-1)

    def mousebuttonsclicked(self):
        pos = pygame.mouse.get_pos()
        if self.resume_btn.rect.collidepoint(pos):
            self.resume_btn.call_back()
        if self.help_btn.rect.collidepoint(pos):
            self.help_btn.call_back()
            self.redraw_screen_fn()


    def pause_game(self):
        self.background_music.fadeout(100)
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        self.quit_game()
                    elif event.key == K_c:
                        self.paused = False
                    elif event.key == K_h:
                        self.set_help_flag(not self.help_flag)
                        self.redraw_screen_fn()
                elif event.type == QUIT:
                    self.quit_game()
                elif event.type == MOUSEBUTTONDOWN:
                    self.mousebuttonsclicked()
                elif event.type == MOUSEMOTION:
                    self.redraw_screen_fn()

        self.background_music.play(-1)

    def draw(self, screen, status):
        score_text = self.score_font.render("Score: " + str(self.score), True, (0, 128, 0))
        screen.blit(score_text, (self.screen_width - 250, 50))
        if len(status):
            status_text = self.status_font.render("Status: " + status, True, (0, 0, 128))
            screen.blit(status_text, (self.screen_width - 250, 90))
        if self.help_flag:
            help_text = self.help_font.render(self.help_text, True, (255, 255, 0))
        else:
            help_text = self.help_font.render(self.display_help, True, (255, 255, 0))
        screen.blit(help_text, (self.screen_width - 250, 110))

    def set_help_flag(self, value):
        self.help_flag = value

    def get_help_flag(self):
        return self.help_flag

    def quit_game(self):
        self.background_music.stop()
        pygame.quit()
        sys.exit()