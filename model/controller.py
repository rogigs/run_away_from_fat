import pygame
from pygame.locals import *
from model.pause_menu import PauseMenu


class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.pause_menu = PauseMenu(screen)
        self.on = True
        self.pause = True

    def show(self):
        self.on = True
        while self.on:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    print("mousedown")
                elif event.type == MOUSEBUTTONUP:
                    print("mouseup")

            if self.pause:
                self.on = self.pause_menu.show_pause()
