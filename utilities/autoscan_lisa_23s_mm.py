#!/usr/bin/python

import numpy as np
import subprocess, os
from datetime import datetime

bvals = np.linspace(-0.8, 0.8, 9)
pol = 'mm'
name = '23s_mm'

timestamp = datetime.now().strftime('%Y%m%d/%H%M%S')

outfolder = os.environ['HOME'] + "/julian/data/" + timestamp + '-' + name

if not os.path.exists(outfolder):
  os.makedirs(outfolder)

for b in bvals:
  # write job script
  with open('../tmp/job-' + name, 'wb') as ifile:
    ifile.write('#PBS -lwalltime=30:00\n')
    ifile.write('#PBS -lnodes=1:cpu3\n')
    ifile.write('cd $TMPDIR\n')
    ifile.write('cp $HOME/julian/solve18/bin/solve18_%s "$TMPDIR"\n' %pol)
    # write new config.infoy
    ifile.write('echo "&PARAMS" > config.info\n')
    ifile.write('echo "bfield = %14.12fd0," >> config.info\n' %b)
    ifile.write('echo "Wc1 = 2.d0," >> config.info\n')
    ifile.write('echo "Wc2 = 2.d0," >> config.info\n')
    ifile.write('echo "Wp = 0.1d0," >> config.info\n')
    ifile.write('echo "hfs = 4.701d0," >> config.info\n')
    ifile.write('echo "G5p = 6.d0," >> config.info\n')
    ifile.write('echo "Gr1 = 0.05d0," >> config.info\n')
    ifile.write('echo "Gr2 = 0.05d0," >> config.info\n')
    ifile.write('echo "gp = 0.01d0," >> config.info\n')
    ifile.write('echo "gc = 0.8d0" >> config.info\n')
    ifile.write('echo "/" >> config.info\n')
    ifile.write('echo "&STEPPING" >> config.info\n')
    ifile.write('echo "NProbe = 801," >> config.info\n')
    ifile.write('echo "NCoupling = 1401," >> config.info\n')
    ifile.write('echo "ShiftProbe = -100," >> config.info\n')
    ifile.write('echo "ShiftCoupling = -175," >> config.info\n')
    ifile.write('echo "StepProbe = 0.25d0," >> config.info\n')
    ifile.write('echo "StepCoupling = 0.25d0" >> config.info\n')
    ifile.write('echo "/" >> config.info\n')
    ifile.write('echo "&SIM" >> config.info\n')
    ifile.write('echo "pol = \\\"%s\\\"" >> config.info\n' %pol)
    ifile.write('echo "/" >> config.info\n')
    ifile.write('cat config.info\n')
    # run program
    ifile.write('FORT_FMT_RECL=100000 ./solve18_%s\n'%pol)
    # return results to home drive
    ifile.write('cp output.txt "%s/data%5.2f"\n' %(outfolder, b))
  
  while subprocess.call(['qsub',  'job-' + name], cwd='../tmp/') != 0:
    print 'qsub timed out, trying again with identical parameters'

