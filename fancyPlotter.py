#!/usr/bin/env python
import sys
sys.argv.append('-b')
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *

gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

def Cat0BGComps(TFiles = ['testRooFitOut_MVA_Andy.root' ):
  for TFile in TFiles:

