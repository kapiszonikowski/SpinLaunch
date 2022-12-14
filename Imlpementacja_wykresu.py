import numpy as np
import numpy as nu
import matplotlib.pyplot as plt
import os
import imageio
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



droga = 1
listR_xy = [1]
v_x0 = 1
v_y0 = 1
#dodawanie napisów do wykresu
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0/1000), 2} ; Vy = {round(v_y0/1000), 2}'


#dodawanie wykresu
theta = np.arange(0, np.pi * 2, 0.01)
plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), color='b')
plt.text(-0.2 * R_Z, 0.3 * R_Z, 'Z siłami oporu', fontsize=10)
plt.text(-0.9 * R_Z, 0.2 * R_Z, napis_prędkości, fontsize=10)
plt.text(-0.9 * R_Z, 0.1 * R_Z, napis_drogi, fontsize=10)
plt.text(-0.9 * R_Z, 0.0 * R_Z, napis_wysokości, fontsize=10)
my_path = 'C:/Users/pc/Desktop\Жизнь\Studia\SEM III\Wstęp do modelowania zjawisk fizycznych\Projekt - model spinlaunch|'
my_file = "test.jpg"
dir_name = "C:/Windows/Temp/"

plt.rcParams["savefig.directory"] = os.chdir(os.path.dirname(dir_name))



