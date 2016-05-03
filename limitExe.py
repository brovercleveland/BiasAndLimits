#!/usr/bin/env python
import os
import sys

os.chdir(os.environ.get('_CONDOR_SCRATCH_DIR'))
os.system('tar xvzf limitFiles.tgz')

mass=sys.argv[1]
suffix=sys.argv[2]
outPutFolder = sys.argv[4]
syst = sys.argv[5]

cardName = sys.argv[3]

outputName = 'Output'+cardName[3:]
print 'running limitExe, {0}, mass: {1}'.format(cardName,mass)
os.system('combine -M Asymptotic --minimizerStrategy 0 -m {0} -n {2} {1}'.format(mass,cardName,outputName.replace('M'+mass,'').replace('.txt','')))


print 'Done'
