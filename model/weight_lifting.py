import pygame, sys, random
from pygame.locals import *
from model.pause_menu import PauseMenu
from config import IMAGES_PATH, SOUNDS_PATH

class Weight_lifting(PauseMenu):
    def __init__(self, screen, character, force):
        super().__init__(screen)
        self.character = character
        self.force = force

        self._clock = pygame.time.Clock()
        self._height_begin = 675
        self._height_machine = self._height_begin
        self._height_player = self._height_begin

        # TEM QUE SER DE ACOROD COM O LEVEL DA FORCE
        self._velocity = 1
        self._velocity_space = 50
        self.weight = 10

        self.show_tutor = True
        self.result_game = False         

    def _weight(self):
        myfont = pygame.font.SysFont('Arial', 50) 
        textsurface = myfont.render('{} Kg'.format(self.weight), False, (0, 0, 0))
        self.screen.blit(textsurface,(75,220))

    def _player_lose(self):
        game_lose = pygame.image.load(IMAGES_PATH + "weightlifiting/game_lose.png").convert_alpha()
        printt = game_lose.get_rect(center=(1280/2 - 25, 720/2 + 25))
        pygame.draw.rect(self.screen, [0, 0, 0], [284, 264, 633, 201])
        self.screen.blit(game_lose, (printt))

    def _player_win(self):
        game_lose = pygame.image.load(IMAGES_PATH + "weightlifiting/game_lose.png").convert_alpha()
        printt = game_lose.get_rect(center=(1280/2 - 25, 720/2 + 25))
        pygame.draw.rect(self.screen, [0, 0, 0], [284, 264, 633, 201])
        self.screen.blit(game_lose, (printt))
    
    """
    When arrow arrived the end. It return for the begin
    """
    def _control_height(self):
        if self._height_machine <= 300 or self._height_player <= 300:
            self.result_game = True
            self._height_machine = self._height_begin
            self._height_player = self._height_begin

    def _control_velocity_player(self):
        self._height_player -= self._velocity_space 

    def _control_velocity_machine(self):
        self._height_machine -= self._velocity   

    def _control_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.show_tutor and not self.result_game:
                            self._control_velocity_player()
                    if event.key == pygame.K_s:
                        self.show_tutor = False

    def _show_tutor(self):
        if self.show_tutor:
            tutorial = pygame.image.load(IMAGES_PATH + "weightlifiting/tutorial.png").convert_alpha()
            tutorial_print = tutorial.get_rect(center=(1280/2 - 25, 720/2 + 25))
            pygame.draw.rect(self.screen, [0, 0, 0], [284, 264, 633, 201])
            self.screen.blit(tutorial, (tutorial_print))

    def weightlifting(self):
        self._clock.tick(30)
        
        bg_surface = pygame.image.load(IMAGES_PATH + "weightlifiting/bg.png").convert_alpha()
        bg_surface = pygame.transform.smoothscale( bg_surface, (1280, 720) )
    
        character = pygame.image.load(IMAGES_PATH + "weightlifiting/usaim_weight_down.png").convert_alpha()

        machine = pygame.image.load(IMAGES_PATH + "weightlifiting/machine_arrow.png").convert_alpha()
        player = pygame.image.load(IMAGES_PATH + "weightlifiting/user_arrow.png").convert_alpha()

        self.screen.blit(bg_surface, (0,0))
        self.screen.blit(character, (600, 0))
        self.screen.blit(player, [65, self._height_player])
        self.screen.blit(machine, [65, self._height_machine])

        pygame.draw.rect(self.screen,(169, 169, 169),[100, 300, 25, 400])
        pygame.draw.rect(self.screen,(9, 9, 169),[100, self._height_player + 25, 25, 400])

        self._weight()



        self._control_events()
        
        if self.show_tutor:
            self._show_tutor()
        
        if not self.show_tutor and not self.result_game:
            self._control_velocity_machine()

        self._control_height()

        if self.result_game:
            if self._height_machine == self._height_begin:
                self._player_lose()
            if self._height_player == self._height_begin:
                self._player_win()

        pygame.display.flip()
        pygame.display.update()

        pygame.font.init()
   

