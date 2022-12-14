import numpy as np
import numpy as nu
import matplotlib.pyplot as plt


'''
x_0 = float(input())
y_0 = float(input())
R_Z = float(input())
v_x = float(input())
v_y = float(input())
V = [v_x,v_y]
kont = nu.angle(float(input()), angle = True)
'''
# V = [v_x, v_y]
# v_x = float(input("Podaj wartość składowej x-owej prędkości początkowej w metrach na sekundę"))


# -------------------------------------
M_Z = 5.98 * 10 ** 24
R_Z = 6371000
G = 6.6743 * 10 ** (-11)
V_1 = nu.sqrt(G * M_Z / R_Z)
# rocket mass
m_sl_r = 10000
# Drag coefficient for rocket
f = 0.03
# Rocket cross-section
S = np.pi * 0.5 ** 2


# air density formula
def air_density(height):
    return nu.exp(((R_Z - height) / 1000 / 9.038)) * 1.23335 - 0.0075


def drag_altitude(height, speed):
    if float(height) - R_Z <= 85000:
        return 0.5 * air_density(height) * S * speed ** 2 * f / m_sl_r
    else:
        return 0


# --------------------------------------

x_0 = 0.0
y_0 = R_Z
alpha = nu.angle(0, deg=True)
R_xy = (x_0 ** 2 + y_0 ** 2) ** 0.5
k = G * M_Z

Dt = 0.01
v_x0 = 4000
v_y0 = 3000
v_x = v_x0
v_y = v_y0
v_xy = float((v_y ** 2 + v_y ** 2) ** 0.5)
y_0 = R_Z
x_0 = 0.0
x_forplot = [x_0]
y_forplot = [y_0]
X_location = x_0
Y_location = y_0
listR_xy = [R_Z]
droga = 0
for i in range(90000):
    R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
    listR_xy.append(R_xy)
    a_x = -k * X_location * R_xy ** (-3) - drag_altitude(R_xy, v_x)
    a_y = -k * Y_location * R_xy ** (-3) - drag_altitude(R_xy, v_y)
    x_forplot.append(X_location)
    y_forplot.append(Y_location)
    v_x = v_x + a_x * Dt
    v_y = v_y + a_y * Dt
    if R_xy < R_Z:
        break
    X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2
    Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2
    droga = droga + ((x_forplot[i] - x_forplot[i - 1]) ** 2 + (y_forplot[i] - y_forplot[i - 1]) ** 2) ** 0.5
    '''if i % 4000 == 0:
        print(
            f'a_x: {round(a_x, 2)} m/s^2,  ay: {round(a_y, 2)} m/s^2,  R: {round(R_xy)} m,  t: {round(i / 3600000, 2)} h')
        print("Location (x,y):", [round(X_location, 0), round(Y_location)], "m\n")'''

#napisy
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0/1000, 2)} ; Vy = {round(v_y0/1000, 2)}'

#dodawanie wykresu
n = -0.8*R_Z
plt.plot(x_forplot, y_forplot, color='g')
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), color='b')
#plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
plt.text(n, 0.1 * R_Z, napis_drogi, fontsize=10)
plt.text(n, 0.0 * R_Z, napis_wysokości, fontsize=10)
plt.show()

