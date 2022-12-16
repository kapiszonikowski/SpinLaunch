import numpy as np
import numpy as nu
import matplotlib.pyplot as plt
import tkinter as tk #biblioteka do wprowadzania danych
from matplotlib.widgets import Slider

#Stałe------------------------------------------------------------------------------------------------------------------
M_Z = 5.98 * 10 ** 24           #masa ziemi
R_Z = 6371000                   #promień ziemi
G = 6.6743 * 10 ** (-11)        #stała grawitacyjna
V_1 = nu.sqrt(G * M_Z / R_Z)    #I prędkośćkosmiczna
k = G * M_Z
x_0 = 0
y_0 = R_Z + 20
R_xy = (x_0 ** 2 + y_0 ** 2) ** 0.5
listR_xy = []
droga = 0
#alpha = nu.angle(0, deg=True)
f = 0.1                 # Drag coefficient for rocket
S = nu.pi * 0.5 ** 2    # Rocket cross-section
v_g = 30000          #prędkość gazów wylotowych
m_m = 10300         #masa całego modułu
m_r_p = 1000          #początkowa masa rakiety
m_p = 330          #masa paliwa
Dm_1s = m_p / 150   #paliwo tracone w czasie 1 s
m_r = m_r_p
Hnpm = R_xy - R_Z
release_height = 158824
x_forplot = [x_0]
y_forplot = [y_0]
X_location = x_0
Y_location = y_0

Dt = 0.01
v_x0 = 1000
v_y0 = 1800
v_x = v_x0
v_y = v_y0
v_xy = (v_y ** 2 + v_y ** 2) ** 0.5
wazny_x = []
wazny_y = []

#Funkcje----------------------------------------------------------------------------------------------------------------
def air_density(height):                    # air density formula
    return nu.exp(((R_Z - height) / 1000 / 9.038)) * 1.23335 - 0.0075 #obliczone w originie

def drag_acceleration(height, speed, mr):   # drag from the height and air density
    if float(height) - R_Z <= 85000:
        return 0.5 * air_density(height) * S * speed ** 2 * f / mr
    else:
        return 0

def przemieszczenie(x1, x0, y1, y0):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def D_osi(p1, p0):
    return p1 - p0

def thrust_acceleration(x1, x0, y1, y0):
    return 1 / przemieszczenie(x1, x0, y1, y0) * (v_g * Dm_1s + 0.01 * S * 10 * air_density(R_xy)) / m_r

def update_important_location(x, y):
    wazny_x.append(x)
    wazny_y.append(y)

def print_important_values():
    print(f'a_x: {round(a_x, 2)} m/s^2,  ay: {round(a_y, 2)} m/s^2, a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)}, v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
    print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m]; H: {round(R_xy - R_Z)}[m],  t: {round(i / 3600000, 2)}[s]')
    try:
        print(f'x thrust: {a_t_x} y thrust: {a_t_y}, D_osi_x {D_osi(x_forplot[i], x_forplot[i-1])}, D_osi_y {D_osi(y_forplot[i], y_forplot[i-1])}')
    except:
        pass
    print(R_xy, R_Z, Hnpm, m_r)
    print(wazny_x, wazny_y)



#Wpisujemy dane wejściowe-----------------------------------------------------------------------------------------------
v_x0 = 1000
v_y0 = 1800

n = 100                                                 #Określamy jak często wyświetlają się dane

#Oblicanie trajektorii-------------------------------------------------------------------------------------------------
v_x = v_x0
v_y = v_y0
for i in range(500000):                                 #I faza ruchu - do odpalenia silnikami
    if Hnpm < release_height:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x, m_m)      #x-acceleration update
        a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y, m_m)     #y-acceleration update
        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update
        if R_xy < R_Z:
            break
        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update
        x_forplot.append(X_location)
        y_forplot.append(Y_location)
        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
        Hnpm = R_xy - R_Z
        ddif = droga
        #if i % n == 0:
            #print_important_values()
    else:
        break
update_important_location(X_location, Y_location)
for i in range(500000):                                 #II faza ruchu - z silnikami
    if Hnpm >= release_height and m_r > m_r_p - m_p:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)

        a_t_x = D_osi(x_forplot[i], x_forplot[i-1]) * thrust_acceleration(x_forplot[i], x_forplot[i-1], y_forplot[i], y_forplot[i-1])
        a_t_y = D_osi(y_forplot[i], y_forplot[i-1]) * thrust_acceleration(x_forplot[i], x_forplot[i-1], y_forplot[i], y_forplot[i-1])

        a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x, m_r) + a_t_x    #x-acceleration update
        a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y, m_r) + a_t_y    #y-acceleration update

        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update

        x_forplot.append(X_location)
        y_forplot.append(Y_location)

        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
        m_r = m_r - Dm_1s * Dt                                      #rocket mass update
        Hnpm = R_xy - R_Z
        #if i % n == 0:
            #print_important_values()
    else:
        break
update_important_location(X_location, Y_location)
for i in range(500000):                                 #III faza ruchu - po wyczerpaniu paliwa
    if R_xy >= R_Z:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x, m_r)  # x-acceleration update
        a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y, m_r)  # y-acceleration update
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update
        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update
        x_forplot.append(X_location)
        y_forplot.append(Y_location)
        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
        Hnpm = R_xy - R_Z
        #if i % n == 0:
            #print_important_values()
    else:
        break
X1_location = x_0
Y1_location = y_0
x1_forplot = []
y1_forplot = []
v_x = v_x0
v_y = v_y0
for i in range(500000):                                 #I faza ruchu - do odpalenia silnikami
        R_xy = (X1_location ** 2 + Y1_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * X1_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x, m_m)      #x-acceleration update
        a_y = -k * Y1_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y, m_m)     #y-acceleration update
        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update
        if R_xy < R_Z:
            break
        X1_location = X1_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y1_location = Y1_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update
        x1_forplot.append(X1_location)
        y1_forplot.append(Y1_location)
        droga = droga + ((x1_forplot[i] - x1_forplot[i - 1]) ** 2 + (y1_forplot[i] - y1_forplot[i - 1]) ** 2) ** 0.5
        Hnpm = R_xy - R_Z
        ddif = droga
        #print_important_values()

#Tworzenie tekstu-------------------------------------------------------------------------------------------------------
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0/1000, 2)} ; Vy = {round(v_y0/1000, 2)}'

#dodawanie wykresu------------------------------------------------------------------------------------------------------
n = -0.8*R_Z
plt.axis('square')
plt.plot(x_forplot, y_forplot, color='g')
plt.plot(x1_forplot, y1_forplot, color='r')
plt.xlim(-1.5*R_Z, 1.5*R_Z)
plt.ylim(-1.5*R_Z, 1.5*R_Z)
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), color='b')   #model ziemi
plt.scatter(wazny_x, wazny_y)                                   # początak i start działania silników
#dodawanie tekstu
plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
plt.text(n, 0.1 * R_Z, napis_drogi, fontsize=10)
plt.text(n, 0.0 * R_Z, napis_wysokości, fontsize=10)
plt.show()

