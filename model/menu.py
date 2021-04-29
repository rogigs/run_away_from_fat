import pygame
from config import MENU_IMAGES_PATH


class Menu:

    def __init__(self, screen, new_game=None, continue_game=None):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.new_game = new_game
        self.continue_game = continue_game

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
        bg = pygame.transform.scale(pygame.image.load(MENU_IMAGES_PATH + "background.png"), (self.width, self.height))
        self.screen.blit(bg, (0, 0))
        self.continue_g(self.width / 3, self.height / 5 * 2)
        self.new_g(self.width / 3, self.height / 5 * 3)
        self.leave_g(self.width / 3, self.height / 5 * 4)

    def press_continue(self):
        """Changes 'continuar' image to its pressed version."""
        self.continue_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo-pressed.png").convert_alpha())

    def drop_continue(self):
        """Changes 'continuar' image to its unpressed version."""
        self.continue_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo.png").convert_alpha())

    def press_new(self):
        """Changes 'Novo jogo' image to its pressed version."""
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo-pressed.png").convert_alpha())

    def drop_new(self):
        """Changes 'Novo jogo' image to its unpressed version."""
        self.new_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "novo-jogo.png").convert_alpha())

    def press_leave(self):
        """Changes 'Sair' image to its pressed version."""
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair-pressed.png").convert_alpha())

    def drop_leave(self):
        """Changes 'Novo jogo' image to its unpressed version."""
        self.leave_img = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair.png").convert_alpha())

    def scale_it(self, img):
        return pygame.transform.scale(
            img,
            (int(self.width / 3), 100))

    def detect_press(self, pos):
        x, y = pos
        # for continue button
        if (self.width / 3 <= x <= self.width / 3 + self.continue_img.get_width() and
                self.height / 5 <= y <= self.height / 5 * 2 + self.continue_img.get_height()):
            self.press_continue()
        # for new game
        elif (self.width / 3 <= x <= self.width / 3 + self.new_img.get_width() and
              self.height / 5 <= y <= self.height / 5 * 3 + self.new_img.get_height()):
            self.press_new()
        elif (self.width / 3 <= x <= self.width / 3 + self.leave_img.get_width() and
              self.height / 5 <= y <= self.height / 5 * 4 + self.leave_img.get_height()):
            self.press_leave()

    def detect_drop(self):
        self.drop_leave()
        self.drop_new()
        self.drop_continue()
