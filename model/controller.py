import pygame


class Controller:
    def __init__(self, screen):
        self.screen = screen

    def show(self):
        while True:

            self.screen.fill((255, 0, 0))
            pygame.display.update()
