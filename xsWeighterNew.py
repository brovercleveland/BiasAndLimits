#!/usr/bin/env python
import pickle
from signalCBFits import AutoVivification
import configLimits as cfl

f = open('XSBR.p')
xsDict = pickle.load(f)
brDict = pickle.load(f)
f.close()

def LumiXSWeighter(year, lepton, sig, mass, nEvt, YR):
  LumiXSWeighter = 0.0
  if sig == 'ggH': sig = 'ggF'
  if sig == 'qqH': sig = 'VBF'
  if year == '2012': year = '8TeV'
  if year == '2011': year = '7TeV'

  mass = mass+'.0'

  if sig in ['WH','ZH']:
    LumiXSWeighter = nEvt/(xsDict[YR][year][sig][mass]*brDict[YR][year]['ZGamma'][mass]*1000)
  else:
    LumiXSWeighter = nEvt/(xsDict[YR][year][sig][mass]*brDict[YR][year]['ZGamma'][mass]*0.10098*1000)

  if year == '8TeV':
    if (lepton=='mu'): LumiXSWeight = 5.05/(LumiXSWeight)
    if (lepton=='el'): LumiXSWeight = 4.98/(LumiXSWeight)
    if (lepton=='all'): LumiXSWeight = 10.03/(LumiXSWeight)

  else:
    if (lepton=='mu'):
      if cfl.suffix == 'Proper':
        LumiXSWeight = 19.6175/(LumiXSWeight)
      else:
        LumiXSWeight = 19.7175/(LumiXSWeight)

    elif (lepton=='el'):
      if cfl.suffix == 'Proper':
        LumiXSWeight = 19.6195/(LumiXSWeight)
      else:
        LumiXSWeight = 19.7195/(LumiXSWeight)

  return LumiXSWeight



