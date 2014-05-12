#!/usr/bin/env python
import os
import sys

os.chdir(os.environ.get('_CONDOR_SCRATCH_DIR'))
os.system('tar xvzf limitFiles.tgz')

mass=sys.argv[1]
suffix=sys.argv[2]
outPutFolder = sys.argv[4]

cardName = sys.argv[3]
outputName = outPutFolder+'Output'+cardName[3:]
print 'running limitProducer, {0}, mass: {1}'.format(cardName,mass)
os.system('combine -M Asymptotic --minimizerStrategy 1 -m {0} {1} > {2}'.format(mass,cardName,outputName))


print 'Done'
