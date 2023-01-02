import numpy as np
import numpy as nu
import matplotlib.pyplot as plt
import tkinter as tk #biblioteka do wprowadzania danych
from matplotlib.widgets import Slider
import time

#Stałe------------------------------------------------------------------------------------------------------------------
M_Z = 5.98 * 10 ** 24           #masa ziemi
R_Z = 6371000                   #promień ziemi
G = 6.6743 * 10 ** (-11)        #stała grawitacyjna
V_1 = nu.sqrt(G * M_Z / R_Z)    #I prędkośćkosmiczna
x_0 = 0                         #pocztkowy x
y_0 = R_Z + 20                  #pocztkowy y
k = G * M_Z                     #wsp staej grawitacji
Dt = 0.01                       #czas aktualizacji
#alpha = nu.angle(0, deg=True)
f = 0.13                 # Drag coefficient for rocket
S = nu.pi * 0.5 ** 2    # Rocket cross-section
m_m = 10300         #masa całego modułu
v_g = 8750          #prędkość gazów wylotowych
m_r_p = 1000          #początkowa masa rakiety
jak_często = 1000                                   #gęstość rozmieszczenia punktów - dla 100 pokazuje lokalizacje co 1s

#zmienne----------------------------------------------------------------------------------------------------------------
droga = 0                                           #zmienna drogi
v_x0 = 1000                                         #prędkość początkowa y
v_y0 = 1800                                         #prędkość początkowa y
X_location = x_0                                    #zmienna położenia x
Y_location = y_0                                    #zmienna położenia y
R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5   #odległość rakiety od środka ziemi
Hnpm = R_xy - R_Z                                   #wysokość npm
v_x = v_x0                                          #zmienna prędkości x
v_y = v_y0                                          #zmienna prędkości y

i = 0                                               #ilość punktów

m_r = m_r_p     #zmienna masa rakiety
m_p = 600        #masa paliwa
Dm_1s = m_p / 150   #paliwo tracone w czasie 1 s

#Listy------------------------------------------------------------------------------------------------------------------
x_forplot, x1_forplot  = [X_location], [X_location]
y_forplot, y1_forplot = [Y_location], [Y_location]
listR_xy = [R_xy]       #potrzebne? -> TAK
listH_xy, listH_xy1 = [], []
wazny_h, wazny_d, wazny_v, wazny_y, wazny_a, wazny_x = [], [], [], [], [], []
v_xy_l, v_x_l, v_y_l, droga_l, a_x_l, a_y_l, a_xy_l, d_a_lx, d_a_ly = [], [], [], [], [], [], [], [], []

#Funkcje----------------------------------------------------------------------------------------------------------------
def prędkość_kosmiczna(R):
    return nu.sqrt(G * M_Z / R)

def air_density(R_xy):                    # air density formula
    if R_xy < R_Z + 100000:
        return np.exp(((R_Z - R_xy) / 1000 / 9.038)) * 1.23435
    else:
        return 0

def drag_acceleration(R_xy, speed, mr):   # drag from the height and air density
    return 0.5 * air_density(R_xy) * S * speed ** 2 * f / mr

def cos(x, y):
    return y / nu.sqrt(x ** 2 + y ** 2)

def sin(x, y):
    return x / nu.sqrt(x ** 2 + y ** 2)

def D_osi(p1, p0):
    return p1 - p0

def przemieszczenie(x1, x0, y1, y0):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def thrust_acceleration(x1, x0, y1, y0):
    return 1 / przemieszczenie(x1, x0, y1, y0) * (v_g * Dm_1s + 0.01 * S * 10 * air_density(R_xy)) / m_r

def thrust_acceleration1():
    return  (v_g * Dm_1s + 0.01 * S * 10 * air_density(R_xy)) / m_r

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
        print(f'a_x: {round(a_x, 2)} m/s^2 ||  ay: {round(a_y, 2)} m/s^2 || a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)} || v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
        print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m] || H: {round(R_xy - R_Z)}[m] ||  t: {round(i / 3600000, 2)}[s] || m_r: {m_r : .8}\n')
    except:
        print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m] || H: {Hnpm}[m] ||  t: {round(i / 3600000, 2)}[s]')

def reset_xyv():
    global v_x, v_y, X_location, Y_location
    v_x = v_x0
    v_y = v_y0
    X_location = x_0
    Y_location = y_0

def obliczanie_przyspieszenia(faza):
    global R_xy, v_x, X_location, Y_location, v_y, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x
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
                                                                                m_r) + a_t_x # x-acceleration update
            if i % jak_często == 0:
                d_a_lx.append(-drag_acceleration(R_xy, v_x, m_r))
        else:
            a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                m_r) + a_t_x # x-acceleration update
            if i % jak_często == 0:
                d_a_lx.append(drag_acceleration(R_xy, v_x, m_r))
        if v_y > 0:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                m_r) + a_t_y # x-acceleration update
            if i % jak_często == 0:
                d_a_ly.append(-drag_acceleration(R_xy, v_y, m_r))
        else:
            a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                m_r) + a_t_y # y-acceleration update
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
    global R_xy, v_x, X_location, Y_location, v_y, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x, i, x_forplot,\
        x1_forplot, y_forplot, y1_forplot, droga_l, listH_xy, listH_xy1, listR_xy, v_xy_l, v_x_l, v_y_l, a_xy_l, a_x_l,\
        a_y_l
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
    global R_xy, v_x, X_location, Y_location, v_y, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x

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
    return a_t_x, a_t_y

