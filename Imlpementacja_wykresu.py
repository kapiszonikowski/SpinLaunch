from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import numpy as np


def f(t, freq):
    return np.sin(2 * np.pi * freq * t)


t = np.linspace(0, 1, 1000)
init_freq = 3
fig, ax = plt.subplots()
line, = ax.plot(t, f(t, init_freq))
ax.set_xlabel('Czas [s]')
ax.set_ylabel('Amplituda')
fig.subplots_adjust(bottom=0.8, top=1)
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.05])

freq_slider = Slider(
    ax=axfreq,
    label='Frequency [Hz]',
    valmin=0.1,
    valmax=30,
    valinit=init_freq)


def update(val):
    line.set_ydata(f(t, freq_slider.val))
    fig.canvas.draw_idle()


freq_slider.on_changed(update)
plt.show()
