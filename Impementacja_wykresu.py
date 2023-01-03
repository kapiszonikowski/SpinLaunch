from constants import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Slider

# Tworzenie tekstu-------------------------------------------------------------------------------------------------------
nd = round((droga / 1000), 2)
nw = round((max(listR_xy) - R_Z) / 1000, 2)
napis_drogi = f'droga przebyta przez ciao: {nd}km'
napis_wysokości = f'maksymalna wysokość ciała n.p.k: {nw}km'
napis_prędkości = f'początkowe prędkości ciał [km/s]: Vx = {round(v_x0 / 1000, 2)} ; Vy = {round(v_y0 / 1000, 2)}'
napis_paliwa = f'masa paliwa: {m_p}kg'
napis_gazów = f'prędkość gazów wylotowych: {v_g}m\s'
n = -0.8 * R_Z

def wyświetlanie_wykresów(orbita, dane, spin):
    if orbita == 1:
        # ax, ax1 = plt.subplots()
        n = -0.8 * R_Z
        plt.axis('square')
        plt.plot(x_forplot, y_forplot, color='g', label='trajektoria rakiety')
        if spin == 1:
            plt.plot(x1_forplot, y1_forplot, color='r', lw=0.5, label='trajektoria osłony')
        else:
            pass
        plt.xlim(-2 * R_Z, 2 * R_Z)
        plt.ylim(-2 * R_Z, 2 * R_Z)
        theta = np.arange(0, np.pi * 2, 0.01)
        plt.plot(R_Z * np.cos(theta), R_Z * np.sin(theta), lw=2, color='b', label='Ziemia')  # model ziemi
        plt.plot((R_Z + 85000) * np.cos(theta), (R_Z + 85000) * np.sin(theta), color='y', lw=0.3)
        plt.scatter(wazny_x, wazny_y)  # początak i start działania silników
        plt.text(-0.2 * R_Z, 0.3 * R_Z, 'z tarciem', fontsize=10)
        plt.text(n, 0.2 * R_Z, napis_prędkości, fontsize=10)
        plt.text(n, 0.1 * R_Z, napis_paliwa, fontsize=10)
        plt.text(n, 0.0 * R_Z, napis_gazów, fontsize=10)
        plt.legend()
        plt.xlabel('oś X')
        plt.ylabel('oś Y')

        ax = plt.subplot()
        cursor = Cursor(ax, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        '''ax.subplots_adjust(bottom=0.25)
        axslider = ax.add_axes([0.1, 0.1, 0.6, 0.05])
        slider = Slider(ax=axslider, label="Time", valmin=0, valmax=i-1, valstep=1)

        def update(indx):
            ax1.scatter(x_forplot[indx], y_forplot[indx], color='Black')

        ax.canvas.draw_idle()
        slider.on_changed(update)'''

        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

    if dane == 1:
        while len(droga_l) - len(d_a_ly) != 0:
            if len(droga_l) - len(d_a_ly) < 0:
                d_a_ly.remove(d_a_ly[0])
                d_a_lx.remove(d_a_lx[0])
            if len(droga_l) - len(d_a_ly) > 0:
                droga_l.remove(droga_l[0])

            while len(droga_l) - len(a_xy_l) != 0:
                if len(droga_l) - len(a_xy_l) < 0:
                    a_xy_l.remove(a_xy_l[0])
                    a_y_l.remove(a_y_l[0])
                    a_x_l.remove(a_x_l[0])
                    v_x_l.remove(v_x_l[0])
                    v_xy_l.remove(v_xy_l[0])
                    v_y_l.remove(v_y_l[0])
                    listH_xy.remove(listH_xy[0])
                if len(droga_l) - len(a_xy_l) > 0:
                    droga_l.remove(droga_l[0])
        plt.subplot(411)
        plt.plot(droga_l, d_a_ly, color='r', lw=1, ls='-', label='daly ')
        plt.plot(droga_l, d_a_lx, label='dalx')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        aa = plt.subplot(411)
        cursor1 = Cursor(aa, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(412)
        plt.plot(droga_l, a_xy_l, color='g', lw=3, ls='dotted', label='a_xy(d)')
        plt.plot(droga_l, a_x_l, color='r', lw=1, ls='-', label='a_x(d)')
        plt.plot(droga_l, a_y_l, color='y', lw=1, ls='-', label='a_y(d)')
        plt.scatter(wazny_d, wazny_a, label='d_a_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('m/s^2')

        ab = plt.subplot(412)
        cursor2 = Cursor(ab, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(413)
        plt.plot(droga_l, v_xy_l, color='g', lw=3, ls='dotted', label='v_xy(d) [m/s]')
        plt.plot(droga_l, v_x_l, color='r', lw=1, ls='-', label='v_x(d) [m/s]')
        plt.plot(droga_l, v_y_l, color='y', lw=1, ls='-', label='v_y(d) [m/s]')
        plt.scatter(wazny_d, wazny_v, label='d_v_t')
        plt.legend()
        plt.xlabel('km')
        plt.ylabel('m/s)')

        ac = plt.subplot(413)
        cursor3 = Cursor(ac, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        plt.subplot(414)
        x = np.linspace(0, max(droga_l), 100)
        y = 0 * x + 85
        plt.plot(x, y, color='b', lw=1, ls='--', label='koniec atmosfery')
        plt.plot(droga_l, listH_xy, color='b', lw=1, ls='-', label='Hxy_(d) [km]')
        plt.scatter(wazny_d, wazny_h, label='d_h_t')
        plt.legend()
        plt.xlabel('m')
        plt.ylabel('km')

        ad = plt.subplot(414)
        cursor4 = Cursor(ad, horizOn=True, vertOn=True, linewidth=0.5, color='Black')

        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()