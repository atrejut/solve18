import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver
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
	print sel
	freq = data[1:, 0] - data[1:, 0].mean()
	data = data[1:, 1:]

	plt.plot(freq, data[:, sel], label=filename)
plt.legend()
plt.show()
raise RuntimeError

deltac = np.linspace(-20, 20, 41)
spline = UnivariateSpline(freq, data[:, 20], s=0)
trace = spline(deltac)

tic = time.time()

vvals = np.linspace(-30, 30, 121) # this is slightly coars, -40, 40, 81 is a safer option
signal = np.zeros_like(deltac)


def get_trace(A, off, wp, wc, dwp, dwc):
	parms = {
		'fsup' : 1e-2,
		'gp' :  6.,
		'gc' : 0.05,
		'hfr' : 7.8,
		'mubb' : -0.,
		'f5p' : 0.1,
		'nv' : vvals.shape[0],
		'vs' : vvals
	}

	parms['wp'] = 1.*wp/10
	parms['wc'] = 1.*wc
	parms['dwp'] = 1.*dwp/100
	parms['dwc'] = 1.*dwc/10

	for i, D in enumerate(deltac[::-1] + off):
		res = solver.solve(delta=D, **parms).imag
		signal[i] = np.exp(np.trapz(res*np.exp(-(vvals/240.)**2), vvals))
	parms0 = parms.copy()
	parms0['wc'] = 0
	res = solver.solve(delta=0, **parms0).imag
	bg = np.exp(np.trapz(res*np.exp(-(vvals/240.)**2), vvals))
	return A*1000*(signal-bg)



def optimise_cma(): # no additional constraints beyond pulse duration
	import cma
	def fitfun(gene):
		return np.sum((trace - get_trace(*gene))**2)

	initval = [2., 3.9, 4., 2., 1., 2.]
	sigma0 = 0.5
	opts = {}
	opts['maxfevals'] = 300
	opts['tolfun'] = 1e-3
	opts['bounds'] = [[0.1, -10, 1e-5, 1e-5, 1e-5, 1e-5], [100, 10, 10, 10, 3, 3]]
	#opts['popsize'] = 22 # default is 13 for problem dimensionality 24; larger means more global search

	es = cma.CMAEvolutionStrategy(initval, sigma0, opts)
	nh = cma.NoiseHandler(es.N, [1, 1, 30])
	while not es.stop():
		X, fit_vals = es.ask_and_eval(fitfun, evaluations=nh.evaluations)
		es.tell(X, fit_vals)  # prepare for next iteration
		#es.sigma *= nh(X, fit_vals, fitfun, es.ask)  # see method __call__
		#es.countevals += nh.evaluations_just_done  # this is a hack, not important though
		es.disp()
		es.eval_mean(fitfun)
		print '========= evaluations: ', es.countevals, '========'
		print '========= current mean: ', es.fmean, '========'
		print es.mean
		print '========= current best: ', es.best.f, '========'
		print es.best.x

	print(es.stop())
	print 'mean values: ', es.result()[-2]  # take mean value, the best solution is totally off
	print 'best values: ', X[np.argmin(fit_vals)]  # not bad, but probably worse than the mean

	return es

signal = get_trace(A=2., off=3.9, wp=4., wc=2., dwp = 1., dwc = 2.)
print 'total analysis time was:', time.time()-tic, 'seconds'

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




