import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import RectBivariateSpline
import os

folder = '125751-test2_mm/'
Delta = np.linspace(-50, 50, 500) # determine range of coupling laser scan
vvals = np.linspace(-15, 15, 500) # determine range (and stepsize) of velocity class integration

# read meta-data from a random meta-file
meta = {}
metafiles = [x for x in os.listdir(folder) if x.startswith('meta')]
with open(folder + metafiles[0], 'rb') as ifile:
	for line in ifile:
		key, val = line.split()
		try:
			meta[key[:-1]] = float(val)
		except ValueError:
			meta[key[:-1]] = val

dp = meta['ShiftProbe'] + meta['StepProbe']*np.arange(meta['NProbe'])
dc = meta['ShiftCoupling']+meta['StepCoupling']*np.arange(meta['NCoupling'])

signal = np.zeros_like(Delta)

# now here we do it for a whole scan of B-field values
files = [x for x in os.listdir(folder) if x.startswith('data')]
scanres = np.zeros((len(Delta), len(files)))
scanres0 = np.zeros((len(Delta), len(files)))
for i, f in enumerate(sorted(files, key = lambda x : float(x[4:]))):
	A = np.fromfile(folder + f).reshape(meta['NProbe'], meta['NCoupling'])
	index = i#int(round((float(f[4:]) + 0.8)*5))
	print f, index
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




