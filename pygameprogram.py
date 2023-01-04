import sys
import matplotlib
import pygame
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
from pygame.locals import *
from Impementacja_wykresu import *
from constants import *
from funkcje import *

import time

pygame.init()

# Setting Clock
clock = pygame.time.Clock()

# Create the screen
screen_width = 1520
screen_height = 800
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode([1520,800])
pygame.display.set_caption("spinlaunch")

# zmienne
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms",20)
titlefont = pygame.font.SysFont('timesnewroman', 50)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)



# obrazy----------------------------------------------------------------------------------------------------------------
spinlaunchImg = pygame.image.load("SpinLaunch.logo.jpg")
earthImg = pygame.image.load('earth.jpg')

# z maina --------------------------------------------------------------------------------------------------------------

# funkcja przycisku ----------------------------------------------------------------------------------------------------
def create_button(x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))

#wyswietlanie wykresu---------------------------------------------------------------------------------------------------
def plot_display(a, b):
    x = np.linspace(0, 2 * np.pi, 100)
    y = (np.sin(a * x) ** b)
    plt.plot(x, y, color='g', lw=1, label='sin(a*x)')
    plt.show()

#ekran 1. --------------------------------------------------------------------------------------------------------------
def intro():
    title = titlefont.render("Projekt Spinlaunch", True, slategrey)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))

        screen.blit(title, ((screen_width - title.get_width()) / 2, 100))

        start_button = create_button(660, 700, 200, 100, lightgrey, slategrey)

        if start_button:
            menu()

        startbuttontext = titlefont.render("Start", True, blackish)
        screen.blit(startbuttontext, ((screen_width/2 - 50), 725))

        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width())/2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(15)
        return True

#menu glowne------------------------------------------------------------------------------------------------------------
def menu():
    instruction = font.render("wybierz opcje: program-wprowadzanie danych, teoria - wiecej o zjawisku", True, slategrey)
    programText = font.render("PROGRAM", True, blackish)
    teoriaText = font.render("TEORIA", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 0))

        programButtton = create_button((screen_width / 2) - 100, int(screen_height * .33), 200, 50, lightgrey, slategrey)

        if programButtton:
            data_input()

        screen.blit(programText, ((screen_width / 2) - (programText.get_width() / 2), int(screen_height * .33)))

        teoriaButtton = create_button((screen_width / 2) - 100, screen_height / 2, 200, 50, lightgrey, slategrey)

        if teoriaButtton:
            spinlaunch_info()

        screen.blit(teoriaText, ((screen_width / 2) - (programText.get_width() / 2), screen_height / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        pygame.display.update()
        clock.tick(15)

#wprowadzanie danych----------------------------------------------------------------------------------------------------
def data_input():
    title_text = font.render("wprowadzanie danych", True, slategrey)
    vv_x = ""
    vv_y = ''
    #global vv_x
    #vv_x = 0
    #global vv_y
    #vv_y = 0
    v_xActive = False
    v_yActive = False

    ready = font.render("Gotowe!", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))

        v_xSurface = font.render(vv_x, True, white)

        v_xBorder = pygame.Rect(((screen_width - v_xSurface.get_width()) / 2) - 10, screen_height * .20, v_xSurface.get_width() + 10, 50)

        screen.blit(v_xSurface, ((screen_width - v_xSurface.get_width()) / 2, screen_height * .20))


        v_ySurface = font.render(vv_y, True, white)

        v_yBorder = pygame.Rect(((screen_width - v_ySurface.get_width()) / 2) - 10, screen_height - 500,
                                      v_ySurface.get_width() + 10, 50)

        screen.blit(v_ySurface, ((screen_width - v_ySurface.get_width()) / 2, screen_height - 500))



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()



            if event.type == pygame.MOUSEBUTTONDOWN:
                if v_xBorder.collidepoint(event.pos):
                    v_xActive = True
                    v_yActive = False
                if v_yBorder.collidepoint(event.pos):
                    v_yActive = True
                    v_xActive = False


            if event.type == pygame.KEYDOWN:
                if v_xActive:
                    if event.key == pygame.K_BACKSPACE:
                        vv_x = vv_x[:-1]
                    else:
                        vv_x += event.unicode
                if v_yActive:
                    if event.key == pygame.K_BACKSPACE:
                        vv_y = vv_y[:-1]
                    else:
                        vv_y += event.unicode
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()



        if v_xActive:
            pygame.draw.rect(screen, white, v_xBorder, 2)
            v_xPrompt = font.render("podaj v_x", True, white)
        else:
            pygame.draw.rect(screen, slategrey, v_xBorder, 2)
            v_xPrompt = font.render("podaj v_x", True, slategrey)

        if v_yActive:
            pygame.draw.rect(screen, white, v_yBorder, 2)
            v_yPrompt = font.render("podaj v_y", True, white)
        else:
            pygame.draw.rect(screen, slategrey, v_yBorder, 2)
            v_yPrompt = font.render("podaj v_y", True, slategrey)





        screen.blit(v_xPrompt, ((screen_width - v_xPrompt.get_width()) / 2,
                                     (screen_height * .20) + v_xSurface.get_height()))
        screen.blit(v_yPrompt, ((screen_width - v_yPrompt.get_width()) / 2,
                                     (screen_height -500) + v_ySurface.get_height()))





        readyButtton = create_button((screen_width / 2) - (ready.get_width() / 2) - 200, screen_height * .9,
                                      ready.get_width() + 10, ready.get_height(), lightgrey, slategrey)

        screen.blit(ready, ((screen_width / 2) - (ready.get_width() / 2) - 195, int(screen_height * .9)))

        if readyButtton:
            if vv_x != "":
                v_x = float(vv_x)
                v_x0 = float(vv_x)
            if vv_y != "":
                v_y = float(vv_y)
                v_y0 = float(vv_y)
            else:
                pass
            print(v_x, v_y, v_x0, v_y0)


            if spin == 1:
                obliczenia_numeryczne(0, 0, wysokość=H_startu)  # Silniki nie zadzaiłały

                reset_xyv()  # resetuje wartości po I przelocie
                obliczenia_numeryczne(1, 0, wysokość=H_startu)  # I faza ruchu - do odpalenia silników

                update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])
                obliczenia_numeryczne(2, 0, wysokość=H_startu)  # II faza ruchu - z silnikami
                update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])

                obliczenia_numeryczne(3, 0, wysokość=H_startu)  # III faza ruchu - po wyczerpaniu paliwa

                wyświetlanie_wykresów(1, 1, 1)  # 0 nie wyświetlam, 1 wyświetlam

            if spin != 1:
                pass
            clear()
            powrot(1,1)
        pygame.display.update()
        clock.tick(15)


