import pygame
import os
from pygame.locals import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT_DIR, 'apagar.png')

class Character():

    def __init__(self, character,  screen):
        if character == 'Usain':
            self.character = pygame.image.load(PATH).convert()
        else:
            self.character = 'Radcliffe'
        self.screen = screen

    def draw(self, x, y):
        return self.screen.blit(self.character, (x, y))
