import pygame


class Menu:

    def __init__(self, screen, new_game=None, continue_game=None):
        self.width, self.height = pygame.display.get_surface().get_size()
        self.screen = screen
        self.new_game = new_game
        self.continue_game = continue_game

        self.continue_img = self.scale_it(pygame.image.load("img/menu/continuar-jogo.png").convert_alpha())
        self.new_img = self.scale_it(pygame.image.load("img/menu/novo-jogo.png").convert_alpha())
        self.leave_img = self.scale_it(pygame.image.load("img/menu/sair.png").convert_alpha())

    def continue_g(self, x, y):
        self.screen.blit(self.continue_img, (x, y))

    def new_g(self, x, y):
        self.screen.blit(self.new_img, (x, y))

    def leave_g(self, x, y):
        self.screen.blit(self.leave_img, (x, y))

    def show(self):
        bg = pygame.transform.scale(pygame.image.load("img/menu/background.png"), (self.width, self.height))
        self.screen.blit(bg, (0, 0))
        self.continue_g(self.width / 3, self.height / 5 * 2)
        self.new_g(self.width / 3, self.height / 5 * 3)
        self.leave_g(self.width / 3, self.height / 5 * 4)

    def press_continue(self):
        self.continue_img = self.scale_it(pygame.image.load(f"img/menu/continuar-jogo-pressed.png").convert_alpha())

    def drop_continue(self):
        self.continue_img = self.scale_it(pygame.image.load("img/menu/continuar-jogo.png").convert_alpha())

    def press_new(self):
        self.new_img = self.scale_it(pygame.image.load(f"img/menu/novo-jogo-pressed.png").convert_alpha())

    def drop_new(self):
        self.new_img = self.scale_it(pygame.image.load("img/menu/novo-jogo.png").convert_alpha())

    def press_leave(self):
        self.leave_img = self.scale_it(pygame.image.load("img/menu/sair-pressed.png").convert_alpha())

    def drop_leave(self):
        self.leave_img = self.scale_it(pygame.image.load("img/menu/sair.png").convert_alpha())

    def scale_it(self, img):
        return pygame.transform.scale(
            img,
            (int(self.width / 3), 64))

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
