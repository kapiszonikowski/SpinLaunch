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
x_0 = 0
k = G * M_Z
y_0 = R_Z + 20
R_xy = (x_0 ** 2 + y_0 ** 2) ** 0.5
listR_xy = []
droga = 0
#alpha = nu.angle(0, deg=True)
f = 0.1                 # Drag coefficient for rocket
S = nu.pi * 0.5 ** 2    # Rocket cross-section
v_g = 8750          #prędkość gazów wylotowych
m_m = 10300         #masa całego modułu
m_r_p = 1000          #początkowa masa rakiety
m_p = 548        #masa paliwa
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
v_xy = (v_x ** 2 + v_y ** 2) ** 0.5
wazny_x = []
wazny_y = []

v_x = v_x0
v_y = v_y0
listH_xy = []
listH_xy1 = []

X1_location = x_0
Y1_location = y_0
x1_forplot = []
y1_forplot = []

#Funkcje----------------------------------------------------------------------------------------------------------------
def air_density(height):                    # air density formula
    return nu.exp(((R_Z - height) / 1000 / 9.038)) * 1.23335 - 0.0075 #obliczone w originie

def drag_acceleration(height, speed, mr):   # drag from the height and air density
    if float(height) - R_Z <= 100000:
        return 0.5 * air_density(height) * S * speed ** 2 * f / mr
    else:
        return 0

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
v_x0 = 1000
v_y0 = 1800
n = 1                                               #Określamy jak często odpalaj się rakiety,albo wyświetlają się dane

#Oblicanie trajektorii-------------------------------------------------------------------------------------------------

                                                        #Silniki nie zadzaiłały-----------------------------------------
for i in range(500000):
        R_xy = (X1_location ** 2 + Y1_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * sin(X1_location, Y1_location) * R_xy ** (-2) - (v_x / nu.sqrt(v_x ** 2 + v_y ** 2)) * drag_acceleration(R_xy, v_x, m_m)      #x-acceleration update
        a_y = -k * cos(X1_location, Y1_location) * R_xy ** (-2) - (v_y / nu.sqrt(v_x ** 2 + v_y ** 2)) * drag_acceleration(R_xy, v_y, m_m)     #y-acceleration update
        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update
        if R_xy < R_Z:
            break
        X1_location = X1_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y1_location = Y1_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update
        x1_forplot.append(X1_location)
        y1_forplot.append(Y1_location)
        droga = droga + przemieszczenie(x1_forplot[i], x1_forplot[i - 1], y1_forplot[i], y1_forplot[i - 1])
        Hnpm = R_xy - R_Z
        listH_xy.append(Hnpm)
        #print_important_values()
        '''if i % 100 == 0:
            try:
                print(f'cos(x) = {cos(x1_forplot[i], y1_forplot[i])} || sin(x) = {sin(x1_forplot[i], y1_forplot[i])}')
                print(f'względne przemieszcanie x = {D_osi(x1_forplot[i], x1_forplot[i - 1]) / przemieszczenie(x1_forplot[i], x1_forplot[i - 1], y1_forplot[i], y1_forplot[i - 1])} || względne przemieszczenie y = {D_osi(y1_forplot[i], y1_forplot[i - 1]) / przemieszczenie(x1_forplot[i], x1_forplot[i - 1], y1_forplot[i], y1_forplot[i - 1])}\n')
            except:
                pass''' #względne przemieszenie, a warkości trygonometryczne

listH_xy.sort()
H_startu = listH_xy[-2]
print(H_startu)

listH_xy = []
droga = 0
v_x = v_x0
v_y = v_y0
v_xy_l = []
v_x_l = []
v_y_l = []
droga_l = []
a_x_l = []
a_y_l = []
a_xy_l = []
for i in range(500000):                                 #I faza ruchu - do odpalenia silników---------------------------
    if Hnpm < H_startu:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)
        a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - (
                    v_x / nu.sqrt(v_x ** 2 + v_y ** 2)) * drag_acceleration(R_xy, v_x, m_m)  # x-acceleration update
        a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - (
                    v_y / nu.sqrt(v_x ** 2 + v_y ** 2)) * drag_acceleration(R_xy, v_y, m_m)  # y-acceleration update
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

        listH_xy.append(Hnpm/1000)
        v_xy_l.append(v_xy(v_x, v_y))
        v_x_l.append(abs(v_x))
        v_y_l.append(abs(v_y))
        droga_l.append(droga)
        a_y_l.append(a_y)
        a_x_l.append(a_x)
        a_xy_l.append(a_xy(a_x, a_y))
        # print_important_values()
    else:
        break

