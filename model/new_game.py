import pygame
from pygame.locals import *
from utils.position import in_bounds
from utils.data_manipulation import Data
from config import NEW_GAME_IMAGES_PATH


class NewGame:

    def __init__(self, screen, bg):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.bg = bg
        self.on = True
        self.usaim, self.radcliffe, self.backbutton = None, None, None

        self.reset_imgs()
        self.usaim_bounds = [
            (self.width // 2 - self.usaim.get_width() - 32, self.height // 2 - 32),
            (self.width // 2 - 32, self.height // 2 - 32 + self.usaim.get_height())
        ]
        self.radcliffe_bounds = [
            (self.width // 2 + 32, self.height // 2 - 32),
            (self.width // 2 + self.radcliffe.get_width() + 32, self.height // 2 - 32 + self.radcliffe.get_height())
        ]

        self.backbutton_bounds = [
            (16, 16),
            (16 + self.backbutton.get_width(), 16 + self.backbutton.get_height())
        ]
        self.input_field = {
            "image": pygame.transform.scale(pygame.image.load("assets/img/fundo-cinza-pressed.png").convert_alpha(),
                                            (420, 50)),
            "bounds": [
                (self.width // 3, 225),
                (self.width // 3 * 2, 275),
            ],
            "content": ""
        }

    def show_usaim(self):
        self.screen.blit(self.usaim, self.usaim_bounds[0])

    def show_radcliffe(self):
        self.screen.blit(self.radcliffe, self.radcliffe_bounds[0])

    def show_backbutton(self):
        self.screen.blit(self.backbutton, self.backbutton_bounds[0])

    def show_title(self):
        img = pygame.image.load(NEW_GAME_IMAGES_PATH + "selecione-personagem.png").convert_alpha()
        img = pygame.transform.scale(img, (self.width // 3 * 2, 180))
        render_img = img.get_rect().center = self.width // 2 - img.get_width() // 2, 32
        self.screen.blit(img, render_img)

    def show_input(self):
        font = pygame.font.Font("assets/font/FreePixel.ttf", 32)
        text = font.render("Nome: " + self.input_field["content"], False, (0, 0, 0))
        self.screen.blit(self.input_field["image"], self.input_field["bounds"][0])
        self.screen.blit(text, (self.input_field["bounds"][0][0] + 12, self.input_field["bounds"][0][1] + 12))

    def handle_typing(self, event):
        if event.key == K_BACKSPACE:
            self.input_field["content"] = self.input_field["content"][:-1]
        elif len(self.input_field["content"]) < 19:
            self.input_field["content"] += event.unicode

    def show(self):
        self.on = True
        while self.on:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.process_mousedown(pygame.mouse.get_pos())
                elif event.type == MOUSEBUTTONUP:
                    result = self.process_mouseup(pygame.mouse.get_pos())
                    if result == "created":
                        return "created"
                    elif result == "back":
                        return "back"
                elif event.type == KEYDOWN:
                    self.handle_typing(event)

            self.screen.blit(self.bg, (0, 0))
            self.show_input()
            self.show_usaim()
            self.show_radcliffe()
            self.show_backbutton()
            self.show_title()
            pygame.display.update()

    def process_mousedown(self, pos):
        if in_bounds(pos, self.usaim_bounds):
            self.usaim = pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "usaim-pressed.png"),
                                                (int(self.width / 6), int(self.height / 13 * 6)))
        if in_bounds(pos, self.radcliffe_bounds):
            self.radcliffe = pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "radcliffe-pressed.png"),
                                                    (int(self.width / 6), int(self.height / 13 * 6)))
        if in_bounds(pos, self.backbutton_bounds):
            self.backbutton = pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "voltar-pressed.png"),
                                                     (80, 80))

    def process_mouseup(self, pos):
        self.reset_imgs()
        if in_bounds(pos, self.usaim_bounds):
            Data.create_new_person("U")
            return "created"
        if in_bounds(pos, self.radcliffe_bounds):
            Data.create_new_person("R")
            return "created"
        if in_bounds(pos, self.backbutton_bounds):
            return "back"

    def reset_imgs(self):
        self.usaim = pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "usaim.png"),
                                            (int(self.width / 6), int(self.height / 13 * 6)))
        self.radcliffe = pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "radcliffe.png"),
                                                (int(self.width / 6), int(self.height / 13 * 6)))
        self.backbutton = pygame.transform.scale(pygame.image.load(NEW_GAME_IMAGES_PATH + "voltar.png"), (80, 80))
