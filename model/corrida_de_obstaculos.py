import time

import pygame, sys, random
from pygame.locals import *
from config import IMAGES_PATH, SOUNDS_PATH
from model.pause_menu import PauseMenu
from utils.position import in_bounds


class CorridaDeObstaculos(PauseMenu):
    def __init__(self, screen, agilidade):

        super().__init__(screen)

    def detect_mousedown(self, pos):
        if in_bounds(pos, self.pause_bounds):
            self.press_pause_button()

    def detect_mouseup(self, pos):
        if in_bounds(pos, self.pause_bounds):
            return self.show_pause()
        self.reset_imgs()
        return True

    def corrida_obstaculo(self, character, resistance):

        # Dificuldade
        dificuldade_lista = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
        dificuldade = [1000, 2000, 2500]

        for i in range(0, 10):
            if dificuldade_lista[i] == resistance:
                for x in range(0, 3):
                    dificuldade[x] = dificuldade[x] + (i * 100)

        # ajusta a velocidade de deslocamento dos obstaculos de acordo com a resistance do jogador
        if resistance <= 50:
            velocidade_obstaculo = 15
        elif resistance <= 80:
            velocidade_obstaculo = 20
        else:
            velocidade_obstaculo = 25

        # mostra a tela depois que o nivel acaba
        def end_game():
            if loser == True:
                lose_effect.play()
                pygame.mixer.quit()
                return 0
            if loser == False:
                win_effect.play()
                pygame.mixer.quit()
                return 10

        # mostra o tutorial do nivel
        def show_tutor():
            pygame.draw.rect(screen, [0, 0, 0], [284, 264, 633, 201])
            screen.blit(tutorial, (tutorial_print))

        # acessa a lista que contem as posições da onde obstaculo caido deve estar e denha ele na tela
        def redraw_obstaculo(obstaculos_caidos):
            for obstaculo in obstaculos_caidos:
                screen.blit(obstaculo_caido, obstaculo)

        # acessa a lista de obstaculos caidos, atualiza a posição dos mesmos, se o obstaculo sair da tela, apaga o mesmo da lista. Devolve uma lista com os novos objetos
        def move_obstaculos_caidos(obstaculos_caidos):
            for obstaculo in obstaculos_caidos:
                obstaculo.centerx -= velocidade_obstaculo
            visible_obstaculos = [obstaculo for obstaculo in obstaculos_caidos if obstaculo.right > -5]
            return visible_obstaculos

        # muda a lista que estão os corações, faz a troca entre um coração vermelho para um coração cinza
        def change_heart(heart_list):
            del (heart_list[get_hit])
            heart_list.insert(get_hit, grey_heart)

        # desenha os corações na tela a partir da lista de corações
        def draw_hearts(hearts_list):
            heart_x = 900
            for heart in hearts_list:
                heart_x += 90
                screen.blit(heart, (heart_x, 30))

        # função que cria o obstaculo
        def create_obstaculo():
            new_obstaculo = obstaculos_surface.get_rect(midbottom=(1300, 587))
            return new_obstaculo

            # função que acessa a lista de obstaculos, altera a posição dos mesmos, e quando saem da tela, apaga eles da lista. Retorna uma nova lista

        def move_obstaculos(obstaculos):
            for obstaculo in obstaculos:
                obstaculo.centerx -= 15
            visible_obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo.right > -5]
            return visible_obstaculos

        # acessa a lista de obstaculos e os desenha na tela
        def draw_obstaculos(obstaculos):
            for obstaculo in obstaculos:
                screen.blit(obstaculos_surface, obstaculo)

        # checa se existe alguma colisão no obstaculo
        def check_collision(obstaculos):
            for obstaculo in obstaculos:
                if runner_rect.colliderect(obstaculo):
                    return True

        # faz a animação do personagem correndo
        def running_animation():
            new_runner = run_frames[run_index]
            new_runner_rect = new_runner.get_rect(center=(150, runner_rect.centery))
            return new_runner_rect, new_runner

            # faz a pista se mover

        def move_pista():
            screen.blit(bg_pista, (bg_pista_x, 315))
            screen.blit(bg_pista, (bg_pista_x + 1200, 315))

        pygame.init()
        # seta a tela para o tamanho 1200X700
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()

        # variaveis do jogo
        # faz com que o personagem va em direção ao chão (usado no momento do pulo)
        gravidade = 0.5
        # usado na animação do personagem
        runner_state = 0
        # status do jogo, só inicia se for true
        game_active = False
        # variavel que armazena se o jogador conseeguiu ou não cumprir a tarefa dessa fase
        loser = False

        # fundo
        bg_surface = pygame.image.load(IMAGES_PATH + "corridaObsImgs/fundo.png").convert()

        # tutorial
        tutorial = pygame.image.load(IMAGES_PATH + "corridaObsImgs/tutorial_corrida.png").convert_alpha()
        tutorial_print = tutorial.get_rect(center=(600, 360))
        showtutor = True

        # pista
        bg_pista = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/pista.png').convert()
        bg_pista_x = 0

        # efeitos sonoros / musica
        hit_sound = pygame.mixer.Sound(SOUNDS_PATH + 'hitSound.mp3')
        jump_sound = pygame.mixer.Sound(SOUNDS_PATH + 'jump.mp3')
        pygame.mixer.music.load(SOUNDS_PATH + 'themeSong.mp3')
        pygame.mixer.music.play(-1)
        lose_effect = pygame.mixer.Sound(SOUNDS_PATH + 'youLose.mp3')
        win_effect = pygame.mixer.Sound(SOUNDS_PATH + 'youWin.mp3')

        # sprite corrida
        if character == "U":
            run_frame2 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/men2.png').convert_alpha()
            run_frame1 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/men1.png').convert_alpha()
            run_frame3 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/men3.png').convert_alpha()
            run_frame4 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/men4.png').convert_alpha()
            run_frame5 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/men5.png').convert_alpha()
        if character == "R":
            run_frame2 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/girl2.png').convert_alpha()
            run_frame1 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/girl1.png').convert_alpha()
            run_frame3 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/girl3.png').convert_alpha()
            run_frame4 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/girl4.png').convert_alpha()
            run_frame5 = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/girl5.png').convert_alpha()

        run_frames = [run_frame1, run_frame2, run_frame3, run_frame4, run_frame5]
        run_index = 0

        runner_surface = run_frames[run_index]
        runner_rect = runner_surface.get_rect(bottomleft=(10, 550))
        RUNNING = pygame.USEREVENT + 1
        pygame.time.set_timer(RUNNING, 100)

        # obstaculos

        # carrega imagem do obstaculo no estado normal
        obstaculos_surface = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/obstaculo.png').convert_alpha()
        # cria uma lista de obstaculos
        obstaculos_list = []
        # carrega imagem do obstaculo no estado caido
        obstaculo_caido = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/obstaculo_caido.png').convert_alpha()
        # cria uma lista de obstaculos caidos
        obstaculo_caido_list = []
        # cria evento que ira chamar a função que realmetne cria os obstaculos
        SPAWNOBSTACULO = pygame.USEREVENT + 3
        pygame.time.set_timer(SPAWNOBSTACULO, random.choice(dificuldade))

        CONTADOR = pygame.USEREVENT + 2
        pygame.time.set_timer(CONTADOR, 1000)  # configurado o timer do Pygame para execução a cada 1 segundo
        temporizador = 60

        font = pygame.font.SysFont('sans', 40)

        # vidas
        # carrega imagem do coração vermelho
        red_heart = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/red_heart.png').convert_alpha()
        # carrega imagem do coração cinza
        grey_heart = pygame.image.load(IMAGES_PATH + 'corridaObsImgs/grey_heart.png').convert_alpha()
        # cria uma lista com tres corações para serem desenhados na tela depois
        lifes_list = [red_heart, red_heart, red_heart]
        # sempre que atingido, essa variavel tem um acréscimo de 1(vai de -1 até 2, para representar os corações na lista)
        get_hit = -1

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        showtutor = False
                        game_active = True

                # função que faz o personagem pular, se o mesmo ja estiver fora do chão, não poderá ser acionado de novo
                if pygame.key.get_pressed()[K_SPACE]:
                    if runner_rect.bottom == 550:
                        jump_sound.play()
                        runner_state = 0
                        runner_state -= 14
                        if runner_rect.top <= 200:
                            runner_rect.top == 200

                # evento que chama a função para criar obstaculos
                if event.type == SPAWNOBSTACULO and game_active:
                    obstaculos_list.append(create_obstaculo())
                    dif = random.choice(dificuldade)
                    pygame.time.set_timer(SPAWNOBSTACULO, dif)

                # evento que faz a animação
                if event.type == RUNNING:
                    if run_index < 4:
                        run_index += 1
                    else:
                        run_index = 0
                    runner_rect, runner_surface = running_animation()

                if event.type == MOUSEBUTTONDOWN:
                    self.detect_mousedown(pygame.mouse.get_pos())
                elif event.type == MOUSEBUTTONUP:
                    result = self.detect_mouseup(pygame.mouse.get_pos())
                    if not result:
                        pygame.mixer.quit()
                        return False

                # capturando evendo de relogio a cada 1 segundo e atualizando a variável contadora
                if event.type == CONTADOR and game_active:
                    temporizador = temporizador - 1

                    # desenha a imagem de fundo na tela (o céu)
            screen.blit(bg_surface, (0, 0))
            # chama a função que desenha os corações
            draw_hearts(lifes_list)
            # atualiza a posição x da pista de corrida
            bg_pista_x -= 9
            # chama a função que desenha a pista na tela
            move_pista()
            # checa na variavel x da pista, se a mesma for menor que 1200 isso significa que a imagem esta totalmente fora da tela e então volta a sua
            # posição inicial
            if bg_pista_x <= -1200:
                bg_pista_x = 0

            # desenha o corredor na tela
            screen.blit(runner_surface, runner_rect)
            if showtutor:
                show_tutor()

            if game_active:
                # gravidade/correr
                runner_state += gravidade
                runner_rect.centery += runner_state
                # define o limite Y da sprite do corredor,
                if runner_rect.bottom > 550:
                    runner_rect.bottom = 550
                # chama a função que checa colisões, passando como parametro a lista de obstaculos
                if check_collision(obstaculos_list):
                    # toca efeito sonoro
                    hit_sound.play()
                    # quando detectado colisão, adiciona um obstaculo na lista de obstaculos caidos
                    obstaculo_caido_list.append(obstaculo_caido.get_rect(bottomleft=(obstaculos_list[0].bottomright)))
                    # deleta o obstaculo onde aconteceu a colisão
                    del (obstaculos_list[0])
                    # incrementa 1 na variavel de hits e muda a cor do coração para cinza
                    get_hit += 1
                    change_heart(lifes_list)
                    if get_hit == 2:
                        loser = True
                        break

                # obstaculos
                # chama a função que move a coordenada X dos obstaculos
                obstaculos_list = move_obstaculos(obstaculos_list)
                # chama a função que move a coordenada X dos obstaculos caidos
                obstaculo_caido_list = move_obstaculos_caidos(obstaculo_caido_list)
                # desenha os obstaculos
                draw_obstaculos(obstaculos_list)
                # redesenhas os obstaculos colocando o obstaculo caido no lugar
                redraw_obstaculo(obstaculo_caido_list)
                timer1 = font.render('Tempo ' + str(temporizador), True, (0, 0, 0))
                screen.blit(timer1, (90, 32))

                # finalizando o jogo
                if temporizador == 0:
                    break

            # mostra botao de pause
            self.show_pause_button()
            pygame.display.update()
            clock.tick(60)
        return end_game()
