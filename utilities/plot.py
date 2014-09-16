import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import RectBivariateSpline
import os

folder = 'mm/B-scan/'

A = np.genfromtxt('../results/' + folder + '/B  0.00.txt').T

plt.figure()
plt.imshow(A)

dp = -20+0.5*np.arange(81)
dc = -50+0.5*np.arange(201)
Delta = np.linspace(-50, 40, 100)
vvals = np.linspace(-15, 15, 1000)
signal = np.zeros_like(Delta)

spline = RectBivariateSpline(dp, dc, A)

for i, D in enumerate(Delta):
	vres = spline.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
	signal[i] = np.exp(np.trapz(vres, vvals))

plt.figure()
plt.plot(Delta, signal)

plt.show()

# now here we do it for a whole scan of B-field values
files = [x for x in os.listdir('../results/' + folder) if x.endswith('.txt')]
scanres = np.zeros((100, 31))
scanres0 = np.zeros((100, 31))
for f in files:
	A = np.genfromtxt('../results/' + folder + f).T
	index = float(f[1:7]) + 15
	spline = RectBivariateSpline(dp, dc, A)
	for i, D in enumerate(Delta):
		vres = spline.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
		scanres[i, index] = np.exp(np.trapz(vres, vvals))
	offset = np.exp(np.trapz(spline.ev(vvals/780.e-3, 100-vvals/486.e-3)*np.exp(-(vvals/240.)**2), vvals))
	scanres0[:, index] = scanres[:, index]-offset
		
plt.figure()
plt.imshow(scanres, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
plt.xlabel('B-Field (G)')
plt.ylabel('Coupling Detuning (MHz)')

plt.figure()
plt.imshow(scanres0, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
plt.xlabel('B-Field (G)')
plt.ylabel('Coupling Detuning (MHz)')

plt.show()




