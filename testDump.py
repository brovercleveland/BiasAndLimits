#!/usr/bin/env python
import sys
sys.argv.append('-b')
import os
from ROOT import *
import numpy as np
import configLimits as cfl

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

f = TFile('outputDir/07-29-14_Proper_YR3_CBG/125.0/higgsCombineTest.Asymptotic.mH125.root')
t = f.Get('limit')
for ev in t:
  print ev.limit
