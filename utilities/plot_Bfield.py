import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import RectBivariateSpline
import os

#folder = '20140919/200820-scanB_mp/'
#folder = '20140919/201134-scanB_mm/'
#folder = '20140919/200748-scanB_pm/'
folder = '20140924/225518-23s_mm/'

probe_range=100
coupling_range=175
pr=probe_range
cr=coupling_range
step_size=0.25
p_steps=int(pr*2*1/step_size+1)
c_steps=int(cr*2*1/step_size+1)


dp = -pr+step_size*np.arange(p_steps)
dc = -cr+step_size*np.arange(c_steps)
Delta = np.linspace(-15, 15, 500)
vvals = np.linspace(-15, 15, 500)
signal = np.zeros_like(Delta)

# now here we do it for a whole scan of B-field values
files = [x for x in os.listdir(folder) if x.startswith('data')]
scanres = np.zeros((len(Delta), len(files)))
scanres0 = np.zeros((len(Delta), len(files)))
for f in sorted(files):
	print folder+f
	A = np.genfromtxt(folder + f, skiprows=17).T
	index = int(round((float(f[4:]) + 0.8)*5))
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
for i in range(len(files)):
        b_value=(i+1)/float(len(files))
        print b_value
        plt.plot(Delta,-1*scanres0[:,i],'b',alpha=b_value)
plt.xlabel('Coupling Detuning (MHz)')
plt.ylabel('signal')

plt.figure()
plt.imshow(scanres0, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
plt.xlabel('B-Field (G)')
plt.ylabel('Coupling Detuning (MHz)')

plt.show()



