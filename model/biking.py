import pygame, sys, random
from pygame.locals import *
import time
from config import IMAGES_PATH, SOUNDS_PATH
from model.hud import HUD
from utils.position import in_bounds


class Biking(HUD):
    def __init__(self, screen):

        super().__init__(screen)

    def detect_mousedown(self, pos):
        if in_bounds(pos, self.pause_bounds):
            self.press_pause_button()

    def detect_mouseup(self, pos):
        if in_bounds(pos, self.pause_bounds):
            return self.show_pause()
        self.reset_imgs()
        return True

    def biking_minigame(self, character, resistance, sound):

        # Dificuldade
        dificuldade_lista = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
        dificuldade = [1500, 2500, 3000]

        for i in range(0, 10):
            if dificuldade_lista[i] == resistance:
                for x in range(0, 3):
                    dificuldade[x] = dificuldade[x] + (i * 100)

        # ajusta a velocidade de deslocamento dos inimigos de acordo com a resistance do jogador
        if resistance <= 50:
            enemy_velocity = 15
            movement_factor = 15
        elif resistance <= 80:
            enemy_velocity = 25
            movement_factor = 20
        else:
            enemy_velocity = 35
            movement_factor = 25

        # checa se existe alguma colisão 
        def check_collision(inimigos):
            for enemyinlist in inimigos:
                if biker_rect.colliderect(enemyinlist):
                    enemy_list.remove(enemyinlist)
                    return True

        # muda a lista que estão os corações, faz a troca entre um coração vermelho para um coração cinza
        def change_heart(heart_list):
            del (heart_list[get_hit])
            heart_list.insert(get_hit, grey_heart)

        # desenha os corações na tela a partir da lista de corações
        def draw_hearts(hearts_list):
            heart_x = 900
            for heart in hearts_list:
                heart_x += 90
                screen.blit(heart, (heart_x, 20))

        # acessa a lista de obstaculos e os desenha na tela
        def draw_enemys(enemys):
            for enemy in enemys:
                new_enemy_biker = biking_enemy_frames[biking_enemy_index]
                screen.blit(new_enemy_biker, enemy)

        def moving_enemys(enemys):
            for enemy in enemys:
                enemy
                enemy.centerx -= enemy_velocity
                enemy.centerx += 8
            visible_enemy = [enemy for enemy in enemys if enemy.right > -5]
            return visible_enemy

        def create_enemy():
            line = random.randrange(1, 3)
            if line == 1:
                new_enemy = enemy_biker_surface.get_rect(center=(1300, 220))
            else:
                new_enemy = enemy_biker_surface.get_rect(center=(1300, 462))
            return new_enemy

        # faz a animação do personagem correndo
        def biking_animation():
            new_biker = biking_frames[biking_index]
            new_biker_rect = new_biker.get_rect(center=(150, biker_y))
            return new_biker_rect, new_biker

        # faz a pista se mover
        def move_pista():
            screen.blit(bg_pista, (bg_pista_x, 95))
            screen.blit(bg_pista, (bg_pista_x + 1280, 95))

        # mostra a tela depois que o nivel acaba
        def end_game():
            if loser == True:
                pygame.mixer.quit()
                return 0
            if loser == False:
                pygame.mixer.quit()
                return 10
                # mostra o tutorial do nivel

        def show_tutor():
            pygame.draw.rect(screen, [0, 0, 0], [264, 254, 680, 220])
            screen.blit(tutorial, (tutorial_print))

        pygame.init()
        # seta a tela para o tamanho 1200X700
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()

        # variaveis do jogo
        # usado na animação do personagem
        biker_state = 0
        biker_y = 462
        # status do jogo, só inicia se for true
        game_active = False
        # variavel que armazena se o jogador conseeguiu ou não cumprir a tarefa dessa fase
        loser = False

        # fundo
        backgound = pygame.image.load(IMAGES_PATH + "biking/fundo_bike.png").convert_alpha()
        backgound2 = backgound
        bg_x = 0

        # tutorial
        tutorial = pygame.image.load(IMAGES_PATH + "biking/tutorial_bike.png").convert_alpha()
        tutorial_print = tutorial.get_rect(center=(600, 360))
        showtutor = True

        # Musicas e sons
        if sound == True:
            pygame.mixer.music.load(SOUNDS_PATH + 'bikingSounds/themeSong.mp3')
            pygame.mixer.music.play(-1)
            men_hit_sound = pygame.mixer.Sound(SOUNDS_PATH + 'bikingSounds/menHey.mp3')
            bike_sound = pygame.mixer.Sound(SOUNDS_PATH + 'bikingSounds/bicycleBuzzer.mp3')

        # pista
        bg_pista = pygame.image.load(IMAGES_PATH + 'biking/pista_bike.png').convert()
        bg_pista_x = 0

        # efeitos sonoros / musica

        # sprite dos ciclistas
        if character == "U":
            bike_frame2 = pygame.image.load(IMAGES_PATH + 'biking/biker_men2.png').convert_alpha()
            bike_frame1 = pygame.image.load(IMAGES_PATH + 'biking/biker_men1.png').convert_alpha()
            bike_frame3 = pygame.image.load(IMAGES_PATH + 'biking/biker_men3.png').convert_alpha()
            bike_frame4 = pygame.image.load(IMAGES_PATH + 'biking/biker_men4.png').convert_alpha()
            bike_frame5 = pygame.image.load(IMAGES_PATH + 'biking/biker_men5.png').convert_alpha()
            bike_frame6 = pygame.image.load(IMAGES_PATH + 'biking/biker_men6.png').convert_alpha()
            bike_frame7 = pygame.image.load(IMAGES_PATH + 'biking/biker_men7.png').convert_alpha()
        if character == "R":
            bike_frame2 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl2.png').convert_alpha()
            bike_frame1 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl1.png').convert_alpha()
            bike_frame3 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl3.png').convert_alpha()
            bike_frame4 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl4.png').convert_alpha()
            bike_frame5 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl5.png').convert_alpha()
            bike_frame6 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl6.png').convert_alpha()
            bike_frame7 = pygame.image.load(IMAGES_PATH + 'biking/biker_girl7.png').convert_alpha()

        biking_frames = [bike_frame1, bike_frame2, bike_frame3, bike_frame4, bike_frame5, bike_frame6, bike_frame7]
        biking_index = 0

        biker_surface = biking_frames[biking_index]
        biker_rect = biker_surface.get_rect(bottomleft=(10, 200))

        BIKING = pygame.USEREVENT + 1
        pygame.time.set_timer(BIKING, 100)

        # inimigos
        bike_enemy_frame1 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy1.png').convert_alpha()
        bike_enemy_frame2 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy2.png').convert_alpha()
        bike_enemy_frame3 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy3.png').convert_alpha()
        bike_enemy_frame4 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy4.png').convert_alpha()
        bike_enemy_frame5 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy5.png').convert_alpha()
        bike_enemy_frame6 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy6.png').convert_alpha()
        bike_enemy_frame7 = pygame.image.load(IMAGES_PATH + 'biking/biker_enemy7.png').convert_alpha()
        biking_enemy_frames = [bike_enemy_frame1, bike_enemy_frame2, bike_enemy_frame3, bike_enemy_frame4,
                               bike_enemy_frame5, bike_enemy_frame6, bike_enemy_frame7]
        biking_enemy_index = 0

        enemy_biker_surface = biking_enemy_frames[biking_enemy_index]
        enemy_biker_rect = enemy_biker_surface.get_rect(bottomleft=(10, 0))
        SPAWNENEMY = pygame.USEREVENT + 2
        pygame.time.set_timer(SPAWNENEMY, random.choice(dificuldade))
        enemy_list = []

        CONTADOR = pygame.USEREVENT + 3
        pygame.time.set_timer(CONTADOR, 1000)  # configurado o timer do Pygame para execução a cada 1 segundo
        temporizador = 15

        font = pygame.font.Font("assets/font/FreePixel.ttf", 40)

        # vidas
        # carrega imagem do coração vermelho
        red_heart = pygame.image.load(IMAGES_PATH + 'biking/red_heart.png').convert_alpha()
        # carrega imagem do coração cinza
        grey_heart = pygame.image.load(IMAGES_PATH + 'biking/grey_heart.png').convert_alpha()
        # cria uma lista com tres corações para serem desenhados na tela depois
        lifes_list = [red_heart, red_heart, red_heart]
        # sempre que atingido, essa variavel tem um acréscimo de 1(vai de -1 até 2, para representar os corações na lista)
        get_hit = -1

        while True:
            screen.blit(backgound, (bg_x, 0))
            screen.blit(backgound2, (bg_x + 1280, 0))
            bg_x -= 8
            if bg_x <= -1280:
                bg_x = 0
            draw_hearts(lifes_list)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        showtutor = False
                        game_active = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        biker_y = 220
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        biker_y = 462

                # evento que faz a animação
                if event.type == BIKING:
                    if biking_index < 6:
                        biking_index += 1
                        biking_enemy_index += 1
                    else:
                        biking_index = 0
                        biking_enemy_index = 0
                    biker_rect, biker_surface = biking_animation()

                # evento que chama a função para criar obstaculos
                if event.type == SPAWNENEMY and game_active:
                    enemy_list.append(create_enemy())
                    dif = random.choice(dificuldade)
                    pygame.time.set_timer(SPAWNENEMY, dif)

                # capturando evendo de relogio a cada 1 segundo e atualizando a variável contadora
                if event.type == CONTADOR and game_active:
                    temporizador = temporizador - 1

                if event.type == MOUSEBUTTONDOWN:
                    self.detect_mousedown(pygame.mouse.get_pos())
                elif event.type == MOUSEBUTTONUP:
                    result = self.detect_mouseup(pygame.mouse.get_pos())
                    if not result:
                        pygame.mixer.quit()
                        return False

            # atualiza a posição x da pista 
            bg_pista_x -= movement_factor
            # chama a função que desenha a pista na tela
            move_pista()
            # checa na variavel x da pista, se a mesma for menor que 1200 isso significa que a imagem esta totalmente fora da tela e então volta a sua
            # posição inicial
            if bg_pista_x <= -1280:
                bg_pista_x = 0

            # desenha o ciclista na tela
            screen.blit(biker_surface, biker_rect)
            if showtutor:
                show_tutor()

            if game_active:

                # chama a função que move a coordenada X dos inimigos
                enemy_list = moving_enemys(enemy_list)
                # desenha os inimigos
                draw_enemys(enemy_list)

                if check_collision(enemy_list):
                    # incrementa 1 na variavel de hits e muda a cor do coração para cinza
                    get_hit += 1
                    try:
                        men_hit_sound.play()
                        bike_sound.play()
                    except:
                        pass
                    change_heart(lifes_list)
                    if get_hit == 2:
                        loser = True
                        return end_game()
                        break

                timer1 = font.render('Tempo ' + str(temporizador), True, (0, 0, 0))
                screen.blit(timer1, (90, 32))
                # finalizando o jogo
                if temporizador == 0:
                    return end_game()
                    break

            # mostra botao de pause
            self.show_pause_button()
            self.show_status()
            pygame.display.update()
            clock.tick(60)
