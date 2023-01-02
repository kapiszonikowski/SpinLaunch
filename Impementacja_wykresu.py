import matplotlib.pyplot as plt
from constants import *

# Tworzenie tekstu-------------------------------------------------------------------------------------------------------
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0 / 1000, 2)} ; Vy = {round(v_y0 / 1000, 2)}'
napis_paliwa = f'masa paliwa: {m_p}kg'
napis_gazów = f'prędkość gazów wylotowych: {v_g}m\s'
n = -0.8 * R_Z
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