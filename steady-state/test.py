import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver
from scipy.interpolate import RectBivariateSpline

tic = time.time()
parms = {
	'fsup' : 1e-2,
	'gp' :  6.,
	'gc' : 0.05,
	'hfr' : 8.,
	'mubb' : 0.,
	'wp' : 0.1,
	'wc' : 2.,
	'dwp' : 0.01,
	'dwc' : 0.8,
	'f5p' : 0.4
}
tic = time.time()
res = solver.solve(**parms)
print 'pure fortran time was:', time.time()-tic, 'seconds'

dp = -20+0.5*np.arange(81)
dc = -50+0.5*np.arange(201)
Delta = np.linspace(-15, 15, 100)
vvals = np.linspace(-15, 15, 1000)
signal = np.zeros_like(Delta)

# now here we do it for a whole scan of B-field values
scanres1 = np.zeros_like(Delta)
scanres2 = np.zeros_like(Delta)
A = np.fromfile('./output.data').reshape((81, 201))
spline1 = RectBivariateSpline(dp, dc, A)
spline2 = RectBivariateSpline(dp, dc, res.imag)
for i, D in enumerate(Delta):
  vres = spline1.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
  scanres1[i] = np.exp(np.trapz(vres, vvals))
  vres = spline2.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
  scanres2[i] = np.exp(np.trapz(vres, vvals))
offset = np.exp(np.trapz(spline1.ev(vvals/780.e-3, 100-vvals/486.e-3)*np.exp(-(vvals/240.)**2), vvals))
scanres1 -= scanres1.max()
offset = np.exp(np.trapz(spline2.ev(vvals/780.e-3, 100-vvals/486.e-3)*np.exp(-(vvals/240.)**2), vvals))
scanres2 -= scanres2.max()


print 'total analysis time was:', time.time()-tic, 'seconds'

plt.figure()
plt.plot(Delta, scanres1, label='ODE solver')
plt.plot(Delta, scanres2, label='steady state')
#plt.plot(Delta+5, scanres2[::-1]/1.5, label='steady state adjusted')
plt.legend()

plt.figure()
plt.plot(Delta, (scanres1 - scanres1.min())/(scanres1.max()-scanres1.min()), label='ODE solver')
plt.plot(Delta+5, (scanres2[::-1] - scanres2.min())/(scanres2.max()-scanres2.min()), label='steady state')
plt.legend()
plt.show()