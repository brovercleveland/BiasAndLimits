#! /bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
scram pro CMSSW CMSSW_6_2_3
cd CMSSW_6_2_3/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}


echo $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18}

./biasStudy_toyMaker.py $1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18}
