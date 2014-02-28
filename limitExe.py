#!/usr/bin/env python
import os
import sys

os.chdir(os.environ.get('_CONDOR_SCRATCH_DIR'))
os.system('tar xvzf limitFiles.tgz')

mass=sys.argv[1]
suffix=sys.argv[2]
comboName = '_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
outputName = '_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
print 'running limitProducer, mass: {0}'.format(mass)
os.system('combine -M Asymptotic '+comboName+' > '+outputName)

print 'Done'
