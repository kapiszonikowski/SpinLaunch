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
m_p = 600  # masa paliwa
Dm_1s = m_p / 150  # paliwo tracone w czasie 1 s
test = 0
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
            d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))
        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
            d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
            d_a_ly.append(+drag_acceleration(R_xy, v_y, m_m))

    if faza == 2:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_r) + a_t_x  # x-acceleration update
            if i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_r))
        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_r) + a_t_x  # x-acceleration update
            if i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_r))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_r) + a_t_y  # x-acceleration update
            if i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_r))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_r) + a_t_y  # y-acceleration update
            if i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_r))
    if faza == 3:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_r)  # x-acceleration update
            if i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_r))
        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_r)  # x-acceleration update
            if i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_r))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_r)  # x-acceleration update
            if i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_r))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_r)  # y-acceleration update
            if i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_r))


def updates_appends(faza):
    global R_xy, jak_często, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, i, x_forplot, x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l, a_y_l
    if faza == 0:
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

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

        x_forplot.append(X_location)
        y_forplot.append(Y_location)

        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
        Hnpm = R_xy - R_Z

        i += 1

        droga_l.append(droga)
        listR_xy.append(R_xy)
        listH_xy.append(Hnpm / 1000)
        v_xy_l.append(v_xy(v_x, v_y))
        v_x_l.append(v_x)
        v_y_l.append((v_y))
        a_y_l.append(a_y)
        a_x_l.append(a_x)
        a_xy_l.append(a_xy(a_x, a_y))

    if faza == 2:
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

        i += 1

        if i % jak_często == 0:
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

        if i % jak_często == 0:
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
    global R_xy, v_x, X_location, Y_location, v_y, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x, test

    if prędkość_kosmiczna(R_xy) * cos(X_location, Y_location) > v_x:
        a_t_x = thrust_acceleration1()
        m_r = m_r - Dm_1s * Dt / 1  # rocket mass update
        a_t_y = 0
    else:
        a_t_x = 0
        if -prędkość_kosmiczna(R_xy) * sin(X_location, Y_location) < v_y:
            a_t_y = -sin(X_location, Y_location) * thrust_acceleration1()
            m_r = m_r - Dm_1s * Dt * sin(X_location, Y_location) / 1  # rocket mass update
        else:
            a_t_y = 0
    if a_t_x != 0 or a_t_y != 0:
        test = 1
    return a_t_x, a_t_y


def obliczenia_numeryczne(faza, p_important_values, wysokość, tryb_pracy_silników):
    global R_xy, X_location, Y_location, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x, H_startu, jak_często, test

    if faza == 0:
        while R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values()

    if faza == 1:
        while Hnpm < wysokość and R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values()

    if faza == 2:

        while m_r > m_r_p - m_p and R_Z < R_xy:

            if tryb_pracy_silników == 0:
                naprowadzanie_na_orbite()
                if a_t_x == 0 and a_t_y == 0:
                    break

            if tryb_pracy_silników == 1:
                try:
                    a_t_x = D_osi(x_forplot[-1], x_forplot[-2]) * thrust_acceleration(x_forplot[-1], x_forplot[-2],
                                                                                      y_forplot[-1], y_forplot[-2])
                    a_t_y = D_osi(y_forplot[-1], y_forplot[-2]) * thrust_acceleration(x_forplot[-1], x_forplot[-2],
                                                                                      y_forplot[-1], y_forplot[
                                                                                          -2])  # stare przyśpieszenie
                    m_r = m_r - Dm_1s * Dt / 1  # rocket mass update
                except:
                    a_t_x = 0
                    a_t_y = 0
                if a_t_x != 0 or a_t_y != 0:
                    test = 1
                if v_x > V_1 and Hnpm > 8500:
                    break

            if tryb_pracy_silników == 2:
                # try:
                a_t_x = cos(X_location, Y_location) * thrust_acceleration1()
                a_t_y = -sin(X_location, Y_location) * thrust_acceleration1()
                m_r = m_r - Dm_1s * Dt / 1  # rocket mass update
                # except:
                # pass
                if a_t_x != 0 or a_t_y != 0:
                    test = 1
                if v_x > V_1 and Hnpm > 85000:  # to było o 1 tab do przodu
                    break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values()

    if faza == 3:
        while R_xy > R_Z:

            if droga > 6 * R_Z and X_location > wazny_x[1]:
                break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1:
                print_important_values()


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


def print_important_values():
    try:
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
    global wazny_h, x_forplot, x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l, a_y_l, droga

    x_forplot, x1_forplot = [X_location], [X_location]
    y_forplot, y1_forplot = [Y_location], [Y_location]
    listR_xy = [R_xy]  # potrzebne? -> TAK
    listH_xy, listH_xy1 = [], []
    wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x = [], [], [], [], [], []
    v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly = [], [], [], [], [], [], [], [], []
    droga = 0
def wyświetlanie_wykresów(orbita, dane):
    # Tworzenie tekstu-------------------------------------------------------------------------------------------------------
    # nd = round((droga / 1000), 2)
    # nw = round((max(listR_xy) - R_Z) / 1000, 2)
    # napis_drogi = f'droga przebyta przez ciao: {nd}km'
    # napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
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
        theta = np.arange(0, np.pi * 2, 0.01)
        plt.plot((R_Z + 23.3) * np.cos(theta), (R_Z + 23.3) * np.sin(theta), lw=2, color='b',
                 label='Ziemia')  # model ziemi
        plt.plot((R_Z + 85000) * np.cos(theta), (R_Z + 85000) * np.sin(theta), color='y', lw=0.3)
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

        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        plt.show()
        print('jaaa')

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
        y = 0 * x + 85
        plt.plot(x, y, color='b', lw=1, ls='--', label='koniec atmosfery')
        plt.plot(droga_l, listH_xy, color='b', lw=1, ls='-', label='Hxy_(d) [km]')
        plt.scatter(wazny_d, wazny_h, label='d_h_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('km')

        ad = plt.subplot(414)
        cursor4 = Cursor(ad, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        plt.show()


import time

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
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms", 20)
titlefont = pygame.font.SysFont('timesnewroman', 50)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)

# obrazy----------------------------------------------------------------------------------------------------------------
spinlaunchImg = pygame.image.load("SpinLaunch.logo.jpg")
earthImg = pygame.image.load('earth.jpg')


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


# wyswietlanie wykresu--------------------------------------------------------------------------------------------------
def plot_display(a, b):
    x = np.linspace(0, 2 * np.pi, 100)
    y = (np.sin(a * x) ** b)
    plt.plot(x, y, color='g', lw=1, label='sin(a*x)')
    plt.show()


# ekran 1. -------------------------------------------------------------------------------------------------------------
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
        screen.blit(startbuttontext, ((screen_width / 2 - 50), 725))

        screen.blit(spinlaunchImg, ((screen_width - spinlaunchImg.get_width()) / 2, 300))

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
    instruction = font.render("wybierz opcje: program-wprowadzanie danych, teoria - wiecej o zjawisku", True, slategrey)
    programText = font.render("PROGRAM", True, blackish)
    teoriaText = font.render("TEORIA", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 0))

        programButtton = create_button((screen_width / 2) - 100, int(screen_height * .33), 200, 50, lightgrey,
                                       slategrey)

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


# wprowadzanie danych----------------------------------------------------------------------------------------------------
def data_input():
    global test, R_xy, v_x0, v_y0, jak_często, v_x, X_location, Y_location, v_y, m_r, droga, Hnpm, i, x_forplot, x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l, a_y_l

    title_text = font.render("wprowadzanie danych", True, slategrey)
    vv_x = ""
    vv_y = ''
    v_xActive = False
    v_yActive = False

    ready = font.render("Gotowe!", True, blackish)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))

        v_xSurface = font.render(vv_x, True, white)

        v_xBorder = pygame.Rect(((screen_width - v_xSurface.get_width()) / 2) - 10, screen_height * .20,
                                v_xSurface.get_width() + 10, 50)

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
                                (screen_height - 500) + v_ySurface.get_height()))

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

            spin = 1  # spin = 1 odpalamy spinlauncha
            if spin == 1:

                H_startu = 100000
                jak_często = 1

                obliczenia_numeryczne(0, 0, wysokość=H_startu, tryb_pracy_silników=2)  # Silniki nie zadzaiłały

                reset_xyv()  # resetuje wartości po I przelocie
                #print('a')

                obliczenia_numeryczne(1, 0, wysokość=H_startu,
                                      tryb_pracy_silników=2)  # I faza ruchu - do odpalenia silników

                #print('a')

                obliczenia_numeryczne(2, 0, wysokość=H_startu, tryb_pracy_silników=2)  # II faza ruchu - z silnikami
                #print('a')

                if test == 1:
                    update_important_values(x_forplot[0], y_forplot[0], droga_l[0], listH_xy[0], a_xy_l[0], v_xy_l[0])
                    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1],
                                            v_xy_l[-1])
                    test = 0
                #print('a')
                obliczenia_numeryczne(3, 0, wysokość=H_startu,
                                      tryb_pracy_silników=2)  # III faza ruchu - po wyczerpaniu paliwa
                #print('a')
                #print(x1_forplot)
                #print(d_a_ly)

                wyświetlanie_wykresów(1, 1)  # 0 nie wyświetlam, 1 wyświetlam
                #print('a')

            if spin != 1:
                test = 1
                while test == 1:
                    v_x0 = 100
                    v_y0 = 0
                    v_x = v_x0
                    v_y = v_y0
                    if v_x0 >= 0:
                        test = 0
                    else:
                        test = 1

                test = 1
                while test == 1:
                    f = f  # drag coeficient
                    M_Z = 5.98 * 10 ** 24  # masa planety
                    R_Z = 6371000  # promień planety
                    if M_Z > 0 and R_Z > 0 and f > 0:
                        test = 0
                    else:
                        test = 1
                #print('1')
                test = 1
                while test == 1:
                    Y_location = R_Z + 30  # wysokość staartowa
                    y_forplot[0] = Y_location
                    R_xy = Y_location
                    if Y_location - R_Z > 0:
                        test = 0
                    else:
                        test = 1
                #print('2')
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
                #print('3')
                test = 1
                while test == 1:
                    H_startu = 19  # wybieramy wysokość na kkórej mają zacząć pracować sylniki
                    if H_startu >= 0:
                        test = 0
                    else:
                        test = 1

                #print('4')
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

                #print(droga_l)
                obliczenia_numeryczne(1, 0, wysokość=H_startu,
                                      tryb_pracy_silników=tryb)  # I faza ruchu - do odpalenia silników
                #print(droga_l)
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

                obliczenia_numeryczne(2, 0, wysokość=H_startu, tryb_pracy_silników=tryb)  # II faza ruchu - z silnikami
                #print(droga_l)
                if Hnpm > H_startu:
                    update_important_values(x_forplot[1], y_forplot[1], droga_l[1], listH_xy[1], a_xy_l[1], v_xy_l[1])

                if test == 1:
                    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1],
                                            v_xy_l[-1])

                obliczenia_numeryczne(3, 0, wysokość=H_startu,
                                      tryb_pracy_silników=tryb)  # III faza ruchu - po wyczerpaniu paliwa
                #print(droga_l)

                wyświetlanie_wykresów(0, 1)  # 0 nie wyświetlam, 1 wyświetlam

            clear()
            powrot()
        pygame.display.update()
        clock.tick(15)


# o spinlaunchu----------------------------------------------------------------------------------------------------------
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


# jak wyslac satelite----------------------------------------------------------------------------------------------------
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

        screen.blit(next, ((screen_width / 2) - (next.get_width() / 2) + 200, int(screen_height * .9)))

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


# pytanie o powrót
def powrot():
    #matplotlib.use('TkAgg')
    instruction = font.render("wybierz opcje: ", True, slategrey)
    backText = font.render("POWROT DO WPROWADZANIA ZMIENNYCH", True, blackish)
    plotText = font.render("WYJSCIE Z PROGRAMU", True, blackish)

    running = True
    while (running):
        screen.fill((0, 0, 0))
        screen.blit(earthImg, (0, 0))
        screen.blit(instruction, ((screen_width - instruction.get_width()) / 2, 0))

        backButtton = create_button((screen_width / 2) - 100, int(screen_height * .33), 200, 50, lightgrey, slategrey)

        if backButtton:
            data_input()

        screen.blit(backText, ((screen_width / 2) - (backText.get_width() / 2), int(screen_height * .33)))

        plotButtton = create_button((screen_width / 2) - 100, screen_height / 2, 200, 50, lightgrey, slategrey)

        if plotButtton:
            pygame.quit()
            sys.exit()


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


# pętla glowna-----------------------------------------------------------------------------------------------------------
def oknowyboru():
    pygame.display.set_mode((1520, 800))
    pygame.display.set_caption('okno wyboru')
    running = True
    while (running):
        intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()


pygame.init()
oknowyboru()

