from __future__ import division

import numpy as np
from matplotlib import pyplot as plt
from numpy import pi
import time
import solver_pp as solver
from scipy.interpolate import UnivariateSpline, RectBivariateSpline
import seaborn as sns
import pandas as pd
import matplotlib


pal = sns.diverging_palette(255, 15, s=90, l=50, center="dark", as_cmap=True)
linpal = sns.light_palette('red', reverse=True, as_cmap=True)

def make_cmap(mn, mx):
	lowratio = 1.*abs(mn)/(abs(mn) + mx)
	# lowratio + highratio*highfract = 
	# lowratio + (1-lowratio)*highfract = 
	# highfract + lowratio(1-highfract)
	
	cdict = {'red':   ((0.0, 0.0, 0.0),
	                   (lowratio, 0.0416, 0.0416),
	                   (0.36479+0.63521*lowratio, 1.0, 1.0),
	                   (1.0, 1.0, 1.0)),
	         'green': ((0.0, 0.3, 0.3),
	                   (lowratio, 0.0, 0.0),
	                   (0.36479+0.63521*lowratio, 0.0, 0.0),
	                   (0.746032+0.253968*lowratio, 1.0, 1.0),
	                   (1.0, 1.0, 1.0)),
	         'blue':  ((0.0, 1.0, 1.0),
	                   (lowratio, 0.1, 0.1),
	                   (0.746032+0.253968*lowratio, 0.0, 0.0),
	                   (1.0, 1.0, 1.0))}
	return matplotlib.colors.LinearSegmentedColormap('cmCustom',cdict,512)
custpal = make_cmap(-7/8, 8/8)

# load data, and select frequency range of interest
dfs = {}
for kind in ['same', 'oppos']:#, './data/20s_Zeeman_sym.csv']:
	filename = './data/20s_Zeeman_' + kind + '_pol.csv'
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
	idata /= idata.max()

	dfs['exp_' + kind] = pd.DataFrame(idata, index=f2, columns=b2)

	# plt.figure()
	# plt.title(filename)
	# plt.imshow(idata, aspect='equal', extent=[-17, 17, -20, 20])

counter = 0
for t in ['pm', 'pp']:
	model = np.load('model_' + t + '.npy').T
	freq = np.linspace(-20, 20, 81)
	field = np.linspace(-20, 20, 81)
	spline = RectBivariateSpline(freq, field, model)
	f2 = np.linspace(-20, 20, 401)
	b2 = np.linspace(-17, 17, 61)
	idata = spline(f2, b2)
	if t.startswith('m'):
		idata = -idata
	idata /= idata.max()

	dfs['theo_' + t] = pd.DataFrame(idata, index=f2, columns=b2)


plt.figure()

ax1 = plt.subplot(2, 2, 1)
# sns.heatmap(dfs['exp_same'], vmax=7, center=0, linewidths=0, cbar=False, xticklabels=6, yticklabels=25, ax=ax1)
plt.imshow(dfs['exp_same'], vmin=-7/8, vmax=8/8, aspect='auto', cmap=custpal, extent=[-17, 17, -19.9, 19.9], interpolation='nearest')
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.set_title('Experimental')
plt.grid(True, linestyle='--', alpha=0.2)
ax3 = plt.subplot(2, 2, 3, sharex=ax1)
# sns.heatmap(dfs['exp_oppos'], vmax=7, center=0, linewidths=0, cbar=False, xticklabels=6, yticklabels=25, ax=ax3)
plt.imshow(dfs['exp_oppos'], vmin=-7/8, vmax=8/8, aspect='auto', cmap=custpal, extent=[-17, 17, -19.9, 19.9], interpolation='nearest')
plt.grid(True, linestyle='--', alpha=0.2)

ax2 = plt.subplot(2, 2, 2, sharey=ax1)
# sns.heatmap(dfs['theo_pm'], vmax=7, center=0, linewidths=0, cbar=False, xticklabels=6, yticklabels=25, ax=ax2)
plt.imshow(dfs['theo_pm'], vmin=-7/8, vmax=8/8, aspect='auto', cmap=custpal, extent=[-17, 17, -19.9, 19.9], interpolation='nearest')
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.grid(True, linestyle='--', alpha=0.2)
ax2.set_title('Theory')
ax4 = plt.subplot(2, 2, 4, sharey=ax3)
# sns.heatmap(dfs['theo_pp'], vmax=7, center=0, linewidths=0, cbar=False, xticklabels=6, yticklabels=25, ax=ax4)
plt.imshow(dfs['theo_pp'], vmin=-7/8, vmax=8/8, aspect='auto', cmap=custpal, extent=[-17, 17, -19.9, 19.9], interpolation='nearest')
plt.setp(ax4.get_yticklabels(), visible=False)
plt.grid(True, linestyle='--', alpha=0.2)
plt.tight_layout()
plt.show()