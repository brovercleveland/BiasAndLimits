#! /bin/bash

cardName="12-04-14_HighMass800"
#cardName="12-04-14_HighMassNarrow800"
cardSuffix="_YR3_DCB"
#cardSuffix="_YR3_CBG"


for i in `seq 200.0 5.0 500.0`; do
#for i in 200.0; do
  echo "Checking 0 signal case for " $i
  echo "Max likelihood, signal = 0" > crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
  combine -M MaxLikelihoodFit -t -1 --expectSignal 0 --rMin -20 --rMax 20 --minos=all --minimizerTolerance 0.00001 outputDir/${cardName}${cardSuffix}/${i}/hzg_FullCombo_M${i}_${cardName}.txt | cat >> crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
  echo "Checking nuisances" 
  python diffNuisances.py -a mlfit.root -g plots.root >> crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
  echo "Checking 1 signal case for " $i
  echo "" >> crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
  echo "Max likelihood, signal = 1" >> crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
  combine -M MaxLikelihoodFit -t -1 --expectSignal 1 --rMin -20 --rMax 20 --minos=all --minimizerTolerance 0.00001 outputDir/${cardName}${cardSuffix}/${i}/hzg_FullCombo_M${i}_${cardName}.txt | cat >> crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
  echo "Checking nuisances" 
  python diffNuisances.py -a mlfit.root -g plots.root >> crossCheckOutputs/${cardName}${cardSuffix}_${i}_check.txt
done

#combine -M MaxLikelihoodFit -t -1 --expectSignal 0 outputDir/12-04-14_HighMass800_YR3_DCB/200.0/hzg_FullCombo_M200.0_12-04-14_HighMass800.txt > crossCheckOutputs/12-04-14_HighMass800_YR3_DCB_200.0_check.txt
