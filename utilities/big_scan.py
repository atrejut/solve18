#!/usr/bin/python

import numpy as np
import subprocess, os
from datetime import datetime

nvals = np.linspace(19,26,8)
print nvals
bvals = np.linspace(-0.8, 0.8, 9)
pol =['mm','pm','mp','pp']
hfList = [9.345, 7.769, 6.409, 5.431, 4.701, 4.182 , 3.667,3.356]
velocity=240
probe_range=0
coupling_range=15
step_size=0.25

pr=probe_range+int(round(velocity/0.78))
cr=coupling_range+int(round(velocity/0.48))
p_steps=int(pr*2*1/step_size+1)
c_steps=int(cr*2*1/step_size+1)
print pr
print cr
date = datetime.now().strftime('%Y%m%d')
timestamp=datetime.now().strftime('%H%M%S')

hfs_sel =0;
for n in nvals:
  hfs=hfList[hfs_sel]
  for p in pol:
    name = '%s_s-%s' %(int(n),p)
    outfolder =  os.environ['HOME'] +"/julian_git/data/"+str(date) +"/"+str(timestamp)+"/" +name
    if not os.path.exists(outfolder):
      os.makedirs(outfolder)
    print name
    for b in bvals:
##      print(hfs)
      # write job script
     
      with open('../tmp/job-' + name, 'wb') as ifile:
        ifile.write('#PBS -lwalltime=5:00:00\n')
        ifile.write('#PBS -lnodes=1:cpu3\n')
        ifile.write('cd $TMPDIR\n')
        ifile.write('cp $HOME/julian/solve18/bin/solve18_%s "$TMPDIR"\n' %p)
          # write new config.infoy
        ifile.write('echo "&PARAMS" > config.info\n')
        ifile.write('echo "bfield = %14.12fd0," >> config.info\n' %b)
        ifile.write('echo "Wc1 = 2.d0," >> config.info\n')
        ifile.write('echo "Wc2 = 2.d0," >> config.info\n')
        ifile.write('echo "Wp = 0.1d0," >> config.info\n')
        ifile.write('echo "hfs = %.3fd0," >> config.info\n' %hfs)
        ifile.write('echo "G5p = 6.d0," >> config.info\n')
        ifile.write('echo "Gr1 = 0.05d0," >> config.info\n')
        ifile.write('echo "Gr2 = 0.05d0," >> config.info\n')
        ifile.write('echo "gp = 0.01d0," >> config.info\n')
        ifile.write('echo "gc = 0.8d0" >> config.info\n')
        ifile.write('echo "/" >> config.info\n')
        ifile.write('echo "&STEPPING" >> config.info\n')
        ifile.write('echo "NProbe = %d," >> config.info\n' %p_steps)
        ifile.write('echo "NCoupling = %d," >> config.info\n' %c_steps)
        ifile.write('echo "ShiftProbe = -%d," >> config.info\n' %pr)
        ifile.write('echo "ShiftCoupling = -%d," >> config.info\n' %cr)
        ifile.write('echo "StepProbe = %.2fd0," >> config.info\n' %step_size)
        ifile.write('echo "StepCoupling = %.2fd0" >> config.info\n' %step_size)
        ifile.write('echo "/" >> config.info\n')
        ifile.write('echo "&SIM" >> config.info\n')
        ifile.write('echo "pol = \\\"%s\\\"" >> config.info\n' %p)
        ifile.write('echo "/" >> config.info\n')
        ifile.write('cat config.info\n')
          # run program
        ifile.write('FORT_FMT_RECL=100000 ./solve18_%s\n'%p)
         # return results to home drive
        ifile.write('cp output.meta "%s/meta%5.2f"\n' %(outfolder, b))
        ifile.write('cp output.data "%s/data%5.2f"\n' %(outfolder, b))
      ##  
      ##  while subprocess.call(['qsub',  'job-' + name], cwd='../tmp/') != 0:
      ##    print 'qsub timed out, trying again with identical parameters'
  hfs_sel+=1

