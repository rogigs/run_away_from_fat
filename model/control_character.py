import pygame
import os
from pygame.locals import *
from utils.data_manipulation import Data

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT_DIR, 'img/new_game/usaim.png')


class Control_character():

    def __init__(self, person=None, days=None, coins=None, speed=None, stamina=None, resistance=None):
        self.person = person
        self.days = days
        self.coins = coins
        self.speed = speed
        self.stamina = stamina,
        self.resistance = resistance,

    def get_character(self, person):
        try:
            rows = Data.get_character(person)
            row = rows[0]

            self.person = row[0]
            self.days = row[1]
            self.coins = row[2]
            self.speed = row[3]
            self.stamina = row[4],
            self.resistance = row[5]

        except Exception as e:
            print('Erro ao buscar personagem {}'.format(e))
