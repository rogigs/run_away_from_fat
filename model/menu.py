import pygame
from utils.data_manipulation import Data
from model.new_game import NewGame
from config import MENU_IMAGES_PATH, IMAGES_PATH
from model.control_character import Control_character
from model.controller import Controller


class Menu:
    def __init__(self, screen):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.bg = pygame.transform.scale(pygame.image.load(IMAGES_PATH + "bg.png"), (self.width, self.height))
        self.title = pygame.transform.scale(pygame.image.load(MENU_IMAGES_PATH + "titulo.png"),
                                            (int(self.width / 12 * 7), int(self.height / 5)))
        self.new_game = NewGame(screen, self.bg)
        self.controller = Controller(screen)

        self.has_save = Data.has_save()
        self.continue_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo.png").convert_alpha())
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo.png").convert_alpha())
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair.png").convert_alpha())
        self.sound_img = pygame.transform.scale( pygame.image.load(MENU_IMAGES_PATH + "sound_on.png").convert_alpha(), (215, 150))
        self.sound_status = True

    def change_sound_status(self):
        if self.sound_status == True:
            self.sound_img = pygame.transform.scale(pygame.image.load(MENU_IMAGES_PATH + "sound_off.png").convert_alpha(), (215, 150))
            self.controller.change_sound_status()
        elif self.sound_status == False:
            self.sound_img = pygame.transform.scale(pygame.image.load(MENU_IMAGES_PATH + "sound_on.png").convert_alpha(), (215, 150))
            self.controller.change_sound_status()

    def sound(self, x, y):
        """Shows sound button"""
        self.screen.blit(self.sound_img, (x, y))

    def continue_g(self, x, y):
        """Shows 'continuar' button"""
        c = Control_character()
        c.get_character('U')
        self.screen.blit(self.continue_img, (x, y))

    def new_g(self, x, y):
        """Shows 'Novo Jogo' button"""
        self.screen.blit(self.new_img, (x, y))

    def leave_g(self, x, y):
        """Shows 'Sair' button"""
        self.screen.blit(self.leave_img, (x, y))

    def show(self):
        """Show menu."""
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.title, (self.width / 2 - self.title.get_width() / 2, 50))
        if self.has_save:
            self.continue_g(self.width / 3, self.height / 5 * 2)
        self.new_g(self.width / 3, self.height / 5 * 3)
        self.leave_g(self.width / 3, self.height / 5 * 4)
        self.sound(1050, 550)

    def press_continue(self):
        """Changes 'continuar' image to its pressed version."""
        self.continue_img = self.scale_it(
            pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo-pressed.png").convert_alpha())

    def drop_continue(self):
        """Changes 'continuar' image to its unpressed version."""
        self.controller.show()

    def press_new(self):
        """Changes 'Novo jogo' image to its pressed version."""
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo-pressed.png").convert_alpha())

    def drop_new(self):
        """Changes 'Novo jogo' image to its unpressed version. And go to person creation."""
        result = self.new_game.show()
        self.has_save = Data.has_save()

        if result == "created":
            self.controller.show()

    def press_leave(self):
        """Changes 'Sair' image to its pressed version."""
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair-pressed.png").convert_alpha())

    def drop_leave(self):
        """Changes 'Novo jogo' image to its unpressed version and quit game."""
        pygame.quit()
        exit()

    def scale_it(self, img):
        """Adjust buttons to be a third of screen with 100 oh height."""
        return pygame.transform.scale(
            img,
            (int(self.width / 3), 100))

    def detect_press(self, pos):
        """Detect presses on buttons."""

        x, y = pos
        if (self.width / 3 <= x <= self.width / 3 + self.continue_img.get_width() and
                self.height / 5 * 2 <= y <= self.height / 5 * 2 + self.continue_img.get_height()):
            self.press_continue()

        elif (self.width / 3 <= x <= self.width / 3 + self.new_img.get_width() and
              self.height / 5 * 3 <= y <= self.height / 5 * 3 + self.new_img.get_height()):
            self.press_new()

        elif (self.width / 3 <= x <= self.width / 3 + self.leave_img.get_width() and
              self.height / 5 * 4 <= y <= self.height / 5 * 4 + self.leave_img.get_height()):
            self.press_leave()

    def detect_drop(self, pos):
        """Detect drop on buttons."""
        self.reset_imgs()
        x, y = pos
        if (self.width / 3 <= x <= self.width / 3 + self.continue_img.get_width() and
                self.height / 5 * 2 <= y <= self.height / 5 * 2 + self.continue_img.get_height()):
            self.drop_continue()
        elif (self.width / 3 <= x <= self.width / 3 + self.new_img.get_width() and
              self.height / 5 * 3 <= y <= self.height / 5 * 3 + self.new_img.get_height()):
            self.drop_new()
        elif (1050 <= x <=1050+self.sound_img.get_width() and 
               550 <= y <= 550+self.sound_img.get_height()):
            self.change_sound_status()
            print(self.controller.sound_status) 
        elif (self.width / 3 <= x <= self.width / 3 + self.leave_img.get_width() and
              self.height / 5 * 4 <= y <= self.height / 5 * 4 + self.leave_img.get_height()):
            self.drop_leave()

    def reset_imgs(self):
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo.png").convert_alpha())
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair.png").convert_alpha())
        self.continue_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo.png").convert_alpha())
