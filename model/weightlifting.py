import pygame, sys, random
from pygame.locals import *
from model.pause_menu import PauseMenu
from config import IMAGES_PATH, SOUNDS_PATH

class Weightlifting(PauseMenu):
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

    """
    When arrow arrived the end. It return for the begin
    """
    def _control_height(self):
        if self._height_machine <= 300 or self._height_player <= 300:
            self._height_machine = self._height_begin
            self._height_player = self._height_begin   

    def _control_velocity(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._height_player -= self._velocity_space 

        self._height_machine -= self._velocity   

    def weightlifting(self):
        self._clock.tick(30)
        
        bg_surface = pygame.image.load(IMAGES_PATH + "weightlifiting/bg.png").convert_alpha()
        bg_surface = pygame.transform.smoothscale( bg_surface, (1280, 720) )
    
        character = pygame.image.load(IMAGES_PATH + "weightlifiting/usaim_weight_down.png").convert_alpha()

        machine = pygame.image.load(IMAGES_PATH + "weightlifiting/machine_arrow.png").convert_alpha()
        user = pygame.image.load(IMAGES_PATH + "weightlifiting/user_arrow.png").convert_alpha()


        self._control_velocity()

        self.screen.blit(bg_surface, (0,0))
        self.screen.blit(character, (600, 0))
        self.screen.blit(user, [65, self._height_player])
        self.screen.blit(machine, [65, self._height_machine])

        pygame.draw.rect(self.screen,(169, 169, 169),[100, 300, 25, 400])
        pygame.draw.rect(self.screen,(9, 9, 169),[100, self._height_player + 25, 25, 400])

        self._control_height()

        pygame.display.flip()
        pygame.display.update()

                                            

