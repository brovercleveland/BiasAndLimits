#!/usr/bin/env python

import sys
import configLimits as cfl
YR = cfl.YR
sigFit = cfl.sigFit
highMass = cfl.highMass
suffix = cfl.suffixPostFix

def doTables():

  massList = cfl.massList
  leptonList = cfl.leptonList
  tevList = cfl.tevList
  genList = cfl.genFuncs
  #genListAbbr = ['GE', 'GP', 'SE', 'SP']
  genListAbbr = ['P', 'L', 'E', 'G', 'W', 'H']
  catList = cfl.catListSmall
  fitList = cfl.tableFuncs
  doLandscape = True
  biasMethod ='bgPull'
  #biasMethod ='typeA'

# get all the txt files from the pull plots, put them in a dictionary (they
# are all uniquely named so you can just key on their names, makes callback
# easy later on in the code
  inputFileDict ={}
  latexFile = open('pyTablesNoCat.tex','w')

# start the header
  latexFile.write('\\documentclass[11pt,final]{article}\n')
  latexFile.write('\\usepackage[margin=1in]{geometry}\n')
  latexFile.write('\\usepackage{color, colortbl}\n')
  latexFile.write('\\usepackage{graphics}\n')
  latexFile.write('\\definecolor{Yellow}{rgb}{1,1,0}\n')
  latexFile.write('\\usepackage{pdflscape}\n')
  latexFile.write('\\begin{document}\n')
  if(doLandscape): latexFile.write('\\begin{landscape}\n')
  for mass in massList:
# starting the Type-A tables
    latexFile.write('\\begin{table}[htb]\n')
    latexFile.write(' \\begin{center}\n')
# we are making a column for each fit function (plus and extra column for the
# category number
    latexFile.write('  \\resizebox{\columnwidth}{!}{%\n')
    latexFile.write('  \\begin{tabular}{'+'|c'*(len(fitList)+1)+'|}\n')
    latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{~} \\\\ \n')
    latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{{\\bf Type-A Bias, mH='+mass+'}} \\\\ \n')
    latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{~} \\\\ \n')
    for lepton in leptonList:
      for tev in tevList:
        latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{~} \\\\ \n')
        latexFile.write('  \\hline \n')
        latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{|c|}{'+tev+' '+lepton+'} \\\\ \n')
        latexFile.write('  \\hline \n')
        latexFile.write('  cat. & ')
# we're about to write the header for the individual table, letting it know
# how many fit functions and how many gen functions
        fitListAndGenAbbr = [x +'('+'/'.join(genListAbbr)+')' for x in fitList]
        #fitListAndGenAbbr = [x +'('+'/'.join(genList)+')' for x in fitList]
        latexFile.write((' & ').join(fitListAndGenAbbr))
        latexFile.write(' \\\\ \n')
        latexFile.write('  \\hline \n')
        for cat in catList:
          latexFile.write('  '+cat+' & ')
          fullFitValList = []
          #yellow = False
          for fit in fitList:
            print fit
            fitValList = []
#pull up all the bias values from the files we stored, run thru them in a complicated way, abuse the 'join' command, drink a lot after you finish
            for gen in genList:
              triggerLine = 'triggerLine'

              biasPath = '/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'
              biasPath = biasPath+suffix+'_'+YR+'_'+sigFit+'/'+mass+'.0/biasOutput'
              biasPath = biasPath+'/'+'_'.join(['rawText',tev,lepton,'cat'+cat, gen])+'.txt'

              with open(biasPath, 'r') as myFile:
                while (biasMethod not in triggerLine and triggerLine != ''  ):
                  triggerLine = myFile.readline()
                if biasMethod in triggerLine:
                  nameList = [x.strip(',') for x in myFile.readline().split()]
                  tmpIndex = nameList.index(fit)
                  valList = [x.strip(',') for x in myFile.readline().split()]
                  fitValList.append(valList[tmpIndex])
            #if not yellow:
            if all(abs(float(x))<0.21 for x in fitValList):
              fullFitValList.append('\\cellcolor{Yellow}{\\bf '+' \\slash '.join(fitValList)+'}')
              #yellow = True
            else:
              fullFitValList.append(' \\slash '.join(fitValList))
            #else:
            #  fullFitValList.append(' \\slash '.join(fitValList))
          latexFile.write(' & '.join(fullFitValList))
          latexFile.write(' \\\\ \n')
        latexFile.write('  \\hline \n')

    latexFile.write('  \\end{tabular}%\n')
    latexFile.write('  }\n')
    latexFile.write(' \\caption{'+biasMethod+' Bias, '+mass+'.  Columns show results for the various background models used in combined signal+background fits to background-only toys.  The three numbers given for each background fit model correspond to toys generated from either a power law, Laurent polynomial, or exponential-like truth model.  Boldface and yellow highlight is used to indicate the lowest-order functional form that satisfies the "low-bias" criterion: $|\mu(nS/\sigma(nBG))|<=0.2$  }\n')
    latexFile.write(' \\label{tab:pull}\n')
    latexFile.write(' \\end{center}\n')
    latexFile.write('\\end{table}\n')

  if(doLandscape): latexFile.write('\\end{landscape}\n')
  latexFile.write('\\end{document}\n')

  latexFile.close()



if __name__=="__main__":
  doTables()

