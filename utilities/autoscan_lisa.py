#!/usr/bin/python

import numpy as np
import subprocess

bvals = np.arange(-15, 15, 1)

for b in bvals:
  # write job script
  with open('../tmp/jobscript', 'wb') as ifile:
    ifile.write('#PBS -lwalltime=25:00\n')
    ifile.write('#PBS -lnodes=1\n')
    ifile.write('cd $TMPDIR\n')
    ifile.write('cp $HOME/atreju/solve18/bin/solve18_pp "$TMPDIR"\n')
    # write new config.info
    ifile.write('echo "&PARAMS" > config.info\n')
    ifile.write('echo "bfield = %14.12fd0," >> config.info\n' %b)
    ifile.write('echo "Wc1 = 1.d0," >> config.info\n')
    ifile.write('echo "Wc2 = 1.d0," >> config.info\n')
    ifile.write('echo "Wp = 0.1d0," >> config.info\n')
    ifile.write('echo "hfs = 8.d0," >> config.info\n')
    ifile.write('echo "G5p = 6.d0," >> config.info\n')
    ifile.write('echo "Gr1 = 0.05d0," >> config.info\n')
    ifile.write('echo "Gr2 = 0.05d0," >> config.info\n')
    ifile.write('echo "gp = 0.01d0," >> config.info\n')
    ifile.write('echo "gc = 0.8d0" >> config.info\n')
    ifile.write('echo "/" >> config.info\n')
    ifile.write('echo "&STEPPING" >> config.info\n')
    ifile.write('echo "NProbe = 81," >> config.info\n')
    ifile.write('echo "NCoupling = 201," >> config.info\n')
    ifile.write('echo "ShiftProbe = -20," >> config.info\n')
    ifile.write('echo "ShiftCoupling = -50," >> config.info\n')
    ifile.write('echo "StepProbe = 0.5d0," >> config.info\n')
    ifile.write('echo "StepCoupling = 0.5d0" >> config.info\n')
    ifile.write('echo "/" >> config.info\n')
    ifile.write('echo "&SIM" >> config.info\n')
    ifile.write('echo "pol = \\\"pp\\\"" >> config.info\n')
    ifile.write('echo "/" >> config.info\n')
    ifile.write('cat config.info\n')
    # run program
    ifile.write('./solve18_pp\n')
    # return results to home drive
    ifile.write('cp output.txt $HOME/atreju/bscan/result' + str(b) + '\n')
  
  subprocess.call(['qsub',  'jobscript'], cwd='../tmp/')

