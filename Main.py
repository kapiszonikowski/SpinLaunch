import numpy as np
import numpy as nu
import matplotlib.pyplot as plt
import tkinter as tk #biblioteka do wprowadzania danych


# -------------------------------------
M_Z = 5.98 * 10 ** 24           #masa ziemi
R_Z = 6371000                   #promień ziemi
G = 6.6743 * 10 ** (-11)        #stała grawitacyjna
V_1 = nu.sqrt(G * M_Z / R_Z)    #I prędkośćkosmiczna
k = G * M_Z
x_0 = 0.0
y_0 = R_Z
R_xy = (x_0 ** 2 + y_0 ** 2) ** 0.5
listR_xy = []
droga = 0
#alpha = nu.angle(0, deg=True)
m_sl_r = 10300          # rocket mass
f = 0.1                 # Drag coefficient for rocket
S = nu.pi * 0.5 ** 2    # Rocket cross-section
v_g = 25000          #prędkość gazów wylotowych
m_m = 10300         #masa całego modułu
m_r_p = 1000          #początkowa masa rakiety
m_p = 330          #masa paliwa
Dm_1s = m_p / 30   #paliwo tracone w czasie 1 s
m_r = m_r_p
Hnpm = R_xy - R_Z


# air density formula
def air_density(height):
    return nu.exp(((R_Z - height) / 1000 / 9.038)) * 1.23335 - 0.0075 #obliczone w originie

# drag from the height and air density
def drag_acceleration(height, speed):
    if float(height) - R_Z <= 85000:
        return 0.5 * air_density(height) * S * speed ** 2 * f / m_sl_r
    else:
        return 0

def przemieszczenie(x1, x0, y1, y0):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

def D_osi(p1, p0):
    return p1 - p0

def thrust_acceleration(x1, x0, y1, y0):
    return 1 / przemieszczenie(x1, x0, y1, y0) * (v_g * Dm_1s + 0.01 * S * air_density(R_xy)) / m_r

# ----------------------------------------------------------------------------------------------------------------------

Dt = 0.01
v_x0 = 1000
v_y0 = 1800
v_g = 7000
v_x = v_x0
v_y = v_y0
v_xy = float((v_y ** 2 + v_y ** 2) ** 0.5)
y_0 = R_Z + 32
x_0 = 0
x_forplot = [x_0]
y_forplot = [y_0]
X_location = x_0
Y_location = y_0
for i in range(500000):
    if Hnpm < 61000:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x)      #x-acceleration update
        a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y)     #y-acceleration update
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
        if i % 500 == 0:
            '''print(f'a_x: {round(a_x, 2)} m/s^2,  ay: {round(a_y, 2)} m/s^2, a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)}, v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
            print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m]; H: {round(R_xy - R_Z)}[m],  t: {round(i / 3600000, 2)}[s]\n'''
            print(R_xy, R_Z, Hnpm)

    if Hnpm >= 61000 and m_r > m_r_p - m_p:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)

        a_t_x = D_osi(x_forplot[i], x_forplot[i-1]) * thrust_acceleration(x_forplot[i], x_forplot[i-1], y_forplot[i], y_forplot[i-1])
        a_t_y = D_osi(y_forplot[i], y_forplot[i-1]) * thrust_acceleration(x_forplot[i], x_forplot[i-1], y_forplot[i], y_forplot[i-1])

        a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x) + a_t_x    #x-acceleration update
        a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y) + a_t_y    #y-acceleration update

        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update

        if R_xy < R_Z + 30000:
            print('Twoja rakieta spłonęła w atmoswerze ziemskiej')
            break
        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update

        x_forplot.append(X_location)
        y_forplot.append(Y_location)

        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
        m_r = m_r - Dm_1s * Dt                                      #rocket mass update
        Hnpm = R_xy - R_Z


        if i % 100 == 0:
            print(f'a_x: {round(a_x, 2)} m/s^2,  ay: {round(a_y, 2)} m/s^2, a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)}, v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
            print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m]; H: {round(R_xy - R_Z)}[m],  t: {round(i / 3600000, 2)}[s]')
            print(f'x thrust: {a_t_x} y thrust: {a_t_y}, D_osi_x {D_osi(x_forplot[i], x_forplot[i-1])}, D_osi_y {D_osi(y_forplot[i], y_forplot[i-1])}')
            print(R_xy, R_Z, Hnpm, m_r)
            print()

    else:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x)  # x-acceleration update
        a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y)  # y-acceleration update
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update
        if R_xy < R_Z:
            break
        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update
        x_forplot.append(X_location)
        y_forplot.append(Y_location)
        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
        Hnpm = R_xy - R_Z
        if i % 500 == 0:
            '''print(f'a_x: {round(a_x, 2)} m/s^2,  ay: {round(a_y, 2)} m/s^2, a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)}, v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
            print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m]; H: {round(R_xy - R_Z)}[m],  t: {round(i / 3600000, 2)}[s]\n'''
            print(R_xy, R_Z, Hnpm)

#napisy
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
print(max(listR_xy))
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0/1000, 2)} ; Vy = {round(v_y0/1000, 2)}'

#dodawanie wykresu
n = -0.8*R_Z
plt.axis('square')
plt.plot(x_forplot, y_forplot, color='g')
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), color='b')
plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
plt.text(n, 0.1 * R_Z, napis_drogi, fontsize=10)
plt.text(n, 0.0 * R_Z, napis_wysokości, fontsize=10)
plt.xlim(-1.5*R_Z, 1.5*R_Z)
plt.ylim(-1.5*R_Z, 1.5*R_Z)
plt.show()

