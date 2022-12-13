import numpy as np
import numpy as nu
import matplotlib.pyplot as plt
import time

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
    return np.exp((R_Z - float(height)) / 9.038) * 1.23335 - 0.0075


def drag_force(height, speed):
    if float(height) - R_Z <= 85000:
        return float(0.5 * air_density(height) * S * speed ** 2 * f)
    else:
        return float(0)


# --------------------------------------

x_0 = 0.0
y_0 = R_Z
alpha = nu.angle(0, deg=True)
R_xy = (x_0 ** 2 + y_0 ** 2) ** 0.5
k = G * M_Z

Dt = 0.01
v_x = 0.0
v_y = 7900.0
v_xy = float((v_y ** 2 + v_y ** 2) ** 0.5)
y_0 = R_Z
x_0 = 0.0
x_forplot = [x_0]
y_forplot = [y_0]
X_location = x_0
Y_location = y_0
listR_xy = [R_Z]
for i in range(500000):
    R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
    listR_xy.append(R_xy)
    a_x = -k * X_location * R_xy ** (-3) - drag_force(R_xy, v_x)
    a_y = -k * Y_location * R_xy ** (-3) - drag_force(R_xy, v_y)
    if i % 1 == 0:
        x_forplot.append(X_location)
        y_forplot.append(Y_location)
    v_x = v_x + a_x * Dt
    v_y = v_y + a_y * Dt
    if R_xy < R_Z:
        break
    X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2
    Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2
    location = [X_location, Y_location]
    '''if i % 4000 == 0:
        print(
            f'a_x: {round(a_x, 2)} m/s^2,  ay: {round(a_y, 2)} m/s^2,  R: {round(R_xy)} m,  t: {round(i / 3600000, 2)} h')
        print("Location (x,y):", [round(X_location, 0), round(Y_location)], "m\n")'''


plt.plot(x_forplot, y_forplot, color='g')
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), color='b')
plt.show()
