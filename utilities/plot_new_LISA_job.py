import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import RectBivariateSpline
import os

#folder = '20140919/200820-scanB_mp/'
#folder = '20140919/201134-scanB_mm/'
#folder = '20140919/200748-scanB_pm/'
root = '/home/junaber/julian_git/data/20140928/235731'
##root = 'D:/julian/data/235731/'

probe_range=128
coupling_range=225
pr=probe_range
cr=coupling_range
step_size=0.25
p_steps=int(pr*2*1/step_size+1)
c_steps=int(cr*2*1/step_size+1)


##dp = -pr+step_size*np.arange(p_steps)
##dc = -cr+step_size*np.arange(c_steps)
Delta = np.linspace(-15, 15, 500)
vvals = np.linspace(-100, 100, 5000)
signal = np.zeros_like(Delta)

folders=[x for x in os.listdir(root)]
for folder in folders:
        meta = {}
        metafiles = [x for x in os.listdir(root+folder) if x.startswith('meta')]
        with open(root+folder+'/' + metafiles[0], 'rb') as ifile:
                for line in ifile:
                        key, val = line.split()
                        try:
                                meta[key[:-1]] = float(val)
                        except ValueError:
                                meta[key[:-1]] = val

        dp = meta['ShiftProbe'] + meta['StepProbe']*np.arange(meta['NProbe'])
        dc = meta['ShiftCoupling']+meta['StepCoupling']*np.arange(meta['NCoupling'])
        n=int(folder[0:2])
        pol=folder[-2:]
        # now here we do it for a whole scan of B-field values
        files = [x for x in os.listdir(root+folder) if x.startswith('data')]
        scanres = np.zeros((len(Delta), len(files)))
        scanres0 = np.zeros((len(Delta), len(files)))
        for i, f in enumerate(sorted(files, key = lambda x : float(x[4:]))):
                
##
                print n
                print pol
                print root+folder+'/'+f
##                A = np.genfromtxt(root+folder+'/'+f, skiprows=17).T
##                index = int(round((float(f[4:]) + 0.8)*5))
                A = np.fromfile(root+folder+'/' + f).reshape(meta['NProbe'], meta['NCoupling'])
                index = i
                print f, index
                spline = RectBivariateSpline(dp, dc, A)
                for i, D in enumerate(Delta):
                        vres = spline.ev(vvals/780.e-3, D-vvals/486.e-3)*np.exp(-(vvals/240.)**2)
                        scanres[i, index] = np.exp(np.trapz(vres, vvals))
                offset = np.exp(np.trapz(spline.ev(vvals/780.e-3, 100-vvals/486.e-3)*np.exp(-(vvals/240.)**2), vvals))
                scanres0[:, index] = scanres[:, index]-offset
                        
        ##plt.figure()
        ##plt.imshow(scanres, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
        ##plt.xlabel('B-Field (G)')
        ##plt.ylabel('Coupling Detuning (MHz)')

        plt.figure()
        for i in range(len(files)):
                b_value=(i+1)/float(len(files))
                print b_value
                plt.plot(Delta,-1*scanres0[:,i],'b',alpha=b_value)
        plt.title('EIT for %ss %s' %(n,pol))
        plt.xlabel('Coupling Detuning (MHz)')
        plt.ylabel('signal')
        plt.savefig(root+folder+'/'+'plot.png')
##        plt.show()
        ##plt.figure()
        ##plt.imshow(scanres0, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
        ##plt.xlabel('B-Field (G)')
        ##plt.ylabel('Coupling Detuning (MHz)')
        ##plt.show()



