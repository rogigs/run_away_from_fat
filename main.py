import pygame
from pygame.locals import *
from sys import exit
from model.menu import Menu

pygame.init()
SCREEN_SIZE = (1280, 720)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

menu = Menu(screen)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            menu.detect_press(pygame.mouse.get_pos())
        elif event.type == MOUSEBUTTONUP:
            menu.detect_drop()

    menu.show()


    pygame.display.update()