#o spinlaunchu----------------------------------------------------------------------------------------------------------
def spinlaunch_info():
    title_text = font.render("O spinlaunchu", True, slategrey)

    next = font.render("dalej", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))
        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width()) / 2, 300))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        nextButtton = create_button((screen_width / 2) - (next.get_width() / 2) - 5, screen_height * .9,
                                     next.get_width() + 10, next.get_height(), lightgrey, slategrey)

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2), int(screen_height * .9)))

        if nextButtton:
            teoria()

        pygame.display.update()
        clock.tick(15)

#jak wyslac satelite----------------------------------------------------------------------------------------------------
def teoria():
    title_text = font.render("teoria", True, slategrey)

    next = font.render("dalej", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))
        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width()) / 2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        nextButtton = create_button((screen_width / 2) - (next.get_width() / 2) + 195, screen_height * .9,
                                    next.get_width() + 10, next.get_height(), lightgrey, slategrey)

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2)+200, int(screen_height * .9)))

        if nextButtton:
            parametry()

        pygame.display.update()
        clock.tick(15)

def parametry():
    title_text = font.render("parametry stałe", True, slategrey)

    next = font.render("dalej", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))
        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width()) / 2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        nextButtton = create_button((screen_width / 2) - (next.get_width() / 2), screen_height * .9,
                                    next.get_width() + 10, next.get_height(), lightgrey, slategrey)

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2) + 5, int(screen_height * .9)))

        if nextButtton:
            data_input()

        pygame.display.update()
        clock.tick(15)

def plot(a,b):
    matplotlib.use("Agg")
    import matplotlib.backends.backend_agg as agg
    import pylab

    fig = pylab.figure(figsize=[6, 6], dpi=100)
    ax = fig.gca()
    x = np.linspace(0, 2 * np.pi, 100)
    y = (np.sin(a*x))**b
    ax.plot(x, y, color='g', lw=1, label='sin(a*x)')

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    screen.fill((0, 0, 0))
    window = pygame.display.get_surface()

    size = canvas.get_width_height()
    title_text = font.render("czy chcesz sprobowac jeszcze raz?", True, slategrey)
    screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (400, 100))
    pygame.display.flip()

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

#pytanie o powrót
def powrot(a, b):
    matplotlib.use('TkAgg')
    instruction = font.render("wybierz opcje: ", True, slategrey)
    backText = font.render("POWROT DO WPROWADZANIA ZMIENNYCH", True, blackish)
    plotText = font.render("WYJSCIE Z PROGRAMU I WYSWIETLENIE WYKRESU W MATPLOTLIB", True, blackish)

    running = True
    while(running):
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 0))

        backButtton = create_button((screen_width / 2) - 100, int(screen_height * .33), 200, 50, lightgrey, slategrey)

        if backButtton:
            data_input()

        screen.blit(backText, ((screen_width / 2) - (backText.get_width() / 2), int(screen_height * .33)))

        plotButtton = create_button((screen_width / 2) - 100, screen_height / 2, 200, 50, lightgrey, slategrey)

        if plotButtton:
            #running = False
            #pygame.display.quit()
            plot_display(a, b)
            pygame.display.init()
            pygame.display.flip()
            #main_loop1()

        screen.blit(plotText, ((screen_width / 2) - (backText.get_width() / 2), screen_height / 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(60)


#pętla glowna-----------------------------------------------------------------------------------------------------------
def oknowyboru():
    pygame.display.set_mode((1520,800))
    pygame.display.set_caption('okno wyboru')
    running=True
    while(running):
        intro()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.display.quit()


pygame.init()
oknowyboru()
