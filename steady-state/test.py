import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver
from scipy.interpolate import RectBivariateSpline

tic = time.time()

dp = -20+0.5*np.arange(81)
dc = -50+0.5*np.arange(201)
Delta = np.linspace(-50, 50, 101)
vvals = np.linspace(-15, 15, 1000)
vvals2 = np.linspace(-45, 45, 91)
signal = np.zeros_like(Delta)

parms = {
	'fsup' : 1e-2,
	'gp' :  6.,
	'gc' : 0.05,
	'hfr' : 8.,
	'mubb' : 12.,
	'wp' : 0.1,
	'wc' : 2.,
	'dwp' : 0.01,
	'dwc' : 0.8,
	'f5p' : 0.1,
	'nv' : vvals2.shape[0],
	'vs' : vvals2
}

ints = []
for i, D in enumerate(Delta):
	print D
	ints.append([])
	for j, nv in enumerate([40]):
		# vvals2 = np.linspace(-45, 45, nv)
		vvals2 = np.linspace(-nv, nv, 2*nv+1)
		parms['nv'] = vvals2.shape[0]
		parms['vs'] = vvals2
		res = solver.solve(delta=D, **parms).imag
		ints[-1].append(np.exp(np.trapz(res*np.exp(-(vvals2/240.)**2), vvals2)))
		if D in [-20, 0, 20]:
			bg = solver.solve(delta=1000, **parms).imag
  			plt.plot(vvals2, res - bg, 'x-')
plt.figure()
ints = np.array(ints)
plt.plot(Delta, ints-ints[:1, :])
plt.show()
raise RuntimeError

scanres1 = np.zeros_like(Delta)
scanres2 = np.zeros_like(Delta)
A = np.fromfile('./output.data').reshape((81, 201))
spline1 = RectBivariateSpline(dp, dc, A)
for i, D in enumerate(Delta):
  vres = spline1.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
  scanres1[i] = np.exp(np.trapz(vres, vvals))

  res = solver.solve(delta=D, **parms)  
  scanres2[i] = np.exp(np.trapz(res.imag*np.exp(-(vvals2/240.)**2), vvals2))

offset = np.exp(np.trapz(spline1.ev(vvals/780.e-3, 100-vvals/486.e-3)*np.exp(-(vvals/240.)**2), vvals))
scanres1 -= offset
parms0 = parms.copy()
parms0['wc'] = 0
res = solver.solve(delta=0., **parms0)
offset = np.exp(np.trapz(res.imag*np.exp(-(vvals2/240.)**2), vvals2))
scanres2 -= offset


print 'total analysis time was:', time.time()-tic, 'seconds'

plt.figure()
plt.plot(Delta, scanres1, label='ODE solver')
plt.plot(Delta, scanres2, label='steady state')
plt.legend()

plt.figure()
plt.plot(Delta, scanres1/scanres1.max(), label='ODE solver normalised')
plt.plot(Delta+5, scanres2[::-1]/scanres2.max(), label='steady state normalised')
plt.legend()
plt.show()

raise RuntimeError

parms = {
	'fsup' : 1e-2,
	'gp' :  6.,
	'gc' : 0.05,
	'hfr' : 8.,
	'wp' : 0.1,
	'wc' : 2.,
	'dwp' : 0.01,
	'dwc' : 0.8,
	'f5p' : 0.1,
	'nv' : vvals2.shape[0],
	'vs' : vvals2
}

bscan = np.zeros((Delta.shape[0], 41))
for i, D in enumerate(Delta):
	print D
	for j, b in enumerate(np.linspace(-20, 20, 41)):
	  vres = spline1.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
	  scanres1[i] = np.exp(np.trapz(vres, vvals))

	  res = solver.solve(delta=D, mubb = b, **parms)  
	  bscan[i, j] = np.exp(np.trapz(res.imag*np.exp(-(vvals2/240.)**2), vvals2))
	res = solver.solve(delta=1000., mubb = b, **parms)  
	offset = np.exp(np.trapz(res.imag*np.exp(-(vvals2/240.)**2), vvals2))
	bscan[i, :] -= offset

plt.imshow(bscan)
plt.show()