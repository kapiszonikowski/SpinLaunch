import sys
import pygame
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Slider

# Stałe------------------------------------------------------------------------------------------------------------------
M_Z = 5.98 * 10 ** 24  # masa ziemi
R_Z = 6371000  # promień ziemi
G = 6.6743 * 10 ** (-11)  # stała grawitacyjna
V_1 = np.sqrt(G * M_Z / R_Z)  # I prędkośćkosmiczna
x_0 = 0  # pocztkowy x
y_0 = R_Z + 20  # pocztkowy y
k = G * M_Z  # wsp staej grawitacji
Dt = 0.01  # czas aktualizacji
# alpha = nu.angle(0, deg=True)
f = 0.125  # Drag coefficient for rocket
S = np.pi * 0.5 ** 2  # Rocket cross-section
m_m = 10300  # masa całego modułu
v_g = 8750  # prędkość gazów wylotowych
m_r_p = 1000  # początkowa masa rakiety
jak_często = 100  # gęstość rozmieszczenia punktów - dla 100 pokazuje lokalizacje co 1s
tryb_pracy_silników = 0

# zmienne----------------------------------------------------------------------------------------------------------------
droga = 0  # zmienna drogi
v_x0 = 1000  # prędkość początkowa y
v_y0 = 1800  # prędkość początkowa y
X_location = x_0  # zmienna położenia x
Y_location = y_0  # zmienna położenia y
R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5  # odległość rakiety od środka ziemi
Hnpm = R_xy - R_Z  # wysokość npm
v_x = v_x0  # zmienna prędkości x
v_y = v_y0  # zmienna prędkości y
H_startu = 100000
i = 0  # ilość punktów
spin = 0
m_r = m_r_p  # zmienna masa rakiety
m_p0 = 600  # masa paliwa
m_p = m_p0
Dm_1s = m_p0 / 150  # paliwo tracone w czasie 1 s
test = 0
test1 = 0

# Listy------------------------------------------------------------------------------------------------------------------
x_forplot, x1_forplot = [X_location], [X_location]
y_forplot, y1_forplot = [Y_location], [Y_location]
listR_xy = [R_xy]  # potrzebne? -> TAK
listH_xy, listH_xy1 = [], []
wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x = [], [], [], [], [], []
v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly = [], [], [], [], [], [], [], [], []

#funkcje do wykresu------------------------------------------------------------------------------------------------------
def obliczanie_przyspieszenia(faza):
    global R_xy, v_x, X_location, Y_location, v_y, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x, jak_często
    if faza == 0:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
    if faza == 1:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update

            if Hnpm >= 100 and i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 100:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 100:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 100:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 100:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))
    if faza == 2:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m) + a_t_x  # x-acceleration update

            if Hnpm >= 100 and i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 100:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m) + a_t_x # x-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 100:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m) + a_t_y # x-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 100:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m) + a_t_y # y-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 100:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))
    if faza == 3:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update

            if Hnpm >= 100 and i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 100:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 100:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 100:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
            if Hnpm >= 100 and i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 100:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

def updates_appends(faza):
    global R_xy, jak_często, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, i, x_forplot, x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l, a_y_l
    if faza == 0:
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

        i += 1

        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        Hnpm = R_xy - R_Z


        if Hnpm >= 100 and i % jak_często == 0:
            x1_forplot.append(X_location)
            y1_forplot.append(Y_location)
            listH_xy1.append(Hnpm)

        if Hnpm < 100:
            x1_forplot.append(X_location)
            y1_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            Hnpm = R_xy - R_Z
            listH_xy1.append(Hnpm)

    if faza == 1:
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

        i += 1

        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        Hnpm = R_xy - R_Z

        if Hnpm >= 100 and i % jak_często == 0:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append((v_x))
            v_y_l.append((v_y))
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

        if Hnpm < 100:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
            Hnpm = R_xy - R_Z

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append((v_x))
            v_y_l.append((v_y))
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

    if faza == 2:
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

        i += 1

        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        Hnpm = R_xy - R_Z

        if Hnpm >= 100 and i % jak_często == 0:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append((v_x))
            v_y_l.append((v_y))
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

        if Hnpm < 100:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
            Hnpm = R_xy - R_Z

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append((v_x))
            v_y_l.append((v_y))
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

    if faza == 3:
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

        i += 1

        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        Hnpm = R_xy - R_Z

        if Hnpm >= 100 and i % jak_często == 0:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append((v_x))
            v_y_l.append((v_y))
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

        if Hnpm < 100:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
            Hnpm = R_xy - R_Z

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append((v_x))
            v_y_l.append((v_y))
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

def naprowadzanie_na_orbite():
    global R_xy, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, a_t_x, a_t_y, test, m_p

    if prędkość_kosmiczna(R_xy) * cos(X_location, Y_location) > v_x:
        a_t_x = thrust_acceleration1()
        m_p = m_p - Dm_1s * Dt / 1  # rocket fuel mass update
        m_r = m_r - Dm_1s * Dt / 1  # rocket mass update

        a_t_y = 0
    else:
        a_t_x = 0
        if -prędkość_kosmiczna(R_xy) * sin(X_location, Y_location) < v_y:
            a_t_y = -sin(X_location, Y_location) * thrust_acceleration1()
            m_p = m_p - Dm_1s * Dt * sin(X_location, Y_location) / 1  # rocket fuel mass update
            m_r = m_r - Dm_1s * Dt / 1  # rocket mass update

        else:
            a_t_y = 0
    if a_t_x != 0 or a_t_y != 0:
        test = 1
    print(m_p)

def troche_jak_prawdziwa():
    global R_xy, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, a_t_x, a_t_y, test, m_p
    try:
        a_t_x = D_osi(x_forplot[-1], x_forplot[-2]) * thrust_acceleration(x_forplot[-1], x_forplot[-2],
                                                                          y_forplot[-1], y_forplot[-2])
        a_t_y = D_osi(y_forplot[-1], y_forplot[-2]) * thrust_acceleration(x_forplot[-1], x_forplot[-2],
                                                                          y_forplot[-1], y_forplot[
                                                                              -2])  # stare przyśpieszenie
        m_p = m_p - Dm_1s * Dt / 1  # rocket fuel mass update
        m_r = m_r - Dm_1s * Dt / 1  # rocket mass update


    except:
        a_t_x = 0
        a_t_y = 0
    if a_t_x != 0 or a_t_y != 0:
        test = 1

