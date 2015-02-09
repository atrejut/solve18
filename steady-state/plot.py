import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver_pp as solver
from scipy.interpolate import UnivariateSpline, RectBivariateSpline

# things to do:
# check the different data I have for 20s # zero-field asymmetry in peak height is most pronounced for 'sym' and least pronounced for 'same'
# implement pseudo-monte-carlo sampling (or weighting) for the fit
# try out lmfit instead of cma


# load data, and select frequency range of interest
for filename in ['./data/20s_Zeeman_same_pol.csv', './data/20s_Zeeman_oppos_pol.csv', './data/20s_Zeeman_sym.csv']:
	data = np.genfromtxt(filename, delimiter=',')
	field = data[0, 1:]
	sel = np.where(field == 0)[0]
	freq = data[1:, 0] - data[1:, 0].mean()
	data = data[1:, 1:]
	so = np.argsort(field)
	data = data[:, so]

	spline = RectBivariateSpline(freq, field[so]*17./1500, data)

	f2 = np.linspace(-20, 20, 401)
	b2 = np.linspace(-17, 17, 61)
	idata = spline(f2, b2)

	plt.figure()
	plt.imshow(idata, aspect='equal', extent=[-17, 17, -20, 20])

for t in ['pm', 'pp', 'mm', 'mp']:
	model = np.load('model_' + t + '.npy').T
	freq = np.linspace(-20, 20, 81)
	field = np.linspace(-20, 20, 81)
	spline = RectBivariateSpline(freq, field, model)
	f2 = np.linspace(-20, 20, 401)
	b2 = np.linspace(-17, 17, 61)
	idata = spline(f2, b2)
	if t.startswith('m'):
		idata = -idata

	plt.figure()
	plt.imshow(idata, aspect='equal', extent=[-17, 17, -20, 20])

plt.show()