from Impementacja_wykresu import *
from funkcje import *
import constants as con


v_x0 = 0
v_y0 = 0
if spin == 1:
    obliczenia_numeryczne(0, 1, wysokość=H_startu)  # Silniki nie zadzaiłały

    reset_xyv()  # resetuje wartości po I przelocie
    obliczenia_numeryczne(1, 1, wysokość=H_startu)  # I faza ruchu - do odpalenia silników

    if con.listH_xy[-1] > 0:
        update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])
    obliczenia_numeryczne(2, 1, wysokość=H_startu)  # II faza ruchu - z silnikami
    if test == 1:
        update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])

    obliczenia_numeryczne(3, 1, wysokość=H_startu)  # III faza ruchu - po wyczerpaniu paliwa

    wyświetlanie_wykresów(1, 1, 1)  # 0 nie wyświetlam, 1 wyświetlam
if spin != 1:
    pass
