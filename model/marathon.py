import pygame, sys, random
from pygame.locals import *
from model.hud import HUD
from config import IMAGES_PATH, SOUNDS_PATH

class Marathon(HUD):
    def __init__(self, screen):
        super().__init__(screen) 

        self._clock = pygame.time.Clock()
        self._size_screen = self.screen.get_rect()
        
        self._velocity = 10
        self._images = {
            "character": [True, "marathon/usaim_run_1.png", "marathon/usaim_run_2.png"],
            "runner1": [True, "marathon/usaim_run_1.png", "marathon/usaim_run_2.png"],
            "runner2": [True, "marathon/usaim_run_1.png", "marathon/usaim_run_2.png"],
        }

        self._pos_y_obstacles = 100
        self._pos_y_background = 0
        self._pos_x_character =  self._size_screen[2]/2
        
        self._control_effect_runner = True
        
        self._random_number_adversary = 1
        self._random_pos_adversary = random.randint(0, 2)
        self._random_pos_adversary_aux = self._random_pos_adversary
        self._pos_x_adversary = [self._pos_x_character - 270, self._pos_x_character - 70, self._pos_x_character + 130]
        self._aux_pos_y_adversary = 0

    def _control_pos_y_obstacles(self):
        if self._pos_y_obstacles > self._size_screen[3]:
            self._random_number_adversary = random.randint(1, 2)
            self._random_pos_adversary = random.randint(0, 2)
            self._random_pos_adversary_aux = random.randint(0, 2)
            while self._random_pos_adversary == self._random_pos_adversary_aux:
                self._random_pos_adversary_aux = random.randint(0, 2)
            
            self._aux_pos_y_adversary = random.randint(0, 5)
            if self._aux_pos_y_adversary == 5:
                self._aux_pos_y_adversary -= 200
            else:
                self._aux_pos_y_adversary = 0
            
            self._pos_y_obstacles = 0

    def _draw_adversary(self):
        if self._random_number_adversary == 1:
            self.screen.blit(self._effect_runner("runner1"), [self._pos_x_adversary[self._random_pos_adversary] , self._pos_y_obstacles])
        else:
            self.screen.blit(self._effect_runner("runner1"), [self._pos_x_adversary[self._random_pos_adversary], self._pos_y_obstacles])
            self.screen.blit(self._effect_runner("runner2"), [self._pos_x_adversary[self._random_pos_adversary_aux] , self._pos_y_obstacles + self._aux_pos_y_adversary])


    def _obstacles(self):
        self._control_pos_y_obstacles()
        self._draw_adversary()
        
    def _control_events(self): 
        if pygame.key.get_pressed()[pygame.K_LEFT]:
                self._pos_x_character -= 20
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self._pos_x_character += 20
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self._pos_x_character -= 20
                if event.key == pygame.K_RIGHT:
                    self._pos_x_character += 20

        if self._pos_x_character > 900:
            self._pos_x_character = 900
        if self._pos_x_character < self._size_screen[2]/2 - 250:
            self._pos_x_character = self._size_screen[2]/2 - 250

    def _colision(self):
        if (self._pos_x_character == self._pos_y_obstacles) and self._pos_x_character == self._size_screen[3] - 100:
            print("BATEU")
        else:
            self._pos_y_obstacles += self._velocity        

    def _effect_runner(self, who):
        if self._images[who][0]:
            sprite = pygame.image.load(IMAGES_PATH + self._images[who][1]).convert_alpha()
            sprite = pygame.transform.smoothscale( sprite, (120, 100) )
            self._images[who][0] = False
        else:
            sprite = pygame.image.load(IMAGES_PATH + self._images[who][2]).convert_alpha()
            sprite = pygame.transform.smoothscale( sprite, (120, 100) )
            self._images[who][0] = True
        return sprite

    def marathon(self):   
        while True:
            self._pos_y_background -= self._velocity

            self._clock.tick(10)
                   
           
            
            track = pygame.image.load(IMAGES_PATH + "marathon/track.png").convert_alpha()
            outside_track = pygame.image.load(IMAGES_PATH + "marathon/outside.png").convert_alpha()
            
            self.screen.blit(outside_track, [0, self._pos_y_background])
            self.screen.blit(outside_track, [900, self._pos_y_background])        
            self.screen.blit(track, (self._size_screen[2]/2 - 300, 0))

            if self._pos_y_background < -100:
                self._pos_y_background = 0


            self.screen.blit(self._effect_runner("character"), [self._pos_x_character - 70 , self._size_screen[3] - 100 ])

            self._obstacles()

            self._colision()

            self._control_events()
     
            pygame.display.update()
            pygame.display.flip()


        return 0
    