import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Slider

########################################################################################################################

def przywracanie_do_poczatkowych():
    global M_Z, R_Z, G, V_1, x_0, y_00, y_0, k, Dt, f, S, m_m, v_g, m_r_p, jak_często, tryb_pracy_silników, v_x0,v_y0, m_p0, H_startu
    global droga, X_location, Y_location, R_xy, Hnpm, v_x, v_y, i, spin, m_r, m_p, Dm_1s, test, test1, czy_faza1, czy_faza2, czy_faza3
    global x_forplot, x1_forplot, y_forplot, y1_forplot, listR_xy, listH_xy, listH_xy1, wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x, v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly, ro
    # Stałe------------------------------------------------------------------------------------------------------------------
    M_Z = 5.98 * 10 ** 24  # masa ziemi
    R_Z = 6371000  # promień ziemi
    G = 6.6743 * 10 ** (-11)  # stała grawitacyjna
    V_1 = np.sqrt(G * M_Z / R_Z)  # I prędkośćkosmiczna
    x_0 = 0  # pocztkowy x
    y_00 = 20
    y_0 = R_Z + y_00  # pocztkowy y
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
    v_x0 = 1000  # prędkość początkowa y
    v_y0 = 1800  # prędkość początkowa y
    m_p0 = 600  # masa paliwa
    H_startu = 100000
    ro = 1.23435 #gęsość atmosfery

    # zmienne----------------------------------------------------------------------------------------------------------------
    droga = 0  # zmienna drogi
    X_location = x_0  # zmienna położenia x
    Y_location = y_0  # zmienna położenia y
    R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5  # odległość rakiety od środka ziemi
    Hnpm = R_xy - R_Z  # wysokość npm
    v_x = v_x0  # zmienna prędkości x
    v_y = v_y0  # zmienna prędkości y
    i = 0  # ilość punktów
    spin = 0
    m_r = m_r_p  # zmienna masa rakiety
    m_p = m_p0
    Dm_1s = m_p / 150  # paliwo tracone w czasie 1 s
    test = 0
    test1 = 0
    czy_faza1 = 0
    czy_faza2 = 0
    czy_faza3 = 0
    x_forplot, x1_forplot = [x_0], [x_0]
    y_forplot, y1_forplot = [y_0], [y_0]
    listR_xy = [R_xy]  # potrzebne? -> TAK
    listH_xy, listH_xy1 = [], []
    wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x = [], [], [], [], [], []
    v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly = [], [], [], [], [], [], [], [], []

przywracanie_do_poczatkowych()

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

            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 1000:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 1000:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 1000:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 1000:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))
    if faza == 2:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m) + a_t_x  # x-acceleration update

            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 1000:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m) + a_t_x # x-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 1000:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m) + a_t_y # x-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 1000:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m) + a_t_y # y-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 1000:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))
    if faza == 3:
        if v_x > 0:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update

            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 1000:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))

        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))

            if Hnpm < 1000:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 1000:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
            if Hnpm >= 1000 and i % jak_często == 0:
                d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

            if Hnpm < 1000:
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


        if Hnpm >= 1000 and i % jak_często == 0:
            x1_forplot.append(X_location)
            y1_forplot.append(Y_location)
            listH_xy1.append(Hnpm)

        if Hnpm < 1000:
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

        if Hnpm >= 1000 and i % jak_często == 0:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append(v_x)
            v_y_l.append(v_y)
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

        if Hnpm < 1000:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
            Hnpm = R_xy - R_Z

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append(v_x)
            v_y_l.append(v_y)
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

        if Hnpm >= 1000 and i % jak_często == 0:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append(v_x)
            v_y_l.append(v_y)
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

        if Hnpm < 1000:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
            Hnpm = R_xy - R_Z

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append(v_x)
            v_y_l.append(v_y)
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

        if Hnpm >= 1000 and i % jak_często == 0:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append(v_x)
            v_y_l.append(v_y)
            droga_l.append(droga)
            a_y_l.append(a_y)
            a_x_l.append(a_x)
            a_xy_l.append(a_xy(a_x, a_y))

        if Hnpm < 1000:
            x_forplot.append(X_location)
            y_forplot.append(Y_location)

            R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
            droga = droga + ((x_forplot[-1] - x_forplot[-2]) ** 2 + (y_forplot[-1] - y_forplot[-2]) ** 2) ** 0.5
            Hnpm = R_xy - R_Z

            listR_xy.append(R_xy)
            listH_xy.append(Hnpm / 1000)
            v_xy_l.append(v_xy(v_x, v_y))
            v_x_l.append(v_x)
            v_y_l.append(v_y)
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
    global R_xy, X_location, Y_location, m_r, droga, Hnpm, H_startu, jak_często, test, m_p, czy_faza1, czy_faza2, czy_faza3

    if faza == 0:
        while R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if p_important_values == 1 and i % jak_często == 0:
                print_important_values(faza)

    if faza == 1:
        while Hnpm < wysokość and R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)
            czy_faza1 = 1
            if p_important_values == 1 and i % jak_często == 0:
                print_important_values(faza)
            if Hnpm < 1000:
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
            czy_faza2 = 1
            if p_important_values == 1 and i % jak_często == 0:
                print_important_values(faza)
            if Hnpm < 1000:
                print_important_values(faza)

    if faza == 3:
        while R_xy > R_Z:

            if R_Z <= 6371000:
                if test ==1:
                    if droga > 6 * 6371000 and X_location > wazny_x[1]:
                        break
                if droga > 8 * 6371000:
                    break
            else:
                if test ==1:
                    if droga > 6 * R_Z and X_location > wazny_x[1]:
                        break
                if droga > 8 * R_Z:
                    break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)
            czy_faza3 = 1
            if p_important_values == 1 and i % jak_często == 0:
                print_important_values(faza)
            if Hnpm < 1000:
                print_important_values(faza)

def prędkość_kosmiczna(R):
    return np.sqrt(G * M_Z / R)

def air_density(R_xy):  # air density formula
    global ro
    if R_xy < R_Z + 100000:
        return np.exp(((R_Z - R_xy) / 1000 / 9.038)) * ro
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
            f'a_x: {round(a_x, 2)} m/s^2 ||  ay: {round(a_y, 2)} m/s^2 || a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)} || v_x = {round(v_x, 2)} || v_y = {round(v_y, 2)}')
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
        plt.plot((R_Z + 85000) * np.cos(alfa), (R_Z + 85000) * np.sin(alfa), color='y', lw=0.3, label='Koniec atmosfery')
        try:
            plt.scatter(wazny_x, wazny_y)  # początak i start działania silników
        except:
            pass
        #plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
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
        plt.plot(droga_l, d_a_ly, color='r', lw=1, ls='-', label='Przyśp. oY oporów atm.')
        plt.plot(droga_l, d_a_lx, label='Przyśp. oX oporów atm.')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        aa = plt.subplot(411)
        cursor1 = Cursor(aa, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(412)
        plt.plot(droga_l, a_xy_l, color='g', lw=3, ls='dotted', label='Przyśp. Całkowite')
        plt.plot(droga_l, a_x_l, color='r', lw=1, ls='-', label='Przyśp. na oX')
        plt.plot(droga_l, a_y_l, color='y', lw=1, ls='-', label='Przyśp. na oY')
        plt.scatter(wazny_d, wazny_a, label='Działanie silników')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        ab = plt.subplot(412)
        cursor2 = Cursor(ab, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(413)
        plt.plot(droga_l, v_xy_l, color='g', lw=3, ls='dotted', label='Prędkość Całk.')
        plt.plot(droga_l, v_x_l, color='r', lw=1, ls='-', label='Prędkość na oX]')
        plt.plot(droga_l, v_y_l, color='y', lw=1, ls='-', label='Prędkość na oY')
        plt.scatter(wazny_d, wazny_v, label='Działanie silników')
        plt.legend()
        plt.xlabel('km')
        plt.ylabel('m/s)')

        ac = plt.subplot(413)
        cursor3 = Cursor(ac, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(414)
        if max(listH_xy) > 50:
            plt.subplot(414)
            x = np.linspace(0, max(droga_l), 100)
            y = 0 * x + 100
            plt.plot(x, y, color='b', lw=1, ls='--', label='koniec atmosfery')
        else:
            pass
        print('a')
        plt.plot(droga_l, listH_xy, color='b', lw=1, ls='-', label='Wysokość nad pow.')
        plt.scatter(wazny_d, wazny_h, label='Działanie silników')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('km')

        ad = plt.subplot(414)
        cursor4 = Cursor(ad, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        #figManager = plt.get_current_fig_manager()
        #figManager.window.showMaximized()
        plt.show()
        print('aa')