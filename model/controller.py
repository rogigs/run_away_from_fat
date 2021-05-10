import pygame
from pygame.locals import *
from model.corrida_de_obstaculos import CorridaDeObstaculos
from utils.data_manipulation import Data


class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.corrida_de_obstaculos = CorridaDeObstaculos(screen, 10)
        self.on = True

    def minigame_end(self, result, kind):
        if type(result) == int:
            if result > 0:
                Data.increase_status(result, kind)
                self.show_win_screen(result, kind)
            else:
                self.show_loss_screen()
        elif not result:
            self.on = False

    def show_win_screen(self, result, kind):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    print("mousedown win")
                elif event.type == MOUSEBUTTONUP:
                    print("mouseup win")
            # print(result, kind)

    def write(self, text="", size=32, color=(255, 255, 255), where=(0, 0)):
        font = pygame.font.SysFont("FreePixel", size)
        content = font.render(text, True, color)
        self.screen.blit(content, (where[0] - content.get_width() / 2, where[1]))

    def show_loss_screen(self):
        back = pygame.Surface((self.width, self.height))
        back.set_alpha(215)
        back.fill((0, 0, 0))
        self.screen.blit(back, (0, 0))
        # title
        self.write(text="Você perdeu!", size=72, color=(255, 0, 0), where=(self.width / 2, 100))
        # description
        self.write(text="Nenhum ponto de status lhe foi atribuido.", size=32, where=(self.width / 2, self.height / 2))
        # instruction
        self.write(text="Pressione qualquer tecla para continuar.", size=32,
                   where=(self.width / 2, self.height / 2+50))

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYUP:
                    self.on = False
                    return

    def show(self):
        self.on = True
        while self.on:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    print("mousedown")
                elif event.type == MOUSEBUTTONUP:
                    print("mouseup")
            # corrida_result = self.corrida_de_obstaculos.corrida_obstaculo(Data.get_character()[0])
            corrida_result = 0
            self.minigame_end(corrida_result, "resistance")
