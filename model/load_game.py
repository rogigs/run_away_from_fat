import pygame
from pygame.locals import *

import config
from config import IMAGES_PATH, NEW_GAME_IMAGES_PATH
from model.controller import Controller
from utils.data_manipulation import Data
from utils.position import in_bounds


class LoadGame:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.bg = pygame.transform.scale(pygame.image.load(IMAGES_PATH + "bg.png"), (self.width, self.height))
        self.on = False
        self.saves = Data.get_saves()
        self.buttons = {
            "image": pygame.transform.scale(pygame.image.load("assets/img/fundo-cinza.png").convert_alpha(),
                                            (420, 50)),
            "image_pressed": pygame.transform.scale(
                pygame.image.load("assets/img/fundo-cinza-pressed.png").convert_alpha(),
                (420, 50)),
            "pressed": -1,
            "bounds": [
                [(self.width // 3, 275), (self.width // 3 + 420, 275 + 50)],
                [(self.width // 3, 350), (self.width // 3 + 420, 350 + 50)],
                [(self.width // 3, 425), (self.width // 3 + 420, 425 + 50)],
                [(self.width // 3, 500), (self.width // 3 + 420, 500 + 50)],
                [(self.width // 3, 575), (self.width // 3 + 420, 575 + 50)],
            ]}
        self.backbutton = {
            "pressed": False,
            "image": pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "voltar.png"), (80, 80)),
            "image_pressed": pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "voltar-pressed.png"),
                                                    (80, 80)),
            "bounds": [(16, 16),
                       (16 + 80, 16 + 80)]}

    def blit_buttons(self):
        font = pygame.font.Font("assets/font/FreePixel.ttf", 34)
        for index, save in enumerate(self.saves):
            button = self.buttons["bounds"][index]
            if index == self.buttons["pressed"]:
                self.screen.blit(self.buttons["image_pressed"], button[0])
            else:
                self.screen.blit(self.buttons["image"], button[0])
            content = font.render(f"{save[0]}, dia {save[2] + 1}", True, (0, 0, 0))
            place_text = (button[0][0] + (button[1][0] - button[0][0]) // 2,
                          button[0][1] + (button[1][1] - button[0][1]) // 2)
            self.screen.blit(content,
                             (place_text[0] - content.get_width() // 2, place_text[1] - content.get_height() // 2))

    def blit_title(self):
        font = pygame.font.Font("assets/font/FreePixel.ttf", 90)
        title = font.render("Selecione seu", True, (0, 0, 0))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        title = font.render("usuário", True, (0, 0, 0))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 130))

    def blit_backbutton(self):
        if self.backbutton["pressed"]:
            self.screen.blit(self.backbutton["image_pressed"], self.backbutton["bounds"][0])
        else:
            self.screen.blit(self.backbutton["image"], self.backbutton["bounds"][0])

    def handle_mousedown(self):
        pos = pygame.mouse.get_pos()
        for index, button in enumerate(self.buttons["bounds"]):
            if in_bounds(pos, button):
                self.buttons["pressed"] = index
        if in_bounds(pos, self.backbutton["bounds"]):
            self.backbutton["pressed"] = True

    def handle_mouseup(self):
        pos = pygame.mouse.get_pos()
        self.buttons["pressed"] = -1
        self.backbutton["pressed"] = False

        if in_bounds(pos, self.backbutton["bounds"]):
            self.on = False
        for index, button in enumerate(self.buttons["bounds"]):
            if in_bounds(pos, button):
                config.USERNAME = self.saves[index][0]
                Controller(self.screen).show()

    def show(self):
        self.on = True
        while self.on:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mousedown()
                elif event.type == MOUSEBUTTONUP:
                    self.handle_mouseup()
            self.screen.blit(self.bg, (0, 0))
            self.blit_title()
            self.blit_backbutton()
            self.blit_buttons()
            pygame.display.update()
