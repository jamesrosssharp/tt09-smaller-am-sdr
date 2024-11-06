
import numpy as np
import scipy.signal
from matplotlib import pyplot as plt

a = np.array([  8192., -16276.,   8110.])
b = np.array([ 5.,   0., -5.])

data = np.random.normal(0, 1, 4096)

# Compute using mults, adds and shifts
#datout = scipy.signal.lfilter(b, a, data)

datout = np.zeros(4096)
y0 = 0
y1 = 0
y2 = 0
x0 = 0
x1 = 0
x2 = 0

for i in range(0, len(data)):
    
    y2 = y1
    y1 = y0
    x2 = x1
    x1 = x0
    x0 = int(data[i]*256)

    y0 = int(-a[1]*y1 - a[2]*y2 + b[0]*x0 + b[2]*x2) >> 13
    datout[i] = y0

    print("{} {} {} {} {} y0 = {}", x0, x1, x2, y1, y2, y0)


fft_dat = scipy.fft.fft(datout)

plt.plot(datout)
plt.show()

plt.plot(np.linspace(0, 50000000, 4096), np.abs(fft_dat))
plt.show()


