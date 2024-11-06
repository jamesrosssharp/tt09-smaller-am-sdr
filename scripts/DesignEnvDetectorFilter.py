from scipy import signal
from matplotlib import pyplot as plt
import numpy as np

#b, a = signal.iirfilter(1, [2000 / 500000], btype='lowpass',
#                       analog=False, ftype='butter',
#                       output='ba'
#                       )

#print(a)
#print(b)

alpha = (1024.0 - 1.0) / 1024.0

b = 1 - alpha
a = [1, -alpha]

w, h = signal.freqz(b, a, 10000, fs=50000000)

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)

ax.semilogx(w, 20 * np.log10(np.maximum(abs(h), 1e-5)))

ax.set_title('lowpass frequency response')

ax.set_xlabel('Frequency [Hz]')

ax.set_ylabel('Amplitude [dB]')

#ax.axis((10, 250000, -100, 10))

ax.grid(which='both', axis='both')

plt.show()