def obliczenia_numeryczne(faza, important_values):
    global R_xy, v_x, X_location, Y_location, v_y, m_r, a_x, a_y, droga, Hnpm, a_t_x, a_t_y, a_x

    if faza == 0:
        while R_xy > R_Z:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if important_values == 1:
                print_important_values()

    if faza == 1:
        while Hnpm < 140000:
            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if important_values == 1:
                print_important_values()

    if faza == 2:
        while m_r > m_r_p - m_p and R_Z < R_xy:

            naprowadzanie_na_orbite()

            if a_t_x == 0 and a_t_y == 0:
                break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if important_values == 1:
                print_important_values()

    if faza == 3:
        while R_xy > R_Z:

            if droga > 6*R_Z and X_location > wazny_x[1]:
                break

            obliczanie_przyspieszenia(faza)

            updates_appends(faza)

            if important_values == 1:
                print_important_values()

def wyświetlanie_wykresów(orbita, dane):
    if orbita == 1:
        n = -0.8 * R_Z
        plt.axis('square')
        plt.plot(x_forplot, y_forplot, color='g', label='trajektoria rakiety')
        plt.plot(x1_forplot, y1_forplot, color='r', lw=0.5, label='trajektoria osłony')
        plt.xlim(-2 * R_Z, 2 * R_Z)
        plt.ylim(-2 * R_Z, 2 * R_Z)
        theta = np.arange(0, np.pi * 2, 0.01)
        plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), lw=2, color='b', label='Ziemia')  # model ziemi
        plt.plot((R_Z + 100000) * np.cos(theta), (R_Z + 100000) * np.sin(theta), color='y', lw=0.3)
        plt.scatter(wazny_x, wazny_y)  # początak i start działania silników
        plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
        plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
        plt.text(n, 0.1 * R_Z, napis_paliwa, fontsize=10)
        plt.text(n, 0.0 * R_Z, napis_gazów, fontsize=10)
        plt.legend()
        plt.xlabel('oś X')
        plt.ylabel('oś Y')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

    if dane == 1:
        plt.subplot(411)
        plt.plot(droga_l, d_a_ly, color='r', lw=1, ls='-', label='daly ')
        plt.plot(droga_l, d_a_lx, label='dalx')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        plt.subplot(412)
        plt.plot(droga_l, a_xy_l, color='g', lw=3, ls='dotted', label='a_xy(d)')
        plt.plot(droga_l, a_x_l, color='r', lw=1, ls='-', label='a_x(d)')
        plt.plot(droga_l, a_y_l, color='y', lw=1, ls='-', label='a_y(d)')
        plt.scatter(wazny_d, wazny_a, label='d_a_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        plt.subplot(413)
        plt.plot(droga_l, v_xy_l, color='g', lw=3, ls='dotted', label='v_xy(d) [m/s]')
        plt.plot(droga_l, v_x_l, color='r', lw=1, ls='-', label='v_x(d) [m/s]')
        plt.plot(droga_l, v_y_l, color='y', lw=1, ls='-', label='v_y(d) [m/s]')
        plt.scatter(wazny_d, wazny_v, label='d_v_t')
        plt.legend()
        plt.xlabel('km')
        plt.ylabel('m/s)')

        plt.subplot(414)
        x = np.linspace(0, max(droga_l), 100)
        y = 0 * x + 100
        plt.plot(x, y, color='b', lw=1, ls='--', label='koniec atmosfery')
        plt.plot(droga_l, listH_xy, color='b', lw=1, ls='-', label='Hxy_(d) [km]')
        plt.scatter(wazny_d, wazny_h, label='d_h_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('km')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

#Oblicanie trajektorii--------------------------------------------------------------------------------------------------
t = time.time()
obliczenia_numeryczne(0, 0)          #Silniki nie zadzaiłały
print(time.time()-t)
reset_xyv()                         #resetuje wartości po I przelocie
t = time.time()
obliczenia_numeryczne(1, 0)          #I faza ruchu - do odpalenia silników
print(time.time()-t)
update_important_values(X_location, Y_location, droga, Hnpm/1000, a_xy_l[-1], v_xy_l[-1])
# a_t_x = D_osi(x_forplot[n], x_forplot[n-1]) * thrust_acceleration(x_forplot[n], x_forplot[n-1], y_forplot[n], y_forplot[n-1])
# a_t_y = D_osi(y_forplot[n], y_forplot[n-1]) * thrust_acceleration(x_forplot[n], x_forplot[n-1], y_forplot[n], y_forplot[n-1])    #stare przyśpieszenie
# m_r = m_r - Dm_1s * Dt / 1  # rocket mass update

# a_t_x = cos(X_location, Y_location) * thrust_acceleration1()
# a_t_y = -sin(X_location, Y_location) * thrust_acceleration1()
# m_r = m_r - Dm_1s * Dt / 1  # rocket mass update
t = time.time()
obliczenia_numeryczne(2, 0)          #II faza ruchu - z silnikami
print(time.time()-t)
update_important_values(X_location, Y_location, droga, Hnpm/1000, a_xy_l[-1], v_xy_l[-1])
t = time.time()
obliczenia_numeryczne(3, 0)          #III faza ruchu - po wyczerpaniu paliwa
print(time.time()-t)

#Tworzenie tekstu-------------------------------------------------------------------------------------------------------
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0/1000, 2)} ; Vy = {round(v_y0/1000, 2)}'
napis_paliwa = f'masa paliwa: {m_p}kg'
napis_gazów = f'prędkość gazów wylotowych: {v_g}m\s'
n = -0.8*R_Z

wyświetlanie_wykresów(1,1)