#!/usr/bin/env python
import sys
sys.argv.append('-b')
import os
from ROOT import *
import numpy as np
from collections import defaultdict

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

fullCombo = True
byParts = False

massList = [120.0,120.5,121.0,138.0]

c = TCanvas("c","c",0,0,500,400)
c.cd()

if fullCombo:
  fileListTmp = os.listdir('limitOutputs')
  fileList = filter(lambda fileName: 'FullCombo' in fileName,fileListTmp)
  for mass in massList:
    thisFile = filter(lambda fileName: str(mass) in fileName,fileList)
    print thisFile

