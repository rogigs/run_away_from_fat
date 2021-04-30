import pygame
from config import MENU_IMAGES_PATH
from utils.data_manipulation import Data
from model.new_game import NewGame
from config import MENU_IMAGES_PATH, IMAGES_PATH


class Menu:
    def __init__(self, screen, continue_game=None):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.bg = pygame.transform.scale(pygame.image.load(IMAGES_PATH + "bg.png"), (self.width, self.height))
        self.title = pygame.transform.scale(pygame.image.load(MENU_IMAGES_PATH + "titulo.png"),
                                            (int(self.width / 12 * 7), int(self.height / 5)))
        self.continue_game = continue_game
        self.new_game = NewGame(screen, self.bg)

        self.has_save = Data.has_save()
        self.continue_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo.png").convert_alpha())
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo.png").convert_alpha())
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair.png").convert_alpha())

    def continue_g(self, x, y):
        """Shows 'continuar' button"""
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

    def press_continue(self):
        """Changes 'continuar' image to its pressed version."""
        self.continue_img = self.scale_it(
            pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo-pressed.png").convert_alpha())

    def drop_continue(self):
        """Changes 'continuar' image to its unpressed version."""
        pass

    def press_new(self):
        """Changes 'Novo jogo' image to its pressed version."""
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo-pressed.png").convert_alpha())

    def drop_new(self):
        """Changes 'Novo jogo' image to its unpressed version. And go to person creation."""
        self.new_game.show()

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
        elif (self.width / 3 <= x <= self.width / 3 + self.leave_img.get_width() and
              self.height / 5 * 4 <= y <= self.height / 5 * 4 + self.leave_img.get_height()):
            self.drop_leave()

    def reset_imgs(self):
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo.png").convert_alpha())
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair.png").convert_alpha())
        self.continue_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo.png").convert_alpha())
