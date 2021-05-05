import pygame
from pygame.locals import *
from config import PAUSE_PATH, MENU_IMAGES_PATH
from utils.position import in_bounds


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.img_continue, self.img_menu, self.img_leave, self.img_pause = None, None, None, None
        self.pause = False
        self.reset_imgs()
        self.continue_bounds = (
            (self.width // 2 - self.img_continue.get_width() // 2, 250),
            (self.img_continue.get_width() + self.width // 2 - self.img_continue.get_width() // 2,
             self.img_continue.get_height() + 250)
        )
        self.menu_bounds = (
            (self.width // 2 - self.img_continue.get_width() // 2, 250 + self.img_continue.get_height() * 1.5),
            (self.width // 2 - self.img_continue.get_width() // 2 + self.img_continue.get_width(),
             250 + self.img_continue.get_height() * 1.5 + self.img_continue.get_height())
        )
        self.leave_bounds = (
            (self.width // 2 - self.img_leave.get_width() // 2, 250 + self.img_leave.get_height() * 3),
            (self.width // 2 - self.img_leave.get_width() // 2 + self.img_leave.get_width(),
             250 + self.img_leave.get_height() * 3 + self.img_leave.get_width())
        )
        self.pause_bounds = (
            (16, 16),
            (16 + self.img_pause.get_width(),
             16 + self.img_pause.get_height())
        )

    def show_pause_button(self):
        self.screen.blit(self.img_pause, self.pause_bounds[0])

    def show_title(self):
        img = pygame.transform.scale(pygame.image.load(PAUSE_PATH + "title-pause.png"),
                                     (int(self.width / 12 * 7), int(self.height / 5)))
        self.screen.blit(img, (self.width / 2 - img.get_width() / 2, 50))

    def show_continue(self):
        self.screen.blit(self.img_continue, self.continue_bounds[0])

    def show_go_menu(self):
        self.screen.blit(self.img_menu, self.menu_bounds[0])

    def show_leave(self):
        self.screen.blit(self.img_leave,
                         self.leave_bounds[0])

    def scale_it(self, img):
        """Adjust buttons to be a third of screen with 100 oh height."""
        return pygame.transform.scale(
            img,
            (int(self.width / 3), 100))

    def show_pause(self):
        self.pause = True
        back = pygame.Surface((self.width, self.height))
        back.set_alpha(128)
        back.fill((0, 0, 0))
        self.screen.blit(back, (0, 0))
        while self.pause:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.process_mousedown(pygame.mouse.get_pos())
                elif event.type == MOUSEBUTTONUP:
                    action = self.process_mouseup(pygame.mouse.get_pos())
                    if action == "menu":
                        self.pause = False
                        return False
                    elif action == "continue":
                        self.pause = False
                        return True
            self.show_title()
            self.show_continue()
            self.show_go_menu()
            self.show_leave()
            pygame.display.update()

    def process_mousedown(self, pos):
        print("hi")
        if self.pause:
            if in_bounds(pos, self.continue_bounds):
                self.img_continue = self.scale_it(
                    pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo-pressed.png").convert_alpha())
            elif in_bounds(pos, self.menu_bounds):
                self.img_menu = self.scale_it(pygame.image.load(PAUSE_PATH + "menu-pressed.png").convert_alpha())
            elif in_bounds(pos, self.leave_bounds):
                self.img_leave = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair-pressed.png").convert_alpha())

    def process_mouseup(self, pos):
        if self.pause:
            self.reset_imgs()
            if in_bounds(pos, self.leave_bounds):
                pygame.quit()
                exit()
            elif in_bounds(pos, self.continue_bounds):
                return "continue"
            elif in_bounds(pos, self.menu_bounds):
                return "menu"

    def press_pause_button(self):
        self.img_pause = pygame.transform.scale(pygame.image.load(PAUSE_PATH + "pause-pressed.png").convert_alpha(),
                                                (64, 64))

    def reset_imgs(self):
        self.img_continue = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "continuar-jogo.png").convert_alpha())
        self.img_menu = self.scale_it(pygame.image.load(PAUSE_PATH + "menu.png").convert_alpha())
        self.img_leave = self.scale_it(pygame.image.load(MENU_IMAGES_PATH + "sair.png").convert_alpha())
        self.img_pause = pygame.transform.scale(pygame.image.load(PAUSE_PATH + "pause.png").convert_alpha(), (64, 64))