def zawsze_prostopadle():
    global R_xy, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, a_t_x, a_t_y, test, m_p
    a_t_x = cos(X_location, Y_location) * thrust_acceleration1()
    a_t_y = -sin(X_location, Y_location) * thrust_acceleration1()
    m_p = m_p - Dm_1s * Dt / 1  # rocket fuel mass update
    m_r = m_r - Dm_1s * Dt / 1  # rocket mass update

    if a_t_x != 0 or a_t_y != 0:
        test = 1

def obliczenia_numeryczne(faza, p_important_values, wysokość, tryb_pracy_silników):
    global R_xy, X_location, Y_location, m_r, droga, Hnpm, H_startu, jak_często, test, m_p

    if faza == 0:
        while R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values(faza)

    if faza == 1:
        while Hnpm < wysokość and R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values(faza)

    if faza == 2:

        while m_p > 0 and R_Z < R_xy:
            if tryb_pracy_silników == 0:
                naprowadzanie_na_orbite()
                if a_t_x == 0 and a_t_y == 0:
                    break

            if tryb_pracy_silników == 1:
                troche_jak_prawdziwa()
                if v_x > V_1 and Hnpm > 8500:
                    break

            if tryb_pracy_silników == 2:
                zawsze_prostopadle()
                if v_x > V_1 and Hnpm > 85000:  # to było o 1 tab do przodu
                    break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values(faza)

    if faza == 3:
        while R_xy > R_Z:

            if droga > 6 * R_Z and X_location > wazny_x[1]:
                break
            if droga > 8 * R_Z:
                break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values(faza)

def prędkość_kosmiczna(R):
    return np.sqrt(G * M_Z / R)

def air_density(R_xy):  # air density formula
    if R_xy < R_Z + 100000:
        return np.exp(((R_Z - R_xy) / 1000 / 9.038)) * 1.23435
    else:
        return 0

def drag_acceleration(R_xy, speed, mr):  # drag from the height and air density
    return 0.5 * air_density(R_xy) * S * speed ** 2 * f / mr

def cos(x, y):
    return y / np.sqrt(x ** 2 + y ** 2)

def sin(x, y):
    return x / np.sqrt(x ** 2 + y ** 2)

def D_osi(p1, p0):
    return p1 - p0

def przemieszczenie(x1, x0, y1, y0):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def thrust_acceleration(x1, x0, y1, y0):
    return 1 / przemieszczenie(x1, x0, y1, y0) * (v_g * Dm_1s + 0.01 * S * 10 * air_density(R_xy)) / m_r

def thrust_acceleration1():
    return (v_g * Dm_1s + 0.01 * S * 10 * air_density(R_xy)) / m_r

def update_important_values(x, y, d, h, a, v):
    wazny_x.append(x)
    wazny_y.append(y)
    wazny_d.append(d)
    wazny_h.append(h)
    wazny_a.append(a)
    wazny_v.append(v)

def v_xy(vx, vy):
    return (vx ** 2 + vy ** 2) ** 0.5

def a_xy(ax, ay):
    return (ax ** 2 + ay ** 2) ** 0.5

