import pygame
from pygame.locals import *
from utils.position import in_bounds
from utils.data_manipulation import Data


class NewGame:

    def __init__(self, screen, bg):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.bg = bg
        self.on = True

        self.usaim = pygame.transform.scale(pygame.image.load("img/new_game/usaim.png"),
                                            (int(self.width / 5), int(self.height / 5 * 2)))
        self.usaim_bounds = [
            (self.width / 5, self.height / 5 * 2),
            (self.width / 5 + self.usaim.get_width(),
             self.height / 5 * 2 + self.usaim.get_height())
        ]

    def show_usaim(self):
        self.screen.blit(self.usaim, self.usaim_bounds[0])

    def show(self):
        self.on = True
        while self.on:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.process_mousedown(pygame.mouse.get_pos())
                elif event.type == MOUSEBUTTONUP:
                    self.process_mouseup(pygame.mouse.get_pos())
            self.screen.blit(self.bg, (0, 0))
            self.show_usaim()
            pygame.display.update()

    def process_mousedown(self, pos):
        if in_bounds(pos, self.usaim_bounds):
            self.usaim = pygame.transform.scale(pygame.image.load("img/new_game/usaim-pressed.png"),
                                                (int(self.width / 5), int(self.height / 5 * 2)))

    def process_mouseup(self, pos):
        if in_bounds(pos, self.usaim_bounds):
            self.usaim = pygame.transform.scale(pygame.image.load("img/new_game/usaim.png"),
                                                (int(self.width / 5), int(self.height / 5 * 2)))
            Data.create_new_person("U")
            self.on = False
