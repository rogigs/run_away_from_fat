import pygame
from pygame.locals import *
from sys import exit

from character import Character

pygame.init()
SCREEN_SIZE = (800, 600)
SCREEN = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # ESSE TRECHO DE CÓDIGO DEVE IR PARA A INTERFACE
    character = Character('Usain', SCREEN)
    character.draw(50, 100)

    pygame.display.update()