def print_important_values(faza):
    try:
        if faza == 2:
            print(m_p)
        print(
            f'a_x: {round(a_x, 2)} m/s^2 ||  ay: {round(a_y, 2)} m/s^2 || a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)} || v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
        print(
            f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m] || H: {round(R_xy - R_Z)}[m] ||  t: {round(i / 3600000, 2)}[s] || m_r: {m_r : .8}\n')
    except:
        print(
            f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m] || H: {Hnpm}[m] ||  t: {round(i / 3600000, 2)}[s]')

def reset_xyv():
    global v_x, v_y, X_location, Y_location, R_xy, v_x0, v_y0, x_0, y_0, Hnpm, R_Z
    v_x = v_x0
    v_y = v_y0
    X_location = x_0
    Y_location = y_0
    R_xy = y_0
    Hnpm = R_xy - R_Z

def clear():
    global m_r, m_p, droga, X_location, Y_location, R_xy, Hnpm,  i, x_forplot, x1_forplot, y_forplot, y1_forplot, listR_xy, listH_xy, listH_xy1, wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x, v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly
    m_r = m_r_p
    m_p = m_p0
    droga = 0
    i = 0
    X_location = x_0  # zmienna położenia x
    Y_location = y_0  # zmienna położenia y
    R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5  # odległość rakiety od środka ziemi
    Hnpm = R_xy - R_Z  # wysokość npm
    x_forplot, x1_forplot = [x_0], [x_0]
    y_forplot, y1_forplot = [y_0], [y_0]
    listR_xy = [R_xy]  # potrzebne? -> TAK
    listH_xy, listH_xy1 = [], []
    wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x = [], [], [], [], [], []
    v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly = [], [], [], [], [], [], [], [], []

def print_ploted_data():
    print('ANOTHER LAP')
    print(listH_xy, listH_xy1)
    print(wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x)
    print(v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly)
    print('---------------------------------------------------------------------------------')

def wyświetlanie_wykresów(orbita, dane):
    # Tworzenie tekstu-------------------------------------------------------------------------------------------------------
    nd = round((droga / 1000), 2)
    nw = round((max(listR_xy) - R_Z) / 1000, 2)
    napis_drogi = f'droga przebyta przez ciao: {nd}km'
    napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
    napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0 / 1000, 2)} ; Vy = {round(v_y0 / 1000, 2)}'
    napis_paliwa = f'masa paliwa: {m_p}kg'
    napis_gazów = f'prędkość gazów wylotowych: {v_g}m\s'
    n = -0.8 * R_Z
    if orbita == 1:
        # ax, ax1 = plt.subplots()
        plt.axis('square')
        plt.plot(x_forplot, y_forplot, color='g', label='trajektoria rakiety')
        try:
            plt.plot(x1_forplot, y1_forplot, color='r', lw=0.5, label='trajektoria osłony')
        except:
            pass
        plt.xlim(-2 * R_Z, 2 * R_Z)
        plt.ylim(-2 * R_Z, 2 * R_Z)
        theta = np.arange(0, np.pi * 2, 0.0001)
        alfa = np.arange(0, np.pi * 2, 0.001)
        plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), lw=2, color='b',
                 label='Ziemia')  # model ziemi
        plt.plot((R_Z + 85000) * np.cos(alfa), (R_Z + 85000) * np.sin(alfa), color='y', lw=0.3)
        try:
            plt.scatter(wazny_x, wazny_y)  # początak i start działania silników
        except:
            pass
        plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
        plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
        plt.text(n, 0.1 * R_Z, napis_paliwa, fontsize=10)
        plt.text(n, 0.0 * R_Z, napis_gazów, fontsize=10)
        plt.legend()
        plt.xlabel('oś X')
        plt.ylabel('oś Y')

        ax = plt.subplot()
        cursor = Cursor(ax, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        '''ax.subplots_adjust(bottom=0.25)
        axslider = ax.add_axes([0.1, 0.1, 0.6, 0.05])
        slider = Slider(ax=axslider, label="Time", valmin=0, valmax=i-1, valstep=1)
        def update(indx):
            ax1.scatter(x_forplot[indx], y_forplot[indx], color='Black')
        ax.canvas.draw_idle()
        slider.on_changed(update)'''

        #figManager = plt.get_current_fig_manager()
        #figManager.window.showMaximized()
        plt.show()

    if dane == 1:
        while len(droga_l) - len(d_a_ly) != 0:
            if len(droga_l) - len(d_a_ly) < 0:
                d_a_ly.remove(d_a_ly[0])
                d_a_lx.remove(d_a_lx[0])
            if len(droga_l) - len(d_a_ly) > 0:
                droga_l.remove(droga_l[0])

            while len(droga_l) - len(a_xy_l) != 0:
                if len(droga_l) - len(a_xy_l) < 0:
                    a_xy_l.remove(a_xy_l[0])
                    a_y_l.remove(a_y_l[0])
                    a_x_l.remove(a_x_l[0])
                    v_x_l.remove(v_x_l[0])
                    v_xy_l.remove(v_xy_l[0])
                    v_y_l.remove(v_y_l[0])
                    listH_xy.remove(listH_xy[0])
                if len(droga_l) - len(a_xy_l) > 0:
                    droga_l.remove(droga_l[0])
        plt.subplot(411)
        plt.plot(droga_l, d_a_ly, color='r', lw=1, ls='-', label='daly ')
        plt.plot(droga_l, d_a_lx, label='dalx')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        aa = plt.subplot(411)
        cursor1 = Cursor(aa, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(412)
        plt.plot(droga_l, a_xy_l, color='g', lw=3, ls='dotted', label='a_xy(d)')
        plt.plot(droga_l, a_x_l, color='r', lw=1, ls='-', label='a_x(d)')
        plt.plot(droga_l, a_y_l, color='y', lw=1, ls='-', label='a_y(d)')
        plt.scatter(wazny_d, wazny_a, label='d_a_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        ab = plt.subplot(412)
        cursor2 = Cursor(ab, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(413)
        plt.plot(droga_l, v_xy_l, color='g', lw=3, ls='dotted', label='v_xy(d) [m/s]')
        plt.plot(droga_l, v_x_l, color='r', lw=1, ls='-', label='v_x(d) [m/s]')
        plt.plot(droga_l, v_y_l, color='y', lw=1, ls='-', label='v_y(d) [m/s]')
        plt.scatter(wazny_d, wazny_v, label='d_v_t')
        plt.legend()
        plt.xlabel('km')
        plt.ylabel('m/s)')

        ac = plt.subplot(413)
        cursor3 = Cursor(ac, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(414)
        x = np.linspace(0, max(droga_l), 100)
        y = 0 * x + 100
        plt.plot(x, y, color='b', lw=1, ls='--', label='koniec atmosfery')
        plt.plot(droga_l, listH_xy, color='b', lw=1, ls='-', label='Hxy_(d) [km]')
        plt.scatter(wazny_d, wazny_h, label='d_h_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('km')

        ad = plt.subplot(414)
        cursor4 = Cursor(ad, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        #figManager = plt.get_current_fig_manager()
        #figManager.window.showMaximized()
        plt.show()


pygame.init()

# Setting Clock
clock = pygame.time.Clock()

# Create the screen
screen_width = 1520
screen_height = 800
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode([1520,800])
pygame.display.set_caption("spinlaunch")

# zmienne
font = pygame.font.SysFont("Comfortaa_Regular", 50)
smallfont = pygame.font.SysFont("Comfortaa_Regular", 40)
titlefont = pygame.font.SysFont('Comfortaa_Regular', 70)
littlefont = pygame.font.SysFont('Comfortaa_Thin', 30)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)
granat = (25,25,112)
royalblue = (16,78,139)
gold = (238,180,34)

# obrazy----------------------------------------------------------------------------------------------------------------
spinlaunchImg = pygame.image.load("SpinLaunch.logo.jpg")
#earthImg = pygame.image.load('earth.jpg')
#slImg = pygame.image.load('SpinLaunch.png')
misteryImg = pygame.image.load('mistery.jpg')
#gradient = pygame.image.load('dark-blue-green.jpg')
#gradientImg = pygame.transform.scale(gradient, (1520, 800))
infoImg = pygame.image.load('ospinlaunchu.png')
spin = pygame.image.load('spin.jpg')
spinImg = pygame.transform.scale(spin, (400, 200))
rocket = pygame.image.load('spinlaunch-2.jpg')
rocketImg = pygame.transform.scale(rocket, (380, 200))

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


# ekran 1. --------------------------------------------------------------------------------------------------------------
def intro():
    title = titlefont.render("PROJEKT SPINLAUNCH", True, white)
    addtitle = font.render('czyli model wprowadzania satelity na orbitę', True, white)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))

        screen.blit(title, ((screen_width - title.get_width()) / 2, 150))
        screen.blit(addtitle, ((screen_width - addtitle.get_width()) / 2, title.get_height()+200))

        start_button = create_button(710, 700, 100, 40, blackish, royalblue)

        if start_button:
            menu()

        startbuttontext = smallfont.render("START", True, white)
        screen.blit(startbuttontext, (((screen_width/2) - (startbuttontext.get_width() / 2)), 705))

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

# menu glowne------------------------------------------------------------------------------------------------------------
def menu():
    instruction = titlefont.render("WYBIERZ OPCJĘ", True, white)
    programText = font.render("TEORIA", True, white)
    teoriaText = font.render("PROGRAM", True, white)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 50))

        programButtton = create_button((1000 / 2) - 100, int(screen_height * .40), 200, 50, blackish, royalblue)

        if programButtton:
            spinlaunch_info()

        screen.blit(programText, ((1000 - programText.get_width()) / 2, int(screen_height * .40)+7))

        teoriaButtton = create_button((1900 / 2) - 100, screen_height*.40, 200, 50, blackish, royalblue)

        if teoriaButtton:
            wybor_trybu()

        screen.blit(teoriaText, ((1900 - teoriaText.get_width())/2, (screen_height*.40)+7))

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

# wybór trybu------------------------------------------------------------------------------------------------------------
def wybor_trybu():
    instruction = titlefont.render("WYBIERZ TRYB", True, white)
    programText = font.render("SPINLAUNCH", True, white)
    teoriaText = font.render("PIASKOWNICA", True, white)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 50))

        programButtton = create_button((screen_width/2)-150, int(screen_height * .33), 300, 50, blackish,royalblue)

        if programButtton:
            data_input()

        screen.blit(programText, (((screen_width - programText.get_width()) / 2), int(screen_height * .33)+7))

        teoriaButtton = create_button((screen_width/2)-150, screen_height / 2, 300, 50, blackish, royalblue)

        if teoriaButtton:
            piaskownica()

        screen.blit(teoriaText, (((screen_width - teoriaText.get_width()) / 2), (screen_height / 2)+7))

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

