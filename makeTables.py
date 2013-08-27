#!/usr/bin/env python

import sys

def doTables():

  massList = ['mH120','mH125','mH130','mH135','mH140','mH145','mH150','mH155','mH160']
  leptonList = ['el', 'mu']
  yearList = ['2012']
  genList = ['GaussExp', 'GaussPow', 'SechExp', 'SechPow']
  genListAbbr = ['GE', 'GP', 'SE', 'SP']
  catList = ['0']
  fitList = ['GaussBern3','GaussBern4','GaussBern5']
  doLandscape = False

# get all the txt files from the pull plots, put them in a dictionary (they
# are all uniquely named so you can just key on their names, makes callback
# easy later on in the code
  inputFileDict ={}
  for lepton in leptonList:
    for year in yearList:
      for mass in massList:
        for gen in genList:
          for cat in catList:
            name = lepton+'_'+year+'_'+gen+'_cat'+cat+'_'+mass
            try:
              inputFileDict[name]=open('pullPlotDir/'+lepton+'_'+year+'/'+name+'.txt','r')
            except:
              print 'cannot open','pullPlotDir/'+lepton+'_'+year+'/'+name+'.txt'
              return
  for inFile in inputFileDict.keys():
    print inFile, inputFileDict[inFile]

  latexFile = open('pyTablesNoCat.tex','w')

# start the header
  latexFile.write('\\documentclass[11pt,final]{article}\n')
  latexFile.write('\\usepackage[margin=1in]{geometry}\n')
  latexFile.write('\\usepackage{color, colortbl}\n')
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
    latexFile.write('  \\begin{tabular}{'+'|c'*(len(fitList)+1)+'|}\n')
    latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{~} \\\\ \n')
    latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{{\\bf Type-A Bias, Gaussian turn-on mH='+mass+'}} \\\\ \n')
    latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{~} \\\\ \n')
    for lepton in leptonList:
      for year in yearList:
        latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{c}{~} \\\\ \n')
        latexFile.write('  \\hline \n')
        latexFile.write('  \\multicolumn{'+str(len(fitList)+1)+'}{|c|}{'+year+' '+lepton+'} \\\\ \n')
        latexFile.write('  \\hline \n')
        latexFile.write('  cat. & ')
# we're about to write the header for the individual table, letting it know
# how many fit functions and how many gen functions
        fitListAndGenAbbr = [x +'('+'/'.join(genListAbbr)+')' for x in fitList]
        latexFile.write((' & ').join(fitListAndGenAbbr))
        latexFile.write(' \\\\ \n')
        latexFile.write('  \\hline \n')
        for cat in catList:
          latexFile.write('  '+cat+' & ')
          fullFitValList = []
          yellow = False
          for fit in fitList:
            print fit
            fitValList = []
#pull up all the bias values from the files we stored, run thru them in a complicated way, abuse the 'join' command, drink a lot after you finish
            for gen in genList:
              triggerLine = 'triggerLine'
              name = lepton+'_'+year+'_'+gen+'_cat'+cat+'_'+mass
              while ('typeA' not in triggerLine and triggerLine != ''  ):
                triggerLine = inputFileDict[name].readline()
              if 'typeA' in triggerLine:
                nameList = [x.strip(',') for x in inputFileDict[name].readline().split()]
                tmpIndex = nameList.index(fit)
                valList = [x.strip(',') for x in inputFileDict[name].readline().split()]
                fitValList.append(valList[tmpIndex])
              inputFileDict[name].seek(0)
            if not yellow:
              if all(abs(float(x))<0.2 for x in fitValList):
                fullFitValList.append('\\cellcolor{Yellow}{\\bf '+' \\slash '.join(fitValList)+'}')
                yellow = True
              else:
                fullFitValList.append(' \\slash '.join(fitValList))
            else:
              fullFitValList.append(' \\slash '.join(fitValList))
          latexFile.write(' & '.join(fullFitValList))
          latexFile.write(' \\\\ \n')
        latexFile.write('  \\hline \n')

    latexFile.write('  \\end{tabular}\n')
    latexFile.write(' \\caption{4-Category Type-A Bias, '+mass+', Gaussian turn-on for fit.  Columns show results for the various background models used in combined signal+background fits to background-only toys.  The four numbers given for each background fit model correspond to toys generated from either an gauss*exponential, gauss*power-law, sech*exponential, or sech*power-law truth model.  Boldface and yellow highlight is used to indicate the lowest-order polynomial that satisfies the "low-bias" criterion: $|\mu(nS/\sigma(nBG))|<=0.2$  }\n')
    latexFile.write(' \\label{tab:pull}\n')
    latexFile.write(' \\end{center}\n')
    latexFile.write('\\end{table}\n')

  if(doLandscape): latexFile.write('\\end{landscape}\n')
  latexFile.write('\\end{document}\n')

  latexFile.close()



if __name__=="__main__":
  doTables()

