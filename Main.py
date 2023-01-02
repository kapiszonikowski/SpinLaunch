import time
from funkcje import *
from Impementacja_wykresu import *

t = time.time()
obliczenia_numeryczne(0, 0)  # Silniki nie zadzaiłały
print(time.time() - t)
reset_xyv()  # resetuje wartości po I przelocie
t = time.time()

obliczenia_numeryczne(1, 0)  # I faza ruchu - do odpalenia silników
print(time.time() - t)
update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])
t = time.time()

obliczenia_numeryczne(2, 0)  # II faza ruchu - z silnikami
print(time.time() - t)
update_important_values(x_forplot[-1], y_forplot[-1], droga_l[-1], listH_xy[-1], a_xy_l[-1], v_xy_l[-1])
t = time.time()

obliczenia_numeryczne(3, 0)  # III faza ruchu - po wyczerpaniu paliwa
print(time.time() - t)

print_important_values()

wyświetlanie_wykresów(1, 1)         #0 nie wyświetlam, 1 wyświetlam