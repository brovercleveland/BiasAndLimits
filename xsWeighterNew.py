#!/usr/bin/env python
import pickle
from configLimits import AutoVivification
import configLimits as cfl

f = open('XSBR.p')
xsDict = pickle.load(f)
xsScaleErrDict = pickle.load(f)
xsPDFErrDict = pickle.load(f)
brDict = pickle.load(f)
brErrDict = pickle.load(f)
f.close()

def LumiXSWeighter(year, lepton, sig, mass, nEvt, YR,alt=False):
  LumiXSWeight = 0.0
  if sig == 'ggH': sig = 'ggF'
  if sig == 'qqH': sig = 'VBF'
  if year == '2012': year = '8TeV'
  if year == '2011': year = '7TeV'

  mass = mass+'.0'

  xs = xsDict[YR][year][sig][mass]
  br = brDict[YR]['Zgamma'][mass]

  if type(xs) != float:
    print 'using YR2 xs for ',year,sig,mass
    xs = xsDict['YR2'][year][sig][mass]
  if type(br) != float:
    print 'using YR2 br for ',year,sig,mass
    br = brDict['YR2']['Zgamma'][mass]

  if cfl.modelIndependent:
    LumiXSWeight = nEvt
  elif alt:
    if sig in ['WH','ZH']:
      LumiXSWeight = nEvt/(xs*br*0.10098*1000)
    if sig in ['ttH']:
      LumiXSWeight = nEvt/(xs*br*1000)
  else:
    if sig in ['WH','ZH']:
      LumiXSWeight = nEvt/(xs*br*1000)
    else:
      LumiXSWeight = nEvt/(xs*br*0.10098*1000)

  if year == '7TeV':
    if (lepton=='mu'): LumiXSWeight = 5.05/(LumiXSWeight)
    if (lepton=='el'): LumiXSWeight = 4.98/(LumiXSWeight)
    if (lepton=='all'): LumiXSWeight = 10.03/(LumiXSWeight)

  else:
    if (lepton=='mu'):
      if cfl.suffix == 'Proper':
        LumiXSWeight = 19.6175/(LumiXSWeight)
      else:
        LumiXSWeight = 19.672/(LumiXSWeight)

    elif (lepton=='el'):
      if cfl.suffix == 'Proper':
        LumiXSWeight = 19.6195/(LumiXSWeight)
      else:
        LumiXSWeight = 19.7195/(LumiXSWeight)

  return LumiXSWeight



