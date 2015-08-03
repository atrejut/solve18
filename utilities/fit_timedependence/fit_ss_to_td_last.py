from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver_pp as solver
from scipy.interpolate import RectBivariateSpline, UnivariateSpline
import lmfit

# things to do:
# check the different data I have for 20s # zero-field asymmetry in peak height is most pronounced for 'sym' and least pronounced for 'same'
# implement pseudo-monte-carlo sampling (or weighting) for the fit
# try out lmfit instead of cma


# load data, and select frequency range of interest
arr = np.load('lastTrace_raw.npy')
freq = arr[0, :]
data = arr[1, :]


deltac = np.linspace(-30, 30, 121)

spline = UnivariateSpline(freq, data, s=0)
trace = spline(deltac)

sfield = [0]
trace = np.array(trace)

tic = time.time()

vvals = np.linspace(-60, 60, 961) # this is slightly coars, -80, 80, 321 is a safer option
signal = np.zeros_like(deltac)


def get_trace(wp, wc, dwp, dwc, offs, mubb, fsup, f5p):
	parms = {
	'fsup' : 1.*fsup/100,
	'gp' :  6.,
	'gc' : 0.05,
	'hfr' : 8.,
	'f5p' : 1.*f5p,
	}

	parms['wp'] = 1.*wp/100
	parms['wc'] = 	1.*wc
	parms['dwp'] = 1.*dwp/100
	parms['dwc'] = 1.*dwc/100
	parms['mubb'] = 1.*mubb

	# dp = -20. + 0.25*np.arange(41)
	# dc = -50 + 0.25*np.arange(101)	
	dp = np.linspace(-30, 30, 31)
	dc = np.linspace(-50, 50, 101)

	parms['dps'] = dp
	parms['dcs'] = dc
	parms['ndp'] = dp.shape[0]
	parms['ndc'] = dc.shape[0]

	print wp, wc, dwp, dwc, offs, fsup

	res = solver.solve(**parms).imag
	spline = RectBivariateSpline(dp, dc, res)
	signal = np.zeros_like(deltac)
	for i, D in enumerate(deltac[::-1] + offs):
		vres = spline.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
		signal[i] = np.exp(np.trapz(vres, vvals))

	# parms0 = parms.copy()
	# parms0['wc'] = 0
	# res = solver.solve(delta=0, **parms0).imag
	# bg = np.exp(np.trapz(res*np.exp(-(vvals/240.)**2), vvals))
	#return A*1000*(signal-bg)
	return signal, res



def optimise_cma(): # no additional constraints beyond pulse duration
	import cma
	def fitfun(gene):
		res = 0
		model = get_trace(*gene, mubb=0)
		res += np.sum((trace - model)**2)
		return res

	initval = [ 5.8789797,  4.10093183,  0.54848955,  2.674647,   5.14141705]
	sigma0 = 0.1
	opts = {}
	opts['maxfevals'] = 700
	opts['tolfun'] = 1e-3
	opts['bounds'] = [[0.5, 1, 1e-5, 1e-5, 4], [0.7, 10, 10, 10, 6]]
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

def optimise_lmfit():
	def fitfun(parms):
		model = get_trace(**parms.valuesdict())
		return (trace - model)

	p = lmfit.Parameters()
	#4.93277292753, 5.00357623233, 1.00457897445e-05, 30.3002204416, 5.05735846866,
	p.add('wp', 4.93, min=3, max=7)
	p.add('wc', 5., min=1e-5, max=10)
	p.add('dwp', 1.e-5, min=1e-5, max=10)
	p.add('dwc', 30., min=1e-5, max=100)
	p.add('offs', 5.06, min=4, max=6)
	p.add('mubb', 0, False)
	p.add('fsup', 1, min=0, max=100)
	p.add('f5p', 0.1, False)
	return lmfit.minimize(fitfun, p), p




best_fit = {'wp': 4.9338138774032156, 'wc': 5.0044175275612917, 'dwp': 1.0000570118937041e-05, 'dwc': 30.348260804646358, 'offs': 5.0573762984836677, 'mubb': 0, 'fsup': 0.96205485833260052, 'f5p': 0.1}
like_td_model = {'wp' : 50., 'wc' : 2.5, 'dwp' : 1., 'dwc' : 10., 'offs' : 5., 'mubb' : 0., 'fsup' : 1., 'f5p' : 0.1}
signal, res = get_trace (**like_td_model)
print 'analysis time per trace:', time.time()-tic, 'seconds'
plt.plot(deltac, signal, 'rx-', label='ss signal')
plt.plot(deltac, trace, 'bo', label='td signal')
plt.legend()
plt.show()
data = np.zeros((2, signal.shape[0]))
data[0, :] = deltac
data[1, :] = signal
np.save('same_ss_solution.np', data)

raise RuntimeError


res, parms = optimise_lmfit()
raise RuntimeError

# res = []
# for x in np.logspace(-1, 1, 20):
# 	res.append(get_trace(wp=x, wc=2.4, dwp = 0.04, dwc = 2.1, mubb = 0.)[0])
# plt.plot(res)
# plt.show()



res = optimise_cma()
print res

plt.figure()
for i in range(3):
	model = get_trace(*res.best.x, mubb=res.best.x[-2]*sfield[i] + res.best.x[-1])
	plt.plot(deltac, model)
	print 'plotting experimental trace with current', field[sel]
	plt.plot(freq, data[:, sel], label='raw data')
	plt.plot(deltac, trace, label='spline interpolation')
	plt.plot(deltac, signal, label='model')
	plt.legend()
	plt.show()




