from Impementacja_wykresu import *
from funkcje import *
import constants

constants.v_x0 = 500
constants.v_y0 = 1000

if spin == 1:
    obliczenia_numeryczne(0, 0, wysokość=H_startu)  # Silniki nie zadzaiłały

    reset_xyv()  # resetuje wartości po I przelocie
    obliczenia_numeryczne(1, 0, wysokość=H_startu)  # I faza ruchu - do odpalenia silników

    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])
    obliczenia_numeryczne(2, 0, wysokość=H_startu)  # II faza ruchu - z silnikami
    update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])

    obliczenia_numeryczne(3, 0, wysokość=H_startu)  # III faza ruchu - po wyczerpaniu paliwa

    wyświetlanie_wykresów(1, 1, 1)  # 0 nie wyświetlam, 1 wyświetlam
if spin != 1:
    pass
