#!/usr/bin/python

import numpy as np
import subprocess, os
from datetime import datetime

wpvals = np.linspace(0, 6, 13)
wcvals = np.linspace(0, 20, 41)

pol = 'mp'
name = 'Wscan_mp'

timestamp = datetime.now().strftime('%Y%m%d/%H%M%S')

outfolder = os.environ['HOME'] + "/atreju/data/" + timestamp + '-' + name

if not os.path.exists(outfolder):
  os.makedirs(outfolder)

for wp in wpvals:
  for wc in wcvals:
    # write job script
    with open('../tmp/job-' + name, 'wb') as ifile:
      ifile.write('#PBS -lwalltime=15:00\n')
      ifile.write('#PBS -lnodes=1:cpu3\n')
      ifile.write('cd $TMPDIR\n')
      ifile.write('cp $HOME/atreju/solve18/bin/solve18_%s "$TMPDIR"\n' %pol)
      # write new config.infoy
      ifile.write('echo "&PARAMS" > config.info\n')
      ifile.write('echo "bfield = 10.d0," >> config.info\n')
      ifile.write('echo "Wc1 = %14.12fd0," >> config.info\n' %wc)
      ifile.write('echo "Wc2 = %14.12fd0," >> config.info\n' %wc)
      ifile.write('echo "Wp = %14.12fd0," >> config.info\n' %wp)
      ifile.write('echo "hfs = 8.d0," >> config.info\n')
      ifile.write('echo "G5p = 6.d0," >> config.info\n')
      ifile.write('echo "Gr1 = 0.05d0," >> config.info\n')
      ifile.write('echo "Gr2 = 0.05d0," >> config.info\n')
      ifile.write('echo "gp = 0.01d0," >> config.info\n')
      ifile.write('echo "gc = 0.8d0" >> config.info\n')
      ifile.write('echo "/" >> config.info\n')
      ifile.write('echo "&STEPPING" >> config.info\n')
      ifile.write('echo "NProbe = 401," >> config.info\n')
      ifile.write('echo "NCoupling = 601," >> config.info\n')
      ifile.write('echo "ShiftProbe = -100," >> config.info\n')
      ifile.write('echo "ShiftCoupling = -150," >> config.info\n')
      ifile.write('echo "StepProbe = 0.5d0," >> config.info\n')
      ifile.write('echo "StepCoupling = 0.5d0" >> config.info\n')
      ifile.write('echo "/" >> config.info\n')
      ifile.write('echo "&SIM" >> config.info\n')
      ifile.write('echo "pol = \\\"%s\\\"" >> config.info\n' %pol)
      ifile.write('echo "/" >> config.info\n')
      ifile.write('cat config.info\n')
      # run program
      ifile.write('FORT_FMT_RECL=100000 ./solve18_%s\n'%pol)
      # return results to home drive
      ifile.write('cp output.meta "%s/meta_wp%5.2f_wc%5.2f"\n' %(outfolder, wp, wc))
      ifile.write('cp output.data "%s/data_wp%5.2f_wc%5.2f"\n' %(outfolder, wp, wc))
  
    while subprocess.call(['qsub',  'job-' + name], cwd='../tmp/') != 0:
      print 'qsub timed out, trying again with identical parameters'

