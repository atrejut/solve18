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
data = np.genfromtxt('./data/20s_Zeeman_oppos_pol.csv', delimiter=',')
field = data[0, 1:]
sel = [0, 15, -1] # 15 = np.where(field == 0)[0] for oppos
freq = data[1:, 0] - data[1:, 0].mean()
data = data[1:, 1:]


deltac = np.linspace(-40, 40, 121)
trace = []
for se in sel:
	spline = UnivariateSpline(freq, data[:, se], s=0)
	trace.append(spline(deltac))
	
sfield = field[sel]/100
trace = np.array(trace)

tic = time.time()

vvals = np.linspace(-60, 60, 241) # this is slightly coars, -40, 40, 81 is a safer option
signal = np.zeros_like(deltac)


def get_trace(A, off, wp, wc, dwp, dwc, mubb):
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



def optimise_cma(): # no additional constraints beyond pulse duration
	import cma
	def fitfun(gene):
		res = 0
		for i in range(3):
			model = get_trace(*gene[:-2], mubb=gene[-2]*sfield[i] + gene[-1])
			res += np.sum((trace[i] - model)**2)
		return res

	initval = [2., 3.9, 4., 2., 1., 2., 1., 0.]
	sigma0 = 0.5
	opts = {}
	opts['maxfevals'] = 700
	opts['tolfun'] = 1e-3
	opts['bounds'] = [[0.1, -10, 1e-5, 1e-5, 1e-5, 1e-5, 0.5, -5], [100, 10, 10, 10, 10, 10, 5, 5]]
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

signal = get_trace(A=1.3, off=4.7, wp=4.2, wc=2.4, dwp = 0.04, dwc = 2.1, mubb = 0.)
print 'analysis time per trace:', time.time()-tic, 'seconds'

res = optimise_cma()


plt.figure()
for i in range(3):
	model = get_trace(*res.best.x[:-2], mubb=res.best.x[-2]*sfield[i] + res.best.x[-1])
	plt.plot(deltac, model)
print 'plotting experimental trace with current', field[sel]
plt.plot(freq, data[:, sel], label='raw data')
plt.plot(deltac, trace, label='spline interpolation')
plt.plot(deltac, signal, label='model')
plt.legend()
plt.show()