# wprowadzanie danych----------------------------------------------------------------------------------------------------
def data_input():
    global test, R_xy, v_x0, v_y0, jak_często, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, i, x_forplot, x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l, a_y_l, m_p, H_startu, tryb_pracy_silników

    title_text = font.render("WPROWADŹ NASTĘPUJĄCE PARAMETRY", True, gold)
    vv_x = ''
    vv_y = ''
    mm_p = ''
    HH_startu = ''
    t0='0'
    t1 = '1'
    t2 = '2'
    YY_0 = ''
    v_xActive = False
    v_yActive = False
    m_pActive = False
    H_startuActive = False
    t0Active = False
    t1Active = False
    t2Active = False
    Y_0Active = False

    ready = font.render("Gotowe!", True, white)

    while True:

        # ustawienia tla------------------------------
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(title_text, (40, 20))

        # Y_0
        Y_0Surface = littlefont.render(YY_0, True, white)
        Y_0Border = pygame.Rect(650, screen_height - 690,
                                Y_0Surface.get_width() + 10, 40)
        screen.blit(Y_0Surface, (655, screen_height - 680))

        # v_x
        v_xSurface = littlefont.render(vv_x, True, white)
        v_xBorder = pygame.Rect(650, screen_height - 620,
                                v_xSurface.get_width() + 10, 40)
        screen.blit(v_xSurface, (655, screen_height - 610))

        # v_y
        v_ySurface = littlefont.render(vv_y, True, white)
        v_yBorder = pygame.Rect(650, screen_height - 550,
                                v_ySurface.get_width() + 10, 40)
        screen.blit(v_ySurface, (655, screen_height - 540))

        # m_p
        m_pSurface = littlefont.render(mm_p, True, white)
        m_pBorder = pygame.Rect(650, screen_height - 480,
                                m_pSurface.get_width() + 10, 40)
        screen.blit(m_pSurface, (655, screen_height - 470))

        # H_startu
        H_startuSurface = littlefont.render(HH_startu, True, white)
        H_startuBorder = pygame.Rect(650, screen_height - 410,
                                     H_startuSurface.get_width() + 10, 40)
        screen.blit(H_startuSurface, (655, screen_height - 400))

        #okineka tryb silników
            #t0
        t0Surface = littlefont.render(t0, True, white)
        t0Border = pygame.Rect(1000, screen_height - 540,
                                     t0Surface.get_width() + 10, 40)
        screen.blit(t0Surface, (1005, screen_height - 530))
            #t1
        t1Surface = littlefont.render(t1, True, white)
        t1Border = pygame.Rect(1000, screen_height - 440,
                               t1Surface.get_width() + 10, 40)
        screen.blit(t1Surface, (1005, screen_height - 430))
            #t2
        t2Surface = littlefont.render(t2, True, white)
        t2Border = pygame.Rect(1000, screen_height - 340,
                               t2Surface.get_width() + 10, 40)
        screen.blit(t2Surface, (1005, screen_height - 330))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Y_0Border.collidepoint(event.pos):
                    Y_0Active = True
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if v_xBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = True
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                if v_yBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = True
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                if m_pBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = True
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                if H_startuBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = True
                    t0Active = False
                    t1Active = False
                    t2Active = False
                if t0Border.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = True
                    t1Active = False
                    t2Active = False
                if t1Border.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = True
                    t2Active = False
                if t2Border.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = True

            if event.type == pygame.KEYDOWN:
                if H_startuActive:
                    if event.key == pygame.K_BACKSPACE:
                        HH_startu = HH_startu[:-1]
                    else:
                        HH_startu += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            Y_0Active = True
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                if m_pActive:
                    if event.key == pygame.K_BACKSPACE:
                        mm_p = mm_p[:-1]
                    else:
                        mm_p += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = True
                if v_yActive:
                    if event.key == pygame.K_BACKSPACE:
                        vv_y = vv_y[:-1]
                    else:
                        vv_y += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = True
                            H_startuActive = False
                if v_xActive:
                    if event.key == pygame.K_BACKSPACE:
                        vv_x = vv_x[:-1]
                    else:
                        vv_x += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = True
                            m_pActive = False
                            H_startuActive = False
                if Y_0Active:
                    if event.key == pygame.K_BACKSPACE:
                        YY_0 = YY_0[:-1]
                    else:
                        YY_0 += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = True
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False

                if t2Active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = True
                            t1Active = False
                            t2Active = False
                if t1Active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = True
                if t0Active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = True
                            t2Active = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if Y_0Active:
            pygame.draw.rect(screen, white, Y_0Border, 2)
            Y_0Prompt = littlefont.render("WYSOKOŚĆ STARTU", True, white)
        else:
            pygame.draw.rect(screen, slategrey, Y_0Border, 2)
            Y_0Prompt = littlefont.render("WYSOKOŚĆ STARTU", True, slategrey)

        if v_xActive:
            pygame.draw.rect(screen, white, v_xBorder, 2)
            v_xPrompt = littlefont.render("POZIOMA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, white)
        else:
            pygame.draw.rect(screen, slategrey, v_xBorder, 2)
            v_xPrompt = littlefont.render("POZIOMA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, slategrey)

        if v_yActive:
            pygame.draw.rect(screen, white, v_yBorder, 2)
            v_yPrompt = littlefont.render("PIONOWA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, white)
        else:
            pygame.draw.rect(screen, slategrey, v_yBorder, 2)
            v_yPrompt = littlefont.render("PIONOWA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, slategrey)

        if m_pActive:
            pygame.draw.rect(screen, white, m_pBorder, 2)
            m_pPrompt = littlefont.render("MASA PALIWA (KG)", True, white)
        else:
            pygame.draw.rect(screen, slategrey, m_pBorder, 2)
            m_pPrompt = littlefont.render("MASA PALIWA (KG)", True, slategrey)

        if H_startuActive:
            pygame.draw.rect(screen, white, H_startuBorder, 2)
            H_startuPrompt = littlefont.render("WYSOKOŚĆ URUCHOMIENIA SILNIKÓW", True, white)
        else:
            pygame.draw.rect(screen, slategrey, H_startuBorder, 2)
            H_startuPrompt = littlefont.render("WYSOKOŚĆ URUCHOMIENIA SILNIKÓW", True, slategrey)

        if t0Active:
            pygame.draw.rect(screen, white, t0Border, 2)
            t0Prompt = littlefont.render("tryb 0 - samonaprowadzający na orbitę", True, white)

        else:
            pygame.draw.rect(screen, slategrey, t0Border, 2)
            t0Prompt = littlefont.render("tryb 0 - samonaprowadzający na orbitę", True, slategrey)

        if t1Active:
            pygame.draw.rect(screen, white, t1Border, 2)
            t1Prompt = littlefont.render("tryb 1 - siła ciągu działa wraz z trajektorią rakiety", True, white)
            t1Prompt1 = littlefont.render(" rakiety", True, white)
        else:
            pygame.draw.rect(screen, slategrey, t1Border, 2)
            t1Prompt = littlefont.render("tryb 1 - siła ciągu działa wraz z trajektorią", True, slategrey)
            t1Prompt1 = littlefont.render("rakiety", True, slategrey)
        if t2Active:
            pygame.draw.rect(screen, white, t2Border, 2)
            t2Prompt = littlefont.render("tryb 2 - sila ciągu zawsze działa", True, white)
            t2Prompt1 = littlefont.render("równolegle do powierzchni ziemi", True, white)
        else:
            pygame.draw.rect(screen, slategrey, t2Border, 2)
            t2Prompt = littlefont.render("tryb 2 - sila ciągu zawsze działa", True, slategrey)
            t2Prompt1 = littlefont.render("równolegle do powierzchni ziemi", True, slategrey)

        screen.blit(Y_0Prompt, (50, (screen_height - 700) + v_xSurface.get_height()))
        screen.blit(v_xPrompt, (50, (screen_height - 630) + v_xSurface.get_height()))
        screen.blit(v_yPrompt, (50, (screen_height - 560) + v_ySurface.get_height()))
        screen.blit(m_pPrompt, (50, (screen_height - 490) + m_pSurface.get_height()))
        screen.blit(H_startuPrompt, (50, (screen_height - 420) + H_startuSurface.get_height()))
        screen.blit(t0Prompt, (1100, (screen_height - 550) + t0Surface.get_height()))
        screen.blit(t1Prompt, (1100, (screen_height - 450) + t1Surface.get_height()))
        screen.blit(t1Prompt1, (1100, (screen_height - 420) + t1Surface.get_height()))
        screen.blit(t2Prompt, (1100, (screen_height - 350) + t2Surface.get_height()))
        screen.blit(t2Prompt1, (1100, (screen_height - 320) + t2Surface.get_height()))
        o_silniku = littlefont.render('WYBIERZ TRYB PRACY SILNIKÓW', True, white)
        screen.blit(o_silniku, (1100,(screen_height - 650) + t2Surface.get_height()))


        readyButtton = create_button((screen_width / 2) - (ready.get_width() / 2), screen_height * .9,
                                     ready.get_width() + 10, ready.get_height(), blackish, royalblue)

        screen.blit(ready, ((screen_width / 2) - (ready.get_width() / 2) + 5, int(screen_height * .9)))

        if readyButtton:
            if YY_0 != "":
                Y_location = float(YY_0)
            if vv_x != "":
                v_x = float(vv_x)
                v_x0 = float(vv_x)
            if vv_y != "":
                v_y = float(vv_y)
                v_y0 = float(vv_y)
            if mm_p != "":
                m_p = float(mm_p)
            if HH_startu != "":
                H_startu = float(HH_startu)
            if t0Active != False:
                tryb_pracy_silników = 0
            if t1Active != False:
                tryb_pracy_silników = 1
            if t2Active != False:
                tryb_pracy_silników = 2
            else:
                pass

            spin = 1  # spin = 1 odpalamy spinlauncha
            if spin == 1:

                #H_startu = 100000
                jak_często = 100

                obliczenia_numeryczne(0, 0, H_startu, 0)  # Silniki nie zadzaiłały

                reset_xyv()  # resetuje wartości po I przelocie

                obliczenia_numeryczne(1, 0, H_startu,
                                      0)  # I faza ruchu - do odpalenia silników
                if Hnpm > H_startu:
                    update_important_values(X_location, Y_location, droga, Hnpm / 1000, a_xy(a_x, a_y), v_xy(v_x, v_y))
                    test1 = 1

                obliczenia_numeryczne(2, 0, H_startu, tryb_pracy_silników)  # II faza ruchu - z silnikami

                if test == 1:
                    if test1 == 0:
                        update_important_values(x_forplot[1], y_forplot[1], droga_l[1], listH_xy[1], a_xy_l[1],
                                                v_xy_l[1])
                    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1],
                                            v_xy_l[-1])
                    test = 0

                obliczenia_numeryczne(3, 0, H_startu,
                                      0)  # III faza ruchu - po wyczerpaniu paliwa
                print(v_x0, v_y0, H_startu, tryb_pracy_silników, Y_location)
                wyświetlanie_wykresów(1, 1)  # 0 nie wyświetlam, 1 wyświetlam
                clear()

            powrot()
        pygame.display.update()
        clock.tick(15)

# piaskownica-----------------------------------------------------------------------------------------------------------
def piaskownica():
    global test, R_xy, v_x0, v_y0, jak_często, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, i, x_forplot, x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l, a_y_l, m_p, H_startu, tryb_pracy_silników
    global f, M_Z, R_Z
    title_text = font.render("WPROWADŹ DANE", True, gold)
    vv_x = ''
    vv_y = ''
    mm_p = ''
    HH_startu = ''
    t0 = '0'
    t1 = '1'
    t2 = '2'
    ff = ''
    MM_Z = ''
    RR_Z = ''
    YY_0 = ''

    v_xActive = False
    v_yActive = False
    m_pActive = False
    H_startuActive = False
    t0Active = False
    t1Active = False
    t2Active = False
    fActive = False
    M_ZActive = False
    R_ZActive = False
    Y_0Active = False

    ready = font.render("Gotowe!", True, white)

    while True:

        # ustawienia tla------------------------------
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(title_text, (40,20))

        # Y_0
        Y_0Surface = littlefont.render(YY_0, True, white)
        Y_0Border = pygame.Rect(650, screen_height - 690,
                                Y_0Surface.get_width() + 10, 40)
        screen.blit(Y_0Surface, (655, screen_height - 680))

        # v_x
        v_xSurface = littlefont.render(vv_x, True, white)
        v_xBorder = pygame.Rect(650, screen_height - 620,
                                v_xSurface.get_width() + 10, 40)
        screen.blit(v_xSurface, (655, screen_height - 610))

        # v_y
        v_ySurface = littlefont.render(vv_y, True, white)
        v_yBorder = pygame.Rect(650, screen_height - 550,
                                v_ySurface.get_width() + 10, 40)
        screen.blit(v_ySurface, (655, screen_height - 540))

        # m_p
        m_pSurface = littlefont.render(mm_p, True, white)
        m_pBorder = pygame.Rect(650, screen_height - 480,
                                m_pSurface.get_width() + 10, 40)
        screen.blit(m_pSurface, (655, screen_height - 470))

        # H_startu
        H_startuSurface = littlefont.render(HH_startu, True, white)
        H_startuBorder = pygame.Rect(650, screen_height - 410,
                                     H_startuSurface.get_width() + 10, 40)
        screen.blit(H_startuSurface, (655, screen_height - 400))

        # okineka tryb silników
        # t0
        t0Surface = littlefont.render(t0, True, white)
        t0Border = pygame.Rect(1000, screen_height - 540,
                               t0Surface.get_width() + 10, 40)
        screen.blit(t0Surface, (1005, screen_height - 530))
        # t1
        t1Surface = littlefont.render(t1, True, white)
        t1Border = pygame.Rect(1000, screen_height - 440,
                               t1Surface.get_width() + 10, 40)
        screen.blit(t1Surface, (1005, screen_height - 430))
        # t2
        t2Surface = littlefont.render(t2, True, white)
        t2Border = pygame.Rect(1000, screen_height - 340,
                               t2Surface.get_width() + 10, 40)
        screen.blit(t2Surface, (1005, screen_height - 330))
        #f
        fSurface = littlefont.render(ff, True, white)
        fBorder = pygame.Rect(650, screen_height - 330,
                                     fSurface.get_width() + 10, 40)
        screen.blit(fSurface, (655, screen_height - 320))
        #M_Z
        M_ZSurface = littlefont.render(MM_Z, True, white)
        M_ZBorder = pygame.Rect(650, screen_height - 260,
                                     M_ZSurface.get_width() + 10, 40)
        screen.blit(M_ZSurface, (655, screen_height - 250))
        #R_Z
        R_ZSurface = littlefont.render(RR_Z, True, white)
        R_ZBorder = pygame.Rect(650, screen_height - 180,
                                R_ZSurface.get_width() + 10, 40)
        screen.blit(R_ZSurface, (655, screen_height - 170))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Y_0Border.collidepoint(event.pos):
                    Y_0Active = True
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if v_xBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = True
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if v_yBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = True
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if m_pBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = True
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if H_startuBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = True
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if t0Border.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = True
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if t1Border.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = True
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if t2Border.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = True
                    fActive = False
                    M_ZActive = False
                    R_ZActive = False
                if fBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = True
                    M_ZActive = False
                    R_ZActive = False
                if M_ZBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = True
                    R_ZActive = False
                if R_ZBorder.collidepoint(event.pos):
                    Y_0Active = False
                    v_xActive = False
                    v_yActive = False
                    m_pActive = False
                    H_startuActive = False
                    t0Active = False
                    t1Active = False
                    t2Active = False
                    fActive = False
                    M_ZActive = False
                    R_ZActive = True

            if event.type == pygame.KEYDOWN:
                if R_ZActive:
                    if event.key == pygame.K_BACKSPACE:
                        RR_Z = RR_Z[:-1]
                    else:
                        RR_Z += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            Y_0Active = True
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if M_ZActive:
                    if event.key == pygame.K_BACKSPACE:
                        MM_Z = MM_Z[:-1]
                    else:
                        MM_Z += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = True
                if fActive:
                    if event.key == pygame.K_BACKSPACE:
                        ff = ff[:-1]
                    else:
                        ff += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = True
                            R_ZActive = False
                if H_startuActive:
                    if event.key == pygame.K_BACKSPACE:
                        HH_startu = HH_startu[:-1]
                    else:
                        HH_startu += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = True
                            M_ZActive = False
                            R_ZActive = False
                if m_pActive:
                    if event.key == pygame.K_BACKSPACE:
                        mm_p = mm_p[:-1]
                    else:
                        mm_p += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = True
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if v_yActive:
                    if event.key == pygame.K_BACKSPACE:
                        vv_y = vv_y[:-1]
                    else:
                        vv_y += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = True
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if v_xActive:
                    if event.key == pygame.K_BACKSPACE:
                        vv_x = vv_x[:-1]
                    else:
                        vv_x += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = True
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if Y_0Active:
                    if event.key == pygame.K_BACKSPACE:
                        YY_0 = YY_0[:-1]
                    else:
                        YY_0 += event.unicode
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = True
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if t2Active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = True
                            t1Active = False
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if t1Active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = False
                            t2Active = True
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if t0Active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            Y_0Active = False
                            v_xActive = False
                            v_yActive = False
                            m_pActive = False
                            H_startuActive = False
                            t0Active = False
                            t1Active = True
                            t2Active = False
                            fActive = False
                            M_ZActive = False
                            R_ZActive = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if Y_0Active:
            pygame.draw.rect(screen, white, Y_0Border, 2)
            Y_0Prompt = littlefont.render("WYSOKOŚĆ STARTU", True, white)
        else:
            pygame.draw.rect(screen, slategrey, Y_0Border, 2)
            Y_0Prompt = littlefont.render("WYSOKOŚĆ STARTU", True, slategrey)
        if v_xActive:
            pygame.draw.rect(screen, white, v_xBorder, 2)
            v_xPrompt = littlefont.render("POZIOMA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, white)
        else:
            pygame.draw.rect(screen, slategrey, v_xBorder, 2)
            v_xPrompt = littlefont.render("POZIOMA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, slategrey)

        if v_yActive:
            pygame.draw.rect(screen, white, v_yBorder, 2)
            v_yPrompt = littlefont.render("PIONOWA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, white)
        else:
            pygame.draw.rect(screen, slategrey, v_yBorder, 2)
            v_yPrompt = littlefont.render("PIONOWA WSPÓŁRZĘDNA PRĘDKOŚCI POCZĄTKOWEJ", True, slategrey)

        if m_pActive:
            pygame.draw.rect(screen, white, m_pBorder, 2)
            m_pPrompt = littlefont.render("MASA PALIWA (KG)", True, white)
        else:
            pygame.draw.rect(screen, slategrey, m_pBorder, 2)
            m_pPrompt = littlefont.render("MASA PALIWA (KG)", True, slategrey)

        if H_startuActive:
            pygame.draw.rect(screen, white, H_startuBorder, 2)
            H_startuPrompt = littlefont.render("WYSOKOŚĆ URUCHOMIENIA SILNIKÓW", True, white)
        else:
            pygame.draw.rect(screen, slategrey, H_startuBorder, 2)
            H_startuPrompt = littlefont.render("WYSOKOŚĆ URUCHOMIENIA SILNIKÓW", True, slategrey)

        if t0Active:
            pygame.draw.rect(screen, white, t0Border, 2)
            t0Prompt = littlefont.render("tryb 0 - samonaprowadzający na orbitę", True, white)

        else:
            pygame.draw.rect(screen, slategrey, t0Border, 2)
            t0Prompt = littlefont.render("tryb 0 - samonaprowadzający na orbitę", True, slategrey)

        if t1Active:
            pygame.draw.rect(screen, white, t1Border, 2)
            t1Prompt = littlefont.render("tryb 1 - siła ciągu działa wraz z trajektorią rakiety", True, white)
            t1Prompt1 = littlefont.render(" rakiety", True, white)

        else:
            pygame.draw.rect(screen, slategrey, t1Border, 2)
            t1Prompt = littlefont.render("tryb 1 - siła ciągu działa wraz z trajektorią", True, slategrey)
            t1Prompt1 = littlefont.render("rakiety", True, slategrey)

        if t2Active:
            pygame.draw.rect(screen, white, t2Border, 2)
            t2Prompt = littlefont.render("tryb 2 - sila ciągu zawsze działa", True, white)
            t2Prompt1 = littlefont.render("równolegle do powierzchni planety", True, white)

        else:
            pygame.draw.rect(screen, slategrey, t2Border, 2)
            t2Prompt = littlefont.render("tryb 2 - sila ciągu zawsze działa", True, slategrey)
            t2Prompt1 = littlefont.render("równolegle do powierzchni planety", True, slategrey)

        if fActive:
            pygame.draw.rect(screen, white, fBorder, 2)
            fPrompt = littlefont.render("WSPÓŁCZYNNIK TARCIA", True, white)
        else:
            pygame.draw.rect(screen, slategrey, fBorder, 2)
            fPrompt = littlefont.render("WSPÓŁCZYNNIK TARCIA", True, slategrey)

        if M_ZActive:
            pygame.draw.rect(screen, white, M_ZBorder, 2)
            M_ZPrompt = littlefont.render("MASA PLANETY (10^24 KG)", True, white)
        else:
            pygame.draw.rect(screen, slategrey, M_ZBorder, 2)
            M_ZPrompt = littlefont.render("MASA PLANETY (10^24 KG)", True, slategrey)

        if R_ZActive:
            pygame.draw.rect(screen, white, R_ZBorder, 2)
            R_ZPrompt = littlefont.render("PROMIEŃ PLANETY (KM)", True, white)
        else:
            pygame.draw.rect(screen, slategrey, R_ZBorder, 2)
            R_ZPrompt = littlefont.render("PROMIEŃ PLANETY (KM)", True, slategrey)

        screen.blit(Y_0Prompt, (50, (screen_height - 700) + v_xSurface.get_height()))
        screen.blit(v_xPrompt, (50, (screen_height - 630) + v_xSurface.get_height()))
        screen.blit(v_yPrompt, (50, (screen_height - 560) + v_ySurface.get_height()))
        screen.blit(m_pPrompt, (50, (screen_height - 490) + m_pSurface.get_height()))
        screen.blit(H_startuPrompt, (50, (screen_height - 420) + H_startuSurface.get_height()))
        screen.blit(t0Prompt, (1100, (screen_height - 550) + t0Surface.get_height()))
        screen.blit(t1Prompt, (1100, (screen_height - 450) + t1Surface.get_height()))
        screen.blit(t1Prompt1, (1100, (screen_height - 420) + t1Surface.get_height()))
        screen.blit(t2Prompt, (1100, (screen_height - 350) + t2Surface.get_height()))
        screen.blit(t2Prompt1, (1100, (screen_height - 320) + t2Surface.get_height()))
        o_silniku = littlefont.render('WYBIERZ TRYB PRACY SILNIKÓW', True, white)
        screen.blit(o_silniku, (1100, (screen_height - 650) + t2Surface.get_height()))
        screen.blit(fPrompt, (50, (screen_height-350) + fSurface.get_height()))
        screen.blit(M_ZPrompt, (50, (screen_height - 280) + M_ZSurface.get_height()))
        screen.blit(R_ZPrompt, (50, (screen_height - 210) + R_ZSurface.get_height()))

        readyButtton = create_button(1200 - 200, screen_height * .9,
                                     ready.get_width() + 10, ready.get_height(), blackish, royalblue)

        screen.blit(ready, (1200 - 195, int(screen_height * .9)))

        if readyButtton:
            if YY_0 != "":
                Y_location = float(YY_0)
            if vv_x != "":
                v_x = float(vv_x)
                v_x0 = float(vv_x)
            if vv_y != "":
                v_y = float(vv_y)
                v_y0 = float(vv_y)
            if mm_p != "":
                m_p = float(mm_p)
            if HH_startu != "":
                H_startu = float(HH_startu)
            if ff != "":
                f = float(ff)
            if MM_Z != "":
                M_Z = float(MM_Z)*10**24
            if RR_Z != "":
                R_Z = float(RR_Z)
            if t0Active != False:
                tryb_pracy_silników = 0
            if t1Active != False:
                tryb_pracy_silników = 1
            if t2Active != False:
                tryb_pracy_silników = 2
            else:
                pass

            spin = 0  # spin = 1 odpalamy spinlauncha
            if spin != 1:
                test = 1
                while test == 1:
                    #v_x0 = 100
                    #v_y0 = 0
                    v_x = v_x0
                    v_y = v_y0
                    if v_x0 >= 0:
                        test = 0
                    else:
                        test = 1

                test = 1
                while test == 1:
                    #f = f  # drag coeficient
                    #M_Z = 5.98 * 10 ** 24  # masa planety
                    #R_Z = 6371000  # promień planety
                    if M_Z > 0 and R_Z > 0 and f > 0:
                        test = 0
                    else:
                        test = 1
                print('1')
                test = 1
                while test == 1:
                    Y_location = R_Z + 30  # wysokość staartowa
                    y_forplot[0] = Y_location
                    R_xy = Y_location
                    if Y_location - R_Z > 0:
                        test = 0
                    else:
                        test = 1
                print('2')
                test = 1
                while test == 1:
                    m_r = m_r  # masa całej rakiety
                    m_r_p = m_r  # nie zmieniamy
                    m_m = m_r_p  # nie zmieniamy
                    m_p = m_p  # masa paliwa - nie może być przecież większa od rakiety...
                    if m_r * 0.9 - m_p >= 0:
                        test = 0
                    else:
                        test = 1
                print('3')
                test = 1
                while test == 1:
                    #H_startu = 19  # wybieramy wysokość na kkórej mają zacząć pracować sylniki
                    if H_startu >= 0:
                        test = 0
                    else:
                        test = 1

                print('4')
                test = 1
                while test == 1:
                    tryb = 0  # tryb pracy silników optymalnie 0 - samonaprowadzający na orbitę,
                    # 1 - siła ciągu działa wraz z trajektorią rakiety, 2 - sila ciągu zawsze działa równolegle do powierzchni ziemi
                    if tryb == 0 or tryb == 1 or tryb == 2:
                        test = 0
                    else:
                        test = 1

                test = 1
                while test == 1:
                    jak_często = 1  # jeśli masz podejrzenie, że twój wykres będzie mały, zmniejsz (w przedziałach od 1 do 1000)
                    if 1 <= jak_często <= 1000:
                        test = 0
                    else:
                        test = 1

                print(droga_l)
                obliczenia_numeryczne(1, 0, H_startu,
                                      tryb_pracy_silników)  # I faza ruchu - do odpalenia silników
                print(droga_l)
                '''try:
                    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])
                except:
                    test = 1
                    a_y = -k * cos(X_location, Y_location) * R_xy ** (-2)
                    a_x = -k * sin(X_location, Y_location) * R_xy ** (-2)
                    a_t_x = 0.1
                    a_t_y = 0.1
                    pass
                print('7')
                obliczenia_numeryczne(2, 0, wysokość=H_startu, tryb_pracy_silników=0)  # II faza ruchu - z silnikami
                print('8')
                if test == 1:
                    try:
                        update_important_values(x_forplot[0], y_forplot[0], droga_l[0], listH_xy[0], a_xy_l[0], v_xy_l[0])
                    except:
                        print(x_forplot[0])
                        print(x_forplot[0], y_forplot[0])
                        print(x_forplot[0], y_forplot[0], droga_l[0])
                        print(x_forplot[0], y_forplot[0], droga_l[0], listH_xy[0])
                        print(x_forplot[0], y_forplot[0], droga_l[0], listH_xy[0], a_xy_l[0])
                        print(x_forplot[0], y_forplot[0], droga_l[0], listH_xy[0], a_xy_l[0], v_xy_l[0])
                update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])'''  # stara obsługa błędów

                test1 = Hnpm
                if 0 < Hnpm < H_startu:
                    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1],
                                            v_xy_l[-1])

                obliczenia_numeryczne(2, 0, H_startu, tryb_pracy_silników)  # II faza ruchu - z silnikami

                if Hnpm > H_startu:
                    update_important_values(x_forplot[1], y_forplot[1], droga_l[1], listH_xy[1], a_xy_l[1], v_xy_l[1])

                if test == 1:
                    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1],
                                            v_xy_l[-1])

                obliczenia_numeryczne(3, 0, H_startu,
                                      tryb_pracy_silników)  # III faza ruchu - po wyczerpaniu paliwa
                print(v_x0, v_y0, H_startu, m_p, tryb_pracy_silników, f, M_Z, R_Z, Y_location)
                wyświetlanie_wykresów(1, 1)  # 0 nie wyświetlam, 1 wyświetlam
                clear()

            powrot()
        pygame.display.update()
        clock.tick(15)

# o spinlaunchu----------------------------------------------------------------------------------------------------------
def spinlaunch_info():
    title_text = titlefont.render("O SPINLAUNCHU", True, gold)

    next = littlefont.render("DALEJ", True, white)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 50))
        screen.blit(infoImg, ((screen_width - infoImg.get_width()) / 2, 200))
        screen.blit(rocketImg, (100, 500))
        screen.blit(spinImg, (1100, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        nextButtton = create_button((screen_width / 2) - (next.get_width() / 2) - 5, screen_height-70,
                                    next.get_width() + 10, next.get_height()+10, blackish, royalblue)

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2), int(screen_height-66)))

        if nextButtton:
            teoria()

        pygame.display.update()
        clock.tick(15)

# jak wyslac satelite----------------------------------------------------------------------------------------------------
def teoria():
    title_text = titlefont.render("TEORIA", True, gold)

    next = littlefont.render("DALEJ", True, white)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 50))
        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width()) / 2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        nextButtton = create_button((screen_width / 2) - (next.get_width() / 2) + 195, screen_height-70,
                                    next.get_width() + 10, next.get_height()+10, blackish, royalblue)

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2) + 200, int(screen_height - 66)))

        if nextButtton:
            parametry()

        pygame.display.update()
        clock.tick(15)

def parametry():
    title_text = titlefont.render("PARAMETRY STAŁE", True, gold)

    next = littlefont.render("DALEJ", True, white)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 50))
        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width()) / 2, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        nextButtton = create_button((screen_width / 2) - (next.get_width() / 2), screen_height - 70,
                                    next.get_width() + 10, next.get_height()+10, blackish, royalblue)

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2) + 5, int(screen_height - 66)))

        if nextButtton:
            wybor_trybu()

        pygame.display.update()
        clock.tick(15)

# pytanie o powrót
def powrot():
    instruction = titlefont.render("WYBIERZ OPCJĘ: ", True, gold)
    backText = littlefont.render("SPINLAUNCH", True, white)
    plotText = littlefont.render("PIASKOWNICA", True, white)
    anotherText = littlefont.render("WYJŚCIE Z PROGRAMU", True, white)

    running = True
    while (running):
        screen.fill((0, 0, 0))
        screen.blit(misteryImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 50))

        backButtton = create_button((screen_width / 2) - 125, int(screen_height-550), 250, 50, blackish, royalblue)

        if backButtton:
            data_input()

        screen.blit(backText, ((screen_width / 2) - (backText.get_width() / 2), int(screen_height - 535)))

        plotButtton = create_button((screen_width / 2) - 125, screen_height / 2, 250, 50, blackish, royalblue)

        if plotButtton:
            piaskownica()

        screen.blit(plotText, ((screen_width / 2) - (plotText.get_width() / 2), screen_height - 385))


        anotherButtton = create_button((screen_width / 2) - 125, screen_height - 250, 250, 50, blackish, royalblue)

        if anotherButtton:
            pygame.quit()
            sys.exit()

        screen.blit(anotherText, ((screen_width / 2) - (anotherText.get_width() / 2), (screen_height - 235)))


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

# pętla glowna-----------------------------------------------------------------------------------------------------------
def oknowyboru():
    pygame.display.set_mode((1520, 800))
    pygame.display.set_caption('spinlaunch')
    running = True
    while (running):
        intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()

pygame.init()
oknowyboru()