import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver_pp as solver
from scipy.interpolate import UnivariateSpline

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
	data2 = data[:, so]

	plt.figure()
	plt.imshow(data2, aspect='auto')

deltac = np.linspace(-20, 20, 81)
spline = UnivariateSpline(freq, data[:, 20], s=0)
trace = spline(deltac)

tic = time.time()

vvals = np.linspace(-60, 60, 121) # this is slightly coars, -40, 40, 81 is a safer option

def get_trace(A, off, wp, wc, dwp, dwc, mubb):
	signal = np.zeros_like(deltac)
	parms = {
		'fsup' : 1e-2,
		'gp' :  6.,
		'gc' : 0.05,
		'hfr' : 7.8,
		'f5p' : 0.1,
		'nv' : vvals.shape[0],
		'vs' : vvals
	}

	parms['wp'] = 1.*wp/10
	parms['wc'] = 1.*wc
	parms['dwp'] = 1.*dwp/100
	parms['dwc'] = 1.*dwc/10
	parms['mubb'] = 1.*mubb

	for i, D in enumerate(deltac[::-1] + off):
		res = solver.solve(delta=D, **parms).imag
		signal[i] = np.exp(np.trapz(res*np.exp(-(vvals/240.)**2), vvals))
	parms0 = parms.copy()
	parms0['wc'] = 0
	res = solver.solve(delta=0, **parms0).imag
	bg = np.exp(np.trapz(res*np.exp(-(vvals/240.)**2), vvals))
	return A*1000*(signal-bg)



model=[]
plt.figure()
for b in field:
	print b
	s = get_trace(A=0.98, off=3.98, wp=3.86, wc=2.38, dwp = 1.14, dwc = 3.21, mubb=1.1286*b-0.592)
	plt.plot(s)
	model.append(s)
print 'total analysis time was:', time.time()-tic, 'seconds'
model = np.array(model)
np.save('model_pp.npy', model)

plt.figure()
plt.imshow(model)
plt.show()
raise RuntimeError

res = optimise_cma()

#raise RuntimeError

plt.figure()
sel = 20
signal = get_trace(*res.result()[-2])
print 'plotting experimental trace with current', field[sel]
plt.plot(freq, data[:, sel], label='raw data')
plt.plot(deltac, trace, label='spline interpolation')
plt.plot(deltac, signal, label='model')
plt.legend()
plt.show()




