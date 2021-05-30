import pygame
from pygame.locals import *
from model.corrida_de_obstaculos import CorridaDeObstaculos
from model.weight_lifting import Weight_lifting
from model.marathon import Marathon
from model.biking import  Biking
from utils.data_manipulation import Data


class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_surface().get_size()
        self.on = True

        self.minigame =  Weight_lifting(self.screen, Data.get_character()[0])

    def minigame_end(self, result, kind):
        if type(result) == int:
            Data.increase_day()
            back = pygame.Surface((self.width, self.height))
            back.set_alpha(215)
            back.fill((0, 0, 0))
            self.screen.blit(back, (0, 0))
            self.write(text=f"Fim do {Data.get_day()}º dia", size=48,where=(self.width/2, 300))
            self.write(text="Pressione <Enter> para continuar", size=32,
                       where=(self.width / 2, self.height / 2 + 200))

            if result > 0:
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
                        self.on = False
                        return
        elif not result:
            self.on = False

    def show_win_screen(self, result, kind):
        translation = {"resistance": "resistência", "speed": "velocidade", "strength": "força"}
        # title
        self.write(text="Você venceu!", size=72, color=(0, 255, 0), where=(self.width / 2, 100))
        # description
        if Data.get_status()[kind] <= 90:
            self.write(text=f"+{result} pontos de {translation[kind]} lhe foram atribuidos", size=32,
                       where=(self.width / 2, self.height / 2))
        else:
            self.write(text=f"Você alcançou o limite da {translation[kind]} humana", size=32,
                       where=(self.width / 2, self.height / 2 + 100))



    def write(self, text="", size=32, color=(255, 255, 255), where=(0, 0)):
        font = pygame.font.SysFont("FreePixel", size)
        content = font.render(text, True, color)
        self.screen.blit(content, (where[0] - content.get_width() / 2, where[1]))

    def show_loss_screen(self):
        # title
        self.write(text="Você perdeu!", size=72, color=(255, 0, 0), where=(self.width / 2, 100))
        # description
        self.write(text="Nenhum ponto de status lhe foi atribuido", size=32, where=(self.width / 2, self.height / 2 + 100))

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
            
            # marathon = Marathon(self.screen).marathon()

            # self.minigame_end(marathon, "")

            # corrida_result = CorridaDeObstaculos(self.screen).corrida_obstaculo(Data.get_character()[0],
            #                                                                     Data.get_status()["speed"])
            # # self.minigame_end(corrida_result, "speed")

            weight_lifting = self.minigame.weightlifting(Data.get_status()["strength"])
            self.minigame_end(weight_lifting, "strength")
            # # biking_result=Biking(self.screen).biking_minigame(Data.get_character()[0],
            #                                         Data.get_status()["resistance"])
            # self.minigame_end(biking_result, "resistance")

            
         


            corrida_result = CorridaDeObstaculos(self.screen).corrida_obstaculo(Data.get_character()[0],
                                                                                Data.get_status()["speed"])
            self.minigame_end(corrida_result, "speed")
            
        
            biking_result=Biking(self.screen).biking_minigame(Data.get_character()[0],
                                                    Data.get_status()["resistance"])
            self.minigame_end(biking_result, "resistance")