update_important_location(X_location, Y_location)

for i in range(500000):                                 #II faza ruchu - z silnikami-----------------------------------
    if m_r > m_r_p - m_p and R_Z < R_xy:
        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        listR_xy.append(R_xy)

        '''a_t_x = D_osi(x_forplot[i], x_forplot[i-1]) * thrust_acceleration(x_forplot[i], x_forplot[i-1], y_forplot[i], y_forplot[i-1])
        a_t_y = D_osi(y_forplot[i], y_forplot[i-1]) * thrust_acceleration(x_forplot[i], x_forplot[i-1], y_forplot[i], y_forplot[i-1])'''    #stare przyśpieszenie
        a_t_x = cos(X_location, Y_location) * thrust_acceleration1()
        a_t_y = sin(X_location, Y_location) * thrust_acceleration1()

        a_x = -k * sin(X_location, Y_location) * R_xy ** (-2) - \
                (v_x / nu.sqrt(v_x ** 2 + v_y ** 2)) * drag_acceleration(R_xy, v_x, m_m) + a_t_x    #x-acceleration update
        a_y = -k * cos(X_location, Y_location) * R_xy ** (-2) - \
                (v_y / nu.sqrt(v_x ** 2 + v_y ** 2)) * drag_acceleration(R_xy, v_x, m_m) + a_t_y    #y-acceleration update
        m_r = m_r - Dm_1s * Dt                                                              # rocket mass update

        v_x = v_x + a_x * Dt                                        #x-speed update
        v_y = v_y + a_y * Dt                                        #y-speed update

        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2    #x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2    #y-location update

        x_forplot.append(X_location)
        y_forplot.append(Y_location)

        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5

        listH_xy.append(Hnpm/1000)
        v_xy_l.append(v_xy(v_x, v_y))
        v_x_l.append(abs(v_x))
        v_y_l.append(abs(v_y))
        droga_l.append(droga)
        a_y_l.append(a_y)
        a_x_l.append(a_x)
        a_xy_l.append(a_xy(a_x, a_y))
        #if i % n == 0:
            #print_important_values()
    else:
        break

update_important_location(X_location, Y_location)

for i in range(1500000):                                 #III faza ruchu - po wyczerpaniu paliwa-------------------------
    if R_xy > R_Z:
        if v_x > 0:
            a_x = -k * X_location * R_xy ** (-3) + drag_acceleration(R_xy, v_x, m_r)  # x-acceleration update
        else:
            a_x = -k * X_location * R_xy ** (-3) - drag_acceleration(R_xy, v_x, m_r)  # x-acceleration update
        if v_y > 0:
            a_y = -k * Y_location * R_xy ** (-3) + drag_acceleration(R_xy, v_x, m_r)  # x-acceleration update
        else:
            a_y = -k * Y_location * R_xy ** (-3) - drag_acceleration(R_xy, v_y, m_r)  # y-acceleration update
        v_x = v_x + a_x * Dt  # x-speed update
        v_y = v_y + a_y * Dt  # y-speed update
        X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2  # x-location update
        Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2  # y-location update

        R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
        droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
        Hnpm = R_xy - R_Z

        #if i%n == 0:
            #print_important_values()

        listR_xy.append(R_xy)
        x_forplot.append(X_location)
        y_forplot.append(Y_location)
        listH_xy.append(Hnpm / 1000)
        v_xy_l.append(v_xy(v_x, v_y))
        v_x_l.append(abs(v_x))
        v_y_l.append(abs(v_y))
        droga_l.append(droga)
        a_y_l.append(a_y)
        a_x_l.append(a_x)
        a_xy_l.append(a_xy(a_x, a_y))
    else:
        break

