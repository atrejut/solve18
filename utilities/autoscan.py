import numpy as np
import os, subprocess
import time

fields = np.linspace(-15, 15, 31)

dirname = '../bin/'
pol = 'pp'

start = time.time()

for f in fields:
    with open('master.info', 'r') as source , open('./' + dirname + '/config.info', 'w+') as dest:
      for line in source:
        if line.startswith('bfield'):
          dest.write('bfield = %14.12fd0\n' %f)
        elif line.startswith('pol'):
          dest.write('pol = "' + pol + '"')
        else:
          dest.write(line)
    subprocess.call(r'../bin/solve18_' + pol, cwd='./'+dirname)
    
stop = time.time()

print 'total execution took', (stop-start)/60., 'minutes'
