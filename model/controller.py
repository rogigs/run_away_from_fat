import pygame
from pygame.locals import *
from pygame.mixer import Sound
from model.corrida_de_obstaculos import CorridaDeObstaculos
from model.weight_lifting import WeightLifting
from model.marathon import Marathon
from model.biking import Biking
from utils.data_manipulation import Data


class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.on = True
        self.sound_status = True

    def change_sound_status(self):
        if self.sound_status == True:
            self.sound_status = False
        elif self.sound_status == False:
            self.sound_status = True

    def minigame_end(self, result, kind):
        if type(result) == int:
            Data.increase_day()
            back = pygame.Surface((self.width, self.height))
            back.set_alpha(215)
            back.fill((0, 0, 0))
            self.screen.blit(back, (0, 0))
            self.write(text=f"Fim do {Data.get_day()}º dia", size=48, where=(self.width / 2, 300))
            self.write(text="Pressione <Enter> para continuar", size=32,
                       where=(self.width / 2, self.height / 2 + 200))

            if result > 0:
                if kind != '':
                    Data.increase_status(result, kind)
                self.show_win_screen(result, kind)
            else:
                self.show_loss_screen()

            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == KEYUP and event.key == K_RETURN:
                        return
        elif not result:
            self.on = False

    def show_win_screen(self, result, kind):
        translation = {"resistance": "resistência", "speed": "velocidade", "strength": "força"}
        # title
        self.write(text="Você venceu!", size=72, color=(0, 255, 0), where=(self.width / 2, 100))
        # description
        if kind != "":
            if Data.get_status()[kind] <= 90:
                self.write(text=f"+{result} pontos de {translation[kind]} lhe foram atribuidos", size=32,
                           where=(self.width / 2, self.height / 2))
            else:
                self.write(text=f"Você alcançou o limite da {translation[kind]} humana", size=32,
                           where=(self.width / 2, self.height / 2 + 100))

    def write(self, text="", size=32, color=(255, 255, 255), where=(0, 0)):
        font = pygame.font.Font("assets/font/FreePixel.ttf", size)
        content = font.render(text, True, color)
        self.screen.blit(content, (where[0] - content.get_width() / 2, where[1]))

    def show_loss_screen(self):
        # title
        self.write(text="Você perdeu!", size=72, color=(255, 0, 0), where=(self.width / 2, 100))
        # description
        self.write(text="Nenhum ponto de status lhe foi atribuido", size=32,
                   where=(self.width / 2, self.height / 2 + 100))

    @classmethod
    def get_position(cls, time):
        if time >= 30:
            return 1
        elif time >= 25:
            return 2
        elif time >= 20:
            return 3
        return 0

    def marathon_result(self, time):
        if type(time) == int:
            Data.increase_day()
            back = pygame.Surface((self.width, self.height))
            back.set_alpha(215)
            back.fill((0, 0, 0))
            self.screen.blit(back, (0, 0))
            self.write(text=f"Fim da Maratona", size=72, where=(self.width / 2, 150))
            position = self.get_position(time)
            if position > 0:
                color = {1: (0, 255, 0), 2: (255, 255, 0), 3: (255, 128, 0)}
                self.write(text=f"{position}º Posição", size=48, where=(self.width / 2, 300), color=color[position])
                self.write(text=f"Você subiu no ranking!", size=38, where=(self.width / 2, 400))
                self.write(text=f"Sua próxima maratona será mais desafiadora!", size=38, where=(self.width / 2, 450))
            else:
                self.write(text=f"Você não alcançou o pódio.", size=48, where=(self.width / 2, 350), color=(255, 0, 0))
            self.write(text="Pressione <Enter> para voltar a treinar", size=32,
                       where=(self.width / 2, self.height / 2 + 200))
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == KEYUP and event.key == K_RETURN:
                        return
                pygame.display.update()
        self.on = False
        pygame.mixer.quit()

    def show(self):
        self.on = True
        while self.on:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    pass
                elif event.type == MOUSEBUTTONUP:
                    pass

            ex = Data.get_next_exercise()
            ex = "strength"
            if ex == "marathon":
                result, time, level = Marathon(self.screen).marathon(Data.get_character()[0], Data.get_status())
                self.marathon_result(time)
            elif ex == "resistance":
                biking_result = Biking(self.screen).biking_minigame(Data.get_character()[0],
                                                                    Data.get_status()["resistance"], self.sound_status)
                self.minigame_end(biking_result, "resistance")
            elif ex == "strength":
                weight_result = WeightLifting(self.screen, None).weightlifting(Data.get_status()["strength"],
                                                                               self.sound_status)
                self.minigame_end(weight_result, "strength")
            else:
                corrida_result = CorridaDeObstaculos(self.screen).corrida_obstaculo(Data.get_character()[0],
                                                                                    Data.get_status()["speed"],
                                                                                    self.sound_status)
                self.minigame_end(corrida_result, "speed")
