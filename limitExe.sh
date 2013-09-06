#!/bin/sh

cd ${_CONDOR_SCRATCH_DIR}
mkdir testCards
mv *.txt testCards/.
mv *.root testCards/.

mass=$1
echo "running limitProducer, mass: $mass" >> /dev/stderr
./limitProducer.py $mass

rm limitProducer.py
echo "DONE" >> /dev/stderr
