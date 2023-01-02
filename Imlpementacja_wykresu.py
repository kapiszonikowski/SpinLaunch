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
x_0 = 0                         #pocztkowy x
y_0 = R_Z + 20                  #pocztkowy y
k = G * M_Z                     #wsp staej grawitacji
#alpha = nu.angle(0, deg=True)
f = 0.1                 # Drag coefficient for rocket
S = nu.pi * 0.5 ** 2    # Rocket cross-section
m_m = 10300         #masa całego modułu


#zmienne----------------------------------------------------------------------------------------------------------------
droga = 0                                           #zmienna drogi
Dt = 0.01                                           #jak często zmienia się czas


#Listy------------------------------------------------------------------------------------------------------------------
v_x0 = 1000                                         #prędkość początkowa y
v_y0 = 1800                                         #prędkość początkowa y

X_location = x_0                                    #zmienna położenia x
Y_location = y_0                                    #zmienna położenia y
X1_location = x_0                                   #zmienna x gdy rakieta się nie odpali
Y1_location = y_0                                   #zmienna x gdy rakieta się nie odpali
R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5   #odległość rakiety od środka ziemi
Hnpm = R_xy - R_Z                                   #wysokość npm
v_x = v_x0                                          #zmienna prędkości x
v_y = v_y0                                          #zmienna prędkości y

x_forplot = [X_location]
y_forplot = [Y_location]
x1_forplot = [X_location]
y1_forplot = [Y_location]
listR_xy = [R_xy]       #potrzebne? -> TAK
listH_xy = []
listH_xy1 = []
wazny_x = []
wazny_y = []
wazny_d = []
wazny_a = []
wazny_v = []
wazny_h = []
v_xy_l = []
v_x_l = []
v_y_l = []
droga_l = []
a_x_l = []
a_y_l = []
a_xy_l = []
d_a_lx = []
d_a_ly = []

#Funkcje----------------------------------------------------------------------------------------------------------------
def prędkość_kosmiczna(R):
    return nu.sqrt(G * M_Z / R)

def air_density(R_xy):                    # air density formula
    if R_xy < R_Z + 100000:
        return 2.718281828 ** (((R_Z - R_xy) / 1000 / 9.038)) * 1.23335
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

def update_important_location(x, y):
    wazny_x.append(x)
    wazny_y.append(y)

def v_xy(vx, vy):
    return (vx ** 2 + vy ** 2) ** 0.5

def a_xy(ax, ay):
    return (ax ** 2 + ay ** 2) ** 0.5

def print_important_values():
    try:
        print(f'a_x: {round(a_x, 2)} m/s^2 ||  ay: {round(a_y, 2)} m/s^2 || a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)} || v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
        print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m] || H: {round(R_xy - R_Z)}[m] ||  t: {round(i / 3600000, 2)}[s] || m_r: {m_r : .8}\n')
    except:
        print(f'a_x: {round(a_x, 2)} m/s^2 ||  ay: {round(a_y, 2)} m/s^2 || a_xy = {round((a_x ** 2 + a_y ** 2) ** 0.5, 2)} || v_xy = {round((v_x ** 2 + v_y ** 2) ** 0.5, 2)}')
        print(f'Location (x,y): {[round(X_location, 0), round(Y_location)]}[m] || H: {round(R_xy - R_Z)}[m] ||  t: {round(i / 3600000, 2)}[s]')

#Wpisujemy dane wejściowe-----------------------------------------------------------------------------------------------

v_g = 8750          #prędkość gazów wylotowych
m_r_p = 1000          #początkowa masa rakiety
m_p = 600        #masa paliwa
Dm_1s = m_p / 150   #paliwo tracone w czasie 1 s
m_r = m_r_p                                         #zmienna masa rakiety

w = 800000              #ilość odtworzeń w III fazie ruchu
n = 0                   #ilość iteracji
#Oblicanie trajektorii-------------------------------------------------------------------------------------------------

                                                        #Silniki nie zadzaiłały-----------------------------------------

for i in range(500000):
    if R_xy > R_Z:
        if v_x > 0:
            a_x = -k * sin(X1_location, Y1_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            #d_a_lx.append(-drag_acceleration(R_xy, v_x, m_m))
        else:
            a_x = -k * sin(X1_location, Y1_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_x,
                                                                                      m_m)  # x-acceleration update
            #d_a_lx.append(drag_acceleration(R_xy, v_x, m_m))
        if v_y > 0:
            a_y = -k * cos(X1_location, Y1_location) * R_xy ** (-2) - drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # x-acceleration update
            #d_a_ly.append(-drag_acceleration(R_xy, v_y, m_m))
        else:
            a_y = -k * cos(X1_location, Y1_location) * R_xy ** (-2) + drag_acceleration(R_xy, v_y,
                                                                                      m_m)  # y-acceleration update
            #d_a_ly.append(drag_acceleration(R_xy, v_y, m_m))

        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update

        X1_location = X1_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y1_location = Y1_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update

        x1_forplot.append(X1_location)
        y1_forplot.append(Y1_location)

        Hnpm = R_xy - R_Z
        R_xy = (X1_location ** 2 + Y1_location ** 2) ** 0.5
        listH_xy1.append(Hnpm)

        if listH_xy1[i] - listH_xy1[i-1] < 0:
            a = i
        if round(listH_xy1[i],-1) == 100000 and listH_xy1[i] - listH_xy1[i-1] < 0:
            b = i
            #print(v_x, v_y)
        #print_important_values()
    else:
        break
#print(a, b)
listH_xy1.sort()
H_startu = listH_xy1[-2]
print(H_startu)

n = -0.8*R_Z
plt.axis('square')
#plt.plot(x_forplot, y_forplot, color='g', label='trajektoria rakiety')
plt.plot(x1_forplot, y1_forplot, color='r',lw=0.5, label='trajektoria osłony')
plt.xlim(-2*R_Z, 2*R_Z)
plt.ylim(-2*R_Z, 2*R_Z)
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta),lw=2, color='b', label='Ziemia')   #model ziemi
plt.plot((R_Z + 100000) * np.cos(theta), (R_Z + 100000) * np.sin(theta), color='y', lw=0.3)
#plt.scatter(wazny_x, wazny_y)                                   # początak i start działania silników
#plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
#plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
#plt.text(n, 0.1 * R_Z, napis_paliwa, fontsize=10)
#plt.text(n, 0.0 * R_Z, napis_gazów, fontsize=10)
plt.legend()
plt.xlabel('oś X')
plt.ylabel('oś Y')
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.margins(0.05)
#plt.show()

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)


t1 = np.arange(0.0, 3.0, 0.01)

ax1 = plt.subplot(212)
ax1.margins(0.05)           # Default margin is 0.05, value 0 means fit
ax1.plot(t1, f(t1))

ax2 = plt.subplot(221)
ax2.margins(2, 2)           # Values >0.0 zoom out
ax2.plot(t1, f(t1))
ax2.set_title('Zoomed out')

ax3 = plt.subplot(222)
ax3.margins(x=0, y=-0.25)   # Values in (-0.5, 0.0) zooms in to center
ax3.plot(t1, f(t1))
ax3.set_title('Zoomed in')

plt.show()





