import pygame
from pygame.locals import *
from sys import exit

pygame.init()
SCREEN_SIZE =(800,600)
SCREEN = pygame.display.set_mode(SCREEN_SIZE, 0 ,32)
mouse_x, mouse_y = 0, 0
pos_x, mov_x = 0, 1
while True:
    SCREEN.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.rect(SCREEN, (255, 0, 0), (mouse_x, mouse_y, 50 , 80))
    
    pos_x += mov_x

    if pos_x < 0:
        mov_x = 1
    if pos_x > 800:
        mov_x = -1

    pygame.draw.circle(SCREEN, (0, 255, 0), [pos_x, 30], 35) 
    
    pygame.display.update()
