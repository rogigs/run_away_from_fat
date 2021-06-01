from os import close, stat
import pygame, sys, random
from pygame.locals import *
from model.hud import HUD
from config import IMAGES_PATH, SOUNDS_PATH
from utils.position import in_bounds

class Marathon(HUD):
    def __init__(self, screen):
        super().__init__(screen) 

        self.show_tutor = True
        self._character = "usaim"

        self._clock = pygame.time.Clock()
        self._time_clock = 12
        self._time_clock_initial = self._time_clock
        self._CLOCKTICK = pygame.USEREVENT+3
        self._temporizador = 60
        self._initial_temp = self._temporizador

        self._size_screen = self.screen.get_rect()
        
        self._number_velocity = 20
        self._velocity = self._number_velocity

        self._images = {
            "character": [True, "marathon/" + self._character + "_run_1.png", "marathon/usaim_run_2.png"],
            "runner1": [True, "marathon/usaim_run_1.png", "marathon/usaim_run_2.png"],
            "runner2": [True, "marathon/usaim_run_1.png", "marathon/usaim_run_2.png"],
        }

        self._pos_y_obstacles = 100
        self._pos_y_boost = 100
        self._pos_y_obstacles_aux = [0 , 0]

        self._pos_y_obstacles_aux = self._pos_y_obstacles
        self._pos_y_background = 0
        self._pos_x_character =  self._size_screen[2]/2
        
        self._control_effect_runner = True
        
        self._random_number_adversary = 1
        self._random_pos_adversary = random.randint(0, 2)
        self._random_pos_adversary_aux = self._random_pos_adversary
        self._if_random_boost = random.randint(0, 5)
        self._random_pos_boost = random.randint(0, 2)
        self._pos_x_adversary = [self._pos_x_character - 270, self._pos_x_character - 70, self._pos_x_character + 130]
        self._pos_y_obstacles_aux = [0 , 0]

        self._boost = False
        self._aux_boost = 0

        self.end_game = 0
        self.quit = False
        self._end_game_value = 10


    def detect_mousedown(self, pos):
        if in_bounds(pos, self.pause_bounds):
            self.press_pause_button()

    def detect_mouseup(self, pos):
        if in_bounds(pos, self.pause_bounds):
            return self.show_pause()
        self.reset_imgs()
        return True

    def _control_game_state(self):
        if self._pos_y_obstacles > self._size_screen[3]:
            self._random_number_adversary = random.randint(1, 2)
            self._random_pos_adversary = random.randint(0, 2)
            self._random_pos_adversary_aux = random.randint(0, 2)
            self._if_random_boost = random.randint(0, 3)
            self._random_pos_boost = random.randint(0, 2)

            if self._random_number_adversary == 1:
                self._random_pos_adversary_aux = -1
            else:
                while self._random_pos_adversary == self._random_pos_adversary_aux:
                    self._random_pos_adversary_aux = random.randint(0, 2)
            
            while self._random_pos_adversary == self._random_pos_boost or self._random_pos_adversary_aux == self._random_pos_boost:
                    self._random_pos_boost = random.randint(0, 2)
                    
            
            if self._boost:  
                self._aux_boost += 1
                self._time_clock = 0            
                if self._aux_boost > 3:
                    self._aux_boost = 0
                    self._boost = False
                    self._time_clock = self._time_clock_initial
                    self._velocity = self._number_velocity
                else:
                    self._velocity = self._number_velocity * 10

            self._pos_y_obstacles = 0
            self._pos_y_boost = 0
            self._pos_y_obstacles_aux = [0 , 0]

            self.end_game += 1
    
    def _draw_finished(self, line):
        line_finish = pygame.image.load(IMAGES_PATH + "marathon/line_finish.png").convert_alpha()
        if line != 400:
            self.screen.blit(line_finish, [self._size_screen[2]/2 - 300, line ])
        else:
            self.screen.blit(line_finish, [self._size_screen[2]/2 - 300, 400 ])

                
    def _draw_boost(self):
        if self._if_random_boost == 3:
            flash = pygame.image.load(IMAGES_PATH +"marathon/flash.png").convert_alpha()
            flash = pygame.transform.smoothscale( flash, (100, 100) )
            
            if self._random_number_adversary == 1:
                self._random_pos_adversary_aux = -1
            
            self.screen.blit(flash, [self._pos_x_adversary[self._random_pos_boost] , self._pos_y_boost])

    def _draw_adversary(self):
        if self._random_number_adversary == 1:
            self.screen.blit( self._effect_runner("runner1"), [self._pos_x_adversary[self._random_pos_adversary] , self._pos_y_obstacles])
        else:
            self.screen.blit(self._effect_runner("runner1"), [self._pos_x_adversary[self._random_pos_adversary], self._pos_y_obstacles + self._pos_y_obstacles_aux[0]])
            self.screen.blit(self._effect_runner("runner2"), [self._pos_x_adversary[self._random_pos_adversary_aux] , self._pos_y_obstacles + self._pos_y_obstacles_aux[1]])


    def _obstacles(self):
        self._control_game_state()
        if self.end_game <= self._end_game_value:
            self._draw_boost()
            self._draw_adversary()
    
    def _events_button_pause(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.detect_mousedown(pygame.mouse.get_pos())
        elif event.type == MOUSEBUTTONUP:
            result = self.detect_mouseup(pygame.mouse.get_pos())
            if not result:
                pygame.mixer.quit()
                self.quit = True

    def _control_events(self): 
        if not self.show_tutor:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self._pos_x_character -= self._velocity * 0.8
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self._pos_x_character += self._velocity * 0.8
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self._pos_x_character -= self._velocity * 0.8
                    if event.key == pygame.K_RIGHT:
                        self._pos_x_character += self._velocity * 0.8
                if event.type == self._CLOCKTICK:
                    self._temporizador -= 1
                self._events_button_pause(event)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.show_tutor = False
            
            self._events_button_pause(event)

        if self._pos_x_character > 900:
            self._pos_x_character = 900
        if self._pos_x_character < self._size_screen[2]/2 - 250:
            self._pos_x_character = self._size_screen[2]/2 - 250

    def _pista(self):
        #left
        if self._pos_x_character > 320 and self._pos_x_character < 520 and self._pos_y_obstacles + 20 > self._size_screen[3] - 100:
            return [320, 520]
        #middle
        elif self._pos_x_character > 540 and self._pos_x_character < 740  and self._pos_y_obstacles + 20 > self._size_screen[3] - 100:
            return [540, 740]
        #right
        elif self._pos_x_character > 760 and self._pos_x_character < 960 and self._pos_y_obstacles + 20 > self._size_screen[3] - 100:
            return [760, 960]
        else:
            return [0,0]
            
    def _who_colision(self, who):
        if self._random_pos_adversary == who:
            self._pos_y_obstacles_aux[1] += self._velocity
        else:
            self._pos_y_obstacles_aux[0] += self._velocity
    
    def _colision_boost(self, left, right, sound, state):
        if left == 320 and right == 520 and self._random_pos_boost == 0:
            self._pos_y_boost = -900
            self._boost = True
            if state==True:
                sound.play()
        elif left == 540 and right == 740 and self._random_pos_boost == 1:
            self._pos_y_boost = -900
            self._boost = True 
            if state==True:
                sound.play()
        #right
        elif left == 760 and right == 960 and self._random_pos_boost == 2:
            self._pos_y_boost = -900
            self._boost = True
            if state==True:
                sound.play()
        else:
            self._boost = False
            
    def _colision(self, music, sound):
        adversary_left = (self._random_pos_adversary == 0 or self._random_pos_adversary_aux == 0 ) 
        adversary_middle = (self._random_pos_adversary == 1 or self._random_pos_adversary_aux == 1 ) 
        adversary_right = (self._random_pos_adversary == 2 or self._random_pos_adversary_aux == 2 ) 

        [left, right] = self._pista()

        if self._if_random_boost == 3:
            self._colision_boost(left, right, music,sound)

        if self._random_number_adversary == 1:
            self._random_pos_adversary_aux = -1
        #left
        if left == 320 and right == 520 and adversary_left:
            self._velocity = self._number_velocity / 3
            self._who_colision(0)
        #middle
        elif left == 540 and right == 740 and adversary_middle:
            self._velocity = self._number_velocity / 3
            self._who_colision(1)
        #right
        elif left == 760 and right == 960 and adversary_right:
            self._velocity = self._number_velocity / 3
            self._who_colision(2)
        else:
            self._velocity = self._number_velocity
            self._pos_y_obstacles += self._velocity 
            self._pos_y_boost += self._velocity        


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
    
    def _show_tutor(self):
        if self.show_tutor:
            tutorial = pygame.image.load(IMAGES_PATH + "weightlifiting/tutorial.png").convert_alpha()
            tutorial_print = tutorial.get_rect(center=(1280/2 - 25, 720/2 + 25))
            pygame.draw.rect(self.screen, [0, 0, 0], [284, 264, 633, 201])
          
            self.screen.blit(tutorial, (tutorial_print))

    def _control_character(self, character):
        if character == "U":
            self._character = "usaim"
        else:
            self._character = "rad"

    def _control_difficult(self, status):
        print(status)
        resistance = status["resistance"]
        speed = status["speed"]
        strength = status["strength"]
        difficult = "facil_demais"
        if strength > 20 and resistance > 20 and speed > 20:
            self._number_velocity = 25
            self._time_clock = 14
            self._end_game_value = 12
            difficult = "facil"
        if strength > 50 and resistance > 50 and speed > 20:
            self._number_velocity = 35
            self._time_clock = 20
            difficult = "medio"
            self._end_game_value = 15
        if strength > 70 and resistance > 70 and speed > 20:
            self._number_velocity = 45
            self._time_clock = 25
            self._end_game_value = 20
            difficult = "dificil"
        
        return difficult

    def marathon(self, character, status,sound): 
        font = pygame.font.Font("assets/font/FreePixel.ttf", 40)
        pygame.time.set_timer(self._CLOCKTICK, 1000)    
        
        pos_y_finish = 0 
        line = 0
        if sound == True:
            pygame.mixer.init()
            pygame.mixer.music.load(SOUNDS_PATH+'marathon/background.mp3')
            pygame.mixer.music.play(-1)
        boost_sound = pygame.mixer.Sound(SOUNDS_PATH+'marathon/boost.wav')
        
        self._control_character(character)
        difficult = self._control_difficult(status)
        
        while True:
            self._pos_y_background -= self._velocity

            self._clock.tick(self._time_clock)
                   
            track = pygame.image.load(IMAGES_PATH + "marathon/track.png").convert_alpha()
            outside_track = pygame.image.load(IMAGES_PATH + "marathon/outside.png").convert_alpha()
            
            self.screen.blit(outside_track, [0, self._pos_y_background])
            self.screen.blit(outside_track, [900, self._pos_y_background])        
            self.screen.blit(track, (self._size_screen[2]/2 - 300, 0))

            if self._pos_y_background < -100:
                self._pos_y_background = 0

             # WINNER
            """
                Return result, Time, level
            """
            if self.end_game > self._end_game_value:                     
                line += self._velocity
                self._draw_finished(line)
                pos_y_finish += self._velocity
                if self._size_screen[3] - 100 - pos_y_finish < 200:
                    return  10, self._temporizador, difficult
    
            character = self._effect_runner("character")
            self.screen.blit(character, [self._pos_x_character - 70 , self._size_screen[3] - 100 - pos_y_finish ])

            self._control_events()
            
            if self.show_tutor:
                self._show_tutor()
            else:
                if self.end_game <= self._end_game_value:
                    timer1 = font.render('Tempo ' + str(self._temporizador), True, (0, 0, 0))
                    self.screen.blit(timer1, (120, 30))    

                    self._obstacles()

                    self._colision(boost_sound,sound)
    

            self.show_pause_button()


            pygame.display.update()
            pygame.display.flip()


            # LOSE
            """
                Return result, Time, level
            """
            if self._temporizador == 0 and self.end_game < self._end_game_value:
                return 0, self._temporizador, difficult
            elif self.quit:
                return None, None, None
                
