import numpy as np
import numpy as nu
import matplotlib as plot
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
#V = [v_x, v_y]
#v_x = float(input("Podaj wartość składowej x-owej prędkości początkowej w metrach na sekundę"))




#-------------------------------------
M_Z = 5.98 * 10 ** 24
R_Z = 6371000
G = 6.6743 * 10 ** (-11)
#--------------------------------------

x_0 = 0.0
y_0 = R_Z
v_x = 9000
v_y = 0.0
alpha = nu.angle(0, deg=True)

R_xy = (x_0 ** 2 + y_0 ** 2) ** 0.5
k = G * M_Z

X_location = x_0
Y_location = y_0

Dt = 0.001
v_x = (k / y_0)**(1/2)
for i in range(5500000):
    R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5
    a_x = -k * X_location * R_xy ** (-3)
    a_y = -k * Y_location * R_xy ** (-3)
    v_x = v_x + a_x * Dt
    v_y = v_y + a_y * Dt
    X_location = X_location + v_x * Dt + 0.5 * a_x * Dt ** 2
    Y_location = Y_location + v_y * Dt + 0.5 * a_y * Dt ** 2
    location = [X_location, Y_location]
    if i % 40000 == 0:
        print(f'a_x: {round(a_x,2)} m/s^2,  ay: {round(a_y,2)} m/s^2,  R: {round(R_xy)} m,  t: {round(i/3600000,2)} h')
        print("Location (x,y):", [round(X_location,0), round(Y_location)], "m\n")
