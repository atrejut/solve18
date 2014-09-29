import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import RectBivariateSpline
import os

#folder = '20140919/200820-scanB_mp/'
#folder = '20140919/201134-scanB_mm/'
#folder = '20140919/200748-scanB_pm/'
##root = '$HOME/julian/data/20140925/'
root = 'D:/julian/data/20140925/'

os.mkdir(root+'plots')
folders=[x for x in os.listdir(root)]
for folder in folders:
        n=int(folder[7:9])
        pol=folder[-2:]
        files = [x for x in os.listdir(root+folder) if x.startswith('data')]
        x_values=np.load(root+folder+'/detuning.npy')
        y_values=np.load(root+folder+'/results.npy')
        ##plt.figure()
        ##plt.imshow(scanres, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
        ##plt.xlabel('B-Field (G)')
        ##plt.ylabel('Coupling Detuning (MHz)')
        
        plt.figure()
        for i in range(len(files)):
                b_value=(i+1)/float(len(files))
                print b_value
                plt.plot(x_values,-1*y_values[:,i],'b',alpha=b_value)
        plt.title('EIT for %ss %s' %(n,pol))
        plt.xlabel('Coupling Detuning (MHz)')
        plt.ylabel('signal')
        plt.savefig(root+'plots/'+'%ss_%s.png' %(n,pol))

        ##plt.figure()
        ##plt.imshow(scanres0, aspect='auto', interpolation='none', extent=[-15, 15, -50, 40])
        ##plt.xlabel('B-Field (G)')
        ##plt.ylabel('Coupling Detuning (MHz)')
        ##plt.show()



