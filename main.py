import pygame
from pygame.locals import *
from sys import exit
from model.menu import Menu

from character import Character

pygame.init()
pygame.display.set_caption("Run Away from Fat")
SCREEN_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(SCREEN_SIZE, 0, 32)


menu = Menu(SCREEN)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            menu.detect_press(pygame.mouse.get_pos())
        elif event.type == MOUSEBUTTONUP:
            menu.detect_drop(pygame.mouse.get_pos())

    menu.show()

    # ESSE TRECHO DE CÓDIGO DEVE IR PARA A INTERFACE
    # character = Character('Usain', SCREEN)
    # character.draw(50, 100)

    pygame.display.update()
