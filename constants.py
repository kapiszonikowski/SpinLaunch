import numpy as np
#Stałe------------------------------------------------------------------------------------------------------------------
M_Z = 5.98 * 10 ** 24           #masa ziemi
R_Z = 6371000                   #promień ziemi
G = 6.6743 * 10 ** (-11)        #stała grawitacyjna
V_1 = np.sqrt(G * M_Z / R_Z)    #I prędkośćkosmiczna
x_0 = 0                         #pocztkowy x
y_0 = R_Z + 20                  #pocztkowy y
k = G * M_Z                     #wsp staej grawitacji
Dt = 0.01                       #czas aktualizacji
#alpha = nu.angle(0, deg=True)
f = 0.125                 # Drag coefficient for rocket
S = np.pi * 0.5 ** 2    # Rocket cross-section
m_m = 10300         #masa całego modułu
v_g = 8750          #prędkość gazów wylotowych
m_r_p = 1000          #początkowa masa rakiety
jak_często = 100          #gęstość rozmieszczenia punktów - dla 100 pokazuje lokalizacje co 1s

#zmienne----------------------------------------------------------------------------------------------------------------
droga = 0                                           #zmienna drogi
v_x0 = 100                                         #prędkość początkowa y
v_y0 = 2000                                         #prędkość początkowa y
X_location = x_0                                    #zmienna położenia x
Y_location = y_0                                    #zmienna położenia y
R_xy = (X_location ** 2 + Y_location ** 2) ** 0.5   #odległość rakiety od środka ziemi
Hnpm = R_xy - R_Z                                   #wysokość npm
v_x = v_x0                                          #zmienna prędkości x
v_y = v_y0                                          #zmienna prędkości y
H_startu = 100000
i = 0                                               #ilość punktów
spin = 1
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

