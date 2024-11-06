from scipy import signal
from matplotlib import pyplot as plt
import numpy as np
import cmath
import math

#b, a = signal.iirfilter(1, [450000.0 / 25000000.0, 460000.0 / 25000000.0], btype='bandpass',
#                       analog=False, ftype='butter',
#                       output='ba'
#                       )

r = 0.995
w0 = 0.057

a = np.array([ 1, -2.0*r*math.cos(w0),  r*r ])
b = np.array([ 0.005    , 0  ,  -0.005])



scale_val = 8192.0

print(a)
print(b)

a = np.floor(a*scale_val)
b = np.floor(b*scale_val)

print(a)
print(b)


#[ 1.         -1.99893158  0.9997487 ]
#[ 0.00012565  0.         -0.00012565]


#[ 1.         -1.93116778  0.98751193]
#[ 0.00624404  0.         -0.00624404]

#a = [ 512.0, -988,  505 ]
#b = [ 3    , 0  ,  -3]

#a = [65536, -130776, 65454]
#b = [41,     0,    -41]


a = np.array(a) / scale_val
b = np.array(b) / scale_val


#alpha = (512.0 - 5.0) / 512.0

#b = 1 - alpha
#a = [1, -alpha]

w, h = signal.freqz(b, a, fs=50000000)

#print(w)

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)

ax.semilogx(w, 20 * np.log10(np.maximum(abs(h), 1e-5)))

ax.set_title('19kHz bandpass frequency response')

ax.set_xlabel('Frequency [Hz]')

ax.set_ylabel('Amplitude [dB]')

#ax.axis((10, 250000, -100, 10))

ax.grid(which='both', axis='both')

plt.show()

# Plot poles and zeros

z, p, k = signal.tf2zpk(b, a)

print(z)
print(p)
print(k)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

z1r,z1t = cmath.polar(z[0])
z2r,z2t = cmath.polar(z[1])

p1r,p1t = cmath.polar(p[0])
p2r,p2t = cmath.polar(p[1])

ax.plot(z1t, z1r, 'ko')
ax.plot(z2t, z2r, 'ko')
ax.plot(p1t, p1r, 'kx')
ax.plot(p2t, p2r, 'kx')

ax.set_rmax(1.1)
ax.set_rticks([0.5, 1])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()