H_min = min(listH_xy)
print(H_min)

'''for i in x1_forplot:
    try:
        print(f'cos(x) = {cos(x1_forplot[i], y1_forplot[i])} || sin(x) = {sin(x1_forplot[i], y1_forplot[i])}')
        print(f'względne przemieszcanie x = {D_osi(x1_forplot[i], x1_forplot[i-1]) / przemieszczenie(x1_forplot[i], x1_forplot[i-1], y1_forplot[i], y1_forplot[i-1])}\
             || względne przemieszczenie y = {D_osi(y1_forplot[i], y1_forplot[i-1]) / przemieszczenie(x1_forplot[i], x1_forplot[i-1], y1_forplot[i], y1_forplot[i-1])}')
    except:
        pass''' #czemu nie działa
#Tworzenie tekstu-------------------------------------------------------------------------------------------------------
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0/1000, 2)} ; Vy = {round(v_y0/1000, 2)}'
napis_paliwa = f'masa paliwa: {m_p}kg'
napis_gazów = f'prędkość gazów wylotowych: {v_g}m\s'

#dodawanie wykresu------------------------------------------------------------------------------------------------------
n = -0.8*R_Z


plt.axis('square')
plt.plot(x_forplot, y_forplot, color='g', label='trajektoria rakiety')
plt.plot(x1_forplot, y1_forplot, color='r',lw=0.5, label='trajektoria osłony')
plt.xlim(-2*R_Z, 2*R_Z)
plt.ylim(-2*R_Z, 2*R_Z)
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta),lw=2, color='b', label='Ziemia')   #model ziemi
#plt.plot((R_Z + 76472.93978471309) * np.cos(theta), (R_Z + 76472.93978471309) * np.sin(theta), color='y')
plt.scatter(wazny_x, wazny_y)                                   # początak i start działania silników
plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
plt.text(n, 0.1 * R_Z, napis_paliwa, fontsize=10)
plt.text(n, 0.0 * R_Z, napis_gazów, fontsize=10)
plt.legend()
plt.xlabel('oś X')
plt.ylabel('oś Y')
plt.show()

plt.subplot(311)
plt.plot(droga_l, a_xy_l, color='g',lw = 3, ls='dotted',label='a_xy(d)')
plt.plot(droga_l, a_x_l, color='r',lw = 1, ls='-',label='a_x(d) [m/s^2]')
plt.plot(droga_l, a_y_l, color='y',lw = 1, ls='-',label='a_y(d) [m/s^2]')
plt.legend()
plt.xlabel('droga')
plt.ylabel('a(d)')

plt.subplot(312)
plt.plot(droga_l, v_xy_l, color='g',lw = 3, ls='dotted',label='v_xy(d) [m/s]')
plt.plot(droga_l, v_x_l, color='r',lw = 1, ls='-',label='v_x(d) [m/s]')
plt.plot(droga_l, v_y_l, color='y',lw = 1, ls='-',label='v_y(d) [m/s]')
plt.legend()
plt.xlabel('droga')
plt.ylabel('v(d)')

plt.subplot(313)
x = np.linspace(0, max(droga_l), 100)
y = 0 * x + 100
plt.plot(x, y, color='b',lw = 1, ls='--',label='koniec atmosfery' )
plt.plot(droga_l, listH_xy, color='b',lw = 1, ls='-',label='Hxy_(d) [km]')
plt.legend()
plt.xlabel('droga')
plt.ylabel('H(d)')

plt.show()

"""def f(t, freq):
    return np.sin(2 * np.pi * freq * t)
t = np.linspace(0, 1, 1000)
init_freq = 3
fig, ax = plt.subplots()
line, = ax.plot(t, f(t, init_freq))
ax.set_xlabel('Czas [s]')
ax.set_ylabel('Amplituda')
fig.subplots_adjust(bottom=0.25)
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.05])
freq_slider = Slider(
    ax=axfreq,
    label='Wysokość załączenia silników',
    valmin=R_Z + 50000,
    valmax=R_Z + 150000,
    valinit=R_Z+65000)"""

