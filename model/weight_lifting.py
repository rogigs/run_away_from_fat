import pygame, sys, random
from pygame.locals import *
from model.hud import HUD
from config import IMAGES_PATH, SOUNDS_PATH
from utils.position import in_bounds

class Weight_lifting(HUD):
    def __init__(self, screen, character):
        super().__init__(screen)
        self.character = character

        self._clock = pygame.time.Clock()
        self._height_begin = 675
        self._height_machine = self._height_begin
        self._height_player = self._height_begin

        # TEM QUE SER DE ACOROD COM O LEVEL DA FORCE
        self._velocity = 1
        self._velocity_space = 50
        self.weight = 10

        self.show_tutor = True
        self._end_game = False     
        self._player_win = None    

    def _weight(self):
        myfont = pygame.font.SysFont('Arial', 50) 
        textsurface = myfont.render('{} Kg'.format(self.weight), False, (0, 0, 0))
        self.screen.blit(textsurface,(75,220))
    
    def detect_mousedown(self, pos):
        if in_bounds(pos, self.pause_bounds):
            self.press_pause_button()

    def detect_mouseup(self, pos):
        if in_bounds(pos, self.pause_bounds):
            return self.show_pause()
        self.reset_imgs()
        return True

    """
    When arrow arrived the end. It return for the begin
    """
    def _control_height(self):
        if self._height_machine <= 300 :
            self._end_game = True
            self._player_win = False
            self._height_machine = self._height_begin
            self._height_player = self._height_begin
        if self._height_player <= 300:
            self._end_game = True
            self._player_win = True
            self._height_machine = self._height_begin
            self._height_player = self._height_begin
    
    def _control_velocity_player(self):
        character = pygame.image.load(IMAGES_PATH + "weightlifiting/usaim_weight_medium.png").convert_alpha()
        self.screen.blit(character, (600, 0))
        self._height_player -= self._velocity_space 

    def _control_velocity_machine(self):
        self._height_machine -= self._velocity   

    def _control_events(self, metal_sound):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.show_tutor:
                            self._control_velocity_player()
                            metal_sound.play()
                    if event.key == pygame.K_s:
                        self.show_tutor = False
            if event.type == MOUSEBUTTONDOWN:
                self.detect_mousedown(pygame.mouse.get_pos())
            elif event.type == MOUSEBUTTONUP:
                result = self.detect_mouseup(pygame.mouse.get_pos())
                if not result:
                    pygame.mixer.quit()
                    return False

    def _show_tutor(self):
        if self.show_tutor:
            tutorial = pygame.image.load(IMAGES_PATH + "weightlifiting/tutorial.png").convert_alpha()
            tutorial_print = tutorial.get_rect(center=(1280/2 - 25, 720/2 + 25))
            pygame.draw.rect(self.screen, [0, 0, 0], [284, 264, 633, 201])
            self.screen.blit(tutorial, (tutorial_print))
            
    def _result_game(self):
        if self._player_win:
            self._player_win = None
            return 10
        self._player_win = None
        return 0

    # ACHAR UM JEITO MELHOR DE FAZER ISSO
    def _difficult(self, strength):
        if strength > 20:
            self._velocity = 2
            self._velocity_space = 40
            self.weight = 30
        if strength > 50:
            self._velocity = 3
            self._velocity_space = 35
            self.weight = 70  
        if strength > 70:
            self._velocity = 4
            self._velocity_space = 30
            self.weight = 100 
    
    def weightlifting(self, strength):
        self._end_game = False
        self._difficult(strength)
        pygame.mixer.music.load(SOUNDS_PATH+'gym/back.mp3')
        pygame.mixer.music.play(-1)
        metal_sound = pygame.mixer.Sound(SOUNDS_PATH+'gym/metal.wav')
        while not self._end_game:
            self._clock.tick(30)
            
            bg_surface = pygame.image.load(IMAGES_PATH + "weightlifiting/bg.png").convert_alpha()
            bg_surface = pygame.transform.smoothscale( bg_surface, (1280, 720) )

            if self._height_player < 400:
                character = pygame.image.load(IMAGES_PATH + "weightlifiting/usaim_weight_up.png").convert_alpha()
            else:
                character = pygame.image.load(IMAGES_PATH + "weightlifiting/usaim_weight_down.png").convert_alpha()

            player = pygame.image.load(IMAGES_PATH + "weightlifiting/machine_arrow.png").convert_alpha()
            machine = pygame.image.load(IMAGES_PATH + "weightlifiting/user_arrow.png").convert_alpha()

            self.screen.blit(bg_surface, (0,0))
            self.screen.blit(character, (600, 0))
            self.screen.blit(player, [65, self._height_player])
            self.screen.blit(machine, [65, self._height_machine])

            pygame.draw.rect(self.screen,(169, 169, 169),[100, 300, 25, 400])
            pygame.draw.rect(self.screen,(255, 0, 0),[100, self._height_player + 25, 25, 400])

            self._weight()

            self._control_events(metal_sound)
            
            if self.show_tutor:
                self._show_tutor()
            
            if not self.show_tutor and not self._end_game:
                self._control_velocity_machine()

            self._control_height()

            if self._end_game:
                break
               
            self.show_status()
            self.show_pause_button()

            
            pygame.display.flip()
            pygame.display.update()

            pygame.font.init()
            
        return self._result_game()
    