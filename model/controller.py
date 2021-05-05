import pygame
from pygame.locals import *
from model.pause_menu import PauseMenu
from model.corrida_de_obstaculos import CorridaDeObstaculos


class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.corrida_de_obstaculos = CorridaDeObstaculos(screen, "usaim", 10)
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

            corrida_result = self.corrida_de_obstaculos.corrida_obstaculo()
            if not corrida_result:
                self.on = False
