#!/usr/bin/env python

# class for multi-layered nested dictionaries, pretty cool
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

##########
# common #
##########

doMVA = False
#suffix = 'Proper'
#suffix = '05-07-14_Proper'
#suffix = '05-07-14_PhoMVA'
#suffix = '05-07-14_PhoMVAKinMVA'
suffix = '07-25-14_PhoMVAHighMass'
#suffix = '07-25-14_PhoMVAKinMVA'
#suffix = '07-25-14_PhoMVA'
#suffix = '07-29-14_Proper'

#leptonList = ['mu','el']
leptonList = ['mu']
#yearList = ['2011','2012']
yearList = ['2012']
#tevList = ['7TeV','8TeV']
tevList = ['8TeV']
catListBig = ['0','1','2','3','4','5','6','7','8','9']
#catListSmall = ['0','1','2','3','4','5']
catListSmall = ['0']
#massList = ['120','125','130','135','140','145','150','155','160']
massList = ['125']
#sigNameList = ['ggH','qqH','ttH','WH','ZH']
sigNameList = ['ggH']
YR = 'YR3'
highMass = True


if highMass:
  massList = ['200','300','400']
  sigNameList = ['ggH']
  yearList = ['2012']
  tevList = ['8TeV']




######################
# initialFitProducer #
######################

debugPlots = True
verbose = True
rootrace = False
allBiasFits= False# Turn on extra fits used in bias studies
sigNameListInput = ['gg','vbf','tth','wh','zh']

bgFitListTurnOn = ['GaussPow','GaussExp','GaussBern3','GaussBern4','GaussBern5']
bgFitListVBF = ['Exp','Pow','Bern2','Bern3','Bern4']
bgFitListHighMass = ['Pow','PowDecay','PowLog','Exp2','Laurent','ExpSum']


if highMass:
  sigNameListInput = ['gg']
  catListSmall = ['0']


##############
# bgCardPrep #
##############

doExt = False

################
# signalCBFits #
################

#sigFit = 'TripG'
sigFit = 'CBG'

testPoint = '125.0'

massListBig = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5',
'124.6','124.7','124.8','124.9','125.0','125.1','125.2','125.3','125.4','125.5',
'125.6','125.7','125.8','125.9','126.0','126.1','126.2','126.3','126.4','126.5',
'127.0','127.5','128.0','128.5','129.0','129.5','130.0',
'130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
'135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
'141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
'151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']

#massListBig = ['125.0']
if highMass:
  massListBig = ['200.0','300.0','400.0']
  testPoint = '200.0'

###############
# batchSignal #
###############

#no special switches

#############
# cardMaker #
#############

#no special switches

#################
# limitProducer #
#################

fullCombo = False
byParts = True

###############
# batchLimits #
###############

#mode = 'Combo'
mode = 'noCombo'

syst = True

########################
########################
# Define limit bgFits: #
########################
########################

bgLimitDict = AutoVivification()
#bgLimitDict[highMass][tev][lepton][cat]
bgLimitDict[True]['8TeV']['mu']['0'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['1'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['2'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['3'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['4'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['5'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['6'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['7'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['8'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['9'] = 'PowDecay'

bgLimitDict[True]['8TeV']['el']['0'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['1'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['2'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['3'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['4'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['5'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['6'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['7'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['8'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['9'] = 'PowDecay'

bgLimitDict[False]['8TeV']['mu']['0'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['1'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['2'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['3'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['4'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['5'] = 'Bern3'
bgLimitDict[False]['8TeV']['mu']['6'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['7'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['8'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['9'] = 'GaussBern5'

bgLimitDict[False]['8TeV']['el']['0'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['1'] = 'GaussBern4'
bgLimitDict[False]['8TeV']['el']['2'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['3'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['4'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['5'] = 'Bern3'
bgLimitDict[False]['8TeV']['el']['6'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['7'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['8'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['9'] = 'GaussBern5'

bgLimitDict[False]['7TeV']['mu']['0'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['mu']['1'] = 'GaussBern4'
bgLimitDict[False]['7TeV']['mu']['2'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['mu']['3'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['mu']['4'] = 'GaussBern5'

bgLimitDict[False]['7TeV']['el']['0'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['el']['1'] = 'GaussBern4'
bgLimitDict[False]['7TeV']['el']['2'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['el']['3'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['el']['4'] = 'GaussBern5'

bgLimitDict[False]['7TeV']['all']['5'] = 'Bern3'

if __name__=='configLimits':
  for name in dir():
      myvalue = eval(name)
      if '__' not in name:
        print name, "=", myvalue

