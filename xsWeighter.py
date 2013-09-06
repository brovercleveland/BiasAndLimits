#!/usr/bin/env python

def LumiXSWeighter(year, lepton, sig, mass, nEvt):
  LumiXSWeight = 0.0
  if(year is '2011'):
    if(sig is 'gg'):
      if(mass is '120'): LumiXSWeight = nEvt/(16.65*0.00111*0.10098*1000)
      if(mass is '125'): LumiXSWeight = nEvt/(15.32*0.00154*0.10098*1000)
      if(mass is '130'): LumiXSWeight = nEvt/(14.16*0.00195*0.10098*1000)
      if(mass is '135'): LumiXSWeight = nEvt/(13.11*0.00227*0.10098*1000)
      if(mass is '140'): LumiXSWeight = nEvt/(12.18*0.00246*0.10098*1000)
      if(mass is '145'): LumiXSWeight = nEvt/(11.33*0.00248*0.10098*1000)
      if(mass is '150'): LumiXSWeight = nEvt/(10.58*0.00231*0.10098*1000)
      if(mass is '155'): LumiXSWeight = nEvt/(9.886*0.00191*0.10098*1000)
      if(mass is '160'): LumiXSWeight = nEvt/(9.202*0.00116*0.10098*1000)

    elif(sig is 'vbf'):
      if(mass is '120'): LumiXSWeight = nEvt/(1.279*0.00111*0.10098*1000)
      if(mass is '125'): LumiXSWeight = nEvt/(1.222*0.00154*0.10098*1000)
      if(mass is '130'): LumiXSWeight = nEvt/(1.168*0.00195*0.10098*1000)
      if(mass is '135'): LumiXSWeight = nEvt/(1.117*0.00227*0.10098*1000)
      if(mass is '140'): LumiXSWeight = nEvt/(1.069*0.00246*0.10098*1000)
      if(mass is '145'): LumiXSWeight = nEvt/(1.023*0.00248*0.10098*1000)
      if(mass is '150'): LumiXSWeight = nEvt/(0.9800*0.00231*0.10098*1000)
      if(mass is '155'): LumiXSWeight = nEvt/(0.9415*0.00191*0.10098*1000)
      if(mass is '160'): LumiXSWeight = nEvt/(0.9043*0.00116*0.10098*1000)

    elif(sig is 'tth'):
      if(mass is '120'): LumiXSWeight = nEvt/(0.0976*0.00111*0.10098*1000)
      if(mass is '125'): LumiXSWeight = nEvt/(0.0863*0.00154*0.10098*1000)
      if(mass is '130'): LumiXSWeight = nEvt/(0.0766*0.00195*0.10098*1000)
      if(mass is '135'): LumiXSWeight = nEvt/(0.0681*0.00227*0.10098*1000)
      if(mass is '140'): LumiXSWeight = nEvt/(0.0607*0.00246*0.10098*1000)
      if(mass is '145'): LumiXSWeight = nEvt/(0.0544*0.00248*0.10098*1000)
      if(mass is '150'): LumiXSWeight = nEvt/(0.0487*0.00231*0.10098*1000)
      if(mass is '155'): LumiXSWeight = nEvt/(0.0438*0.00191*0.10098*1000)
      if(mass is '160'): LumiXSWeight = nEvt/(0.0394*0.00116*0.10098*1000)

    elif(sig is 'wh'):
      if(mass is '120'): LumiXSWeight = nEvt/(0.6561*0.00111*0.10098*1000*(1/0.100974))
      if(mass is '125'): LumiXSWeight = nEvt/(0.5729*0.00154*0.10098*1000*(1/0.100974))
      if(mass is '130'): LumiXSWeight = nEvt/(0.5008*0.00195*0.10098*1000*(1/0.100974))
      if(mass is '135'): LumiXSWeight = nEvt/(0.4390*0.00227*0.10098*1000*(1/0.100974))
      if(mass is '140'): LumiXSWeight = nEvt/(0.3857*0.00246*0.10098*1000*(1/0.100974))
      if(mass is '145'): LumiXSWeight = nEvt/(0.3406*0.00248*0.10098*1000*(1/0.100974))
      if(mass is '150'): LumiXSWeight = nEvt/(0.3001*0.00231*0.10098*1000*(1/0.100974))
      if(mass is '155'): LumiXSWeight = nEvt/(0.2646*0.00191*0.10098*1000*(1/0.100974))
      if(mass is '160'): LumiXSWeight = nEvt/(0.2291*0.00116*0.10098*1000*(1/0.100974))

    elif(sig is 'zh'):
      if(mass is '120'): LumiXSWeight = nEvt/(0.3598*0.00111*0.10098*1000*(1/0.100974))
      if(mass is '125'): LumiXSWeight = nEvt/(0.3158*0.00154*0.10098*1000*(1/0.100974))
      if(mass is '130'): LumiXSWeight = nEvt/(0.2778*0.00195*0.10098*1000*(1/0.100974))
      if(mass is '135'): LumiXSWeight = nEvt/(0.2453*0.00227*0.10098*1000*(1/0.100974))
      if(mass is '140'): LumiXSWeight = nEvt/(0.2172*0.00246*0.10098*1000*(1/0.100974))
      if(mass is '145'): LumiXSWeight = nEvt/(0.1930*0.00248*0.10098*1000*(1/0.100974))
      if(mass is '150'): LumiXSWeight = nEvt/(0.1713*0.00231*0.10098*1000*(1/0.100974))
      if(mass is '155'): LumiXSWeight = nEvt/(0.1525*0.00191*0.10098*1000*(1/0.100974))
      if(mass is '160'): LumiXSWeight = nEvt/(0.1334*0.00116*0.10098*1000*(1/0.100974))

    if (lepton=='mu'): LumiXSWeight = 5.05/(LumiXSWeight)
    if (lepton=='el'): LumiXSWeight = 4.98/(LumiXSWeight)
    if (lepton=='all'): LumiXSWeight = 10.03/(LumiXSWeight)

  elif(year is '2012'):

    if(sig is 'gg'):
      if(mass is '120'): LumiXSWeight = nEvt/(21.13*0.00111*0.10098*1000)
      if(mass is '125'): LumiXSWeight = nEvt/(19.52*0.00154*0.10098*1000)
      if(mass is '130'): LumiXSWeight = nEvt/(18.07*0.00195*0.10098*1000)
      if(mass is '135'): LumiXSWeight = nEvt/(16.79*0.00227*0.10098*1000)
      if(mass is '140'): LumiXSWeight = nEvt/(15.63*0.00246*0.10098*1000)
      if(mass is '145'): LumiXSWeight = nEvt/(14.59*0.00248*0.10098*1000)
      if(mass is '150'): LumiXSWeight = nEvt/(13.65*0.00231*0.10098*1000)
      if(mass is '155'): LumiXSWeight = nEvt/(12.79*0.00191*0.10098*1000)
      if(mass is '160'): LumiXSWeight = nEvt/(11.95*0.00116*0.10098*1000)

    elif(sig is 'vbf'):
      if(mass is '120'): LumiXSWeight = nEvt/(1.649*0.00111*0.10098*1000)
      if(mass is '125'): LumiXSWeight = nEvt/(1.578*0.00154*0.10098*1000)
      if(mass is '130'): LumiXSWeight = nEvt/(1.511*0.00195*0.10098*1000)
      if(mass is '135'): LumiXSWeight = nEvt/(1.448*0.00227*0.10098*1000)
      if(mass is '140'): LumiXSWeight = nEvt/(1.389*0.00246*0.10098*1000)
      if(mass is '145'): LumiXSWeight = nEvt/(1.333*0.00248*0.10098*1000)
      if(mass is '150'): LumiXSWeight = nEvt/(1.280*0.00231*0.10098*1000)
      if(mass is '155'): LumiXSWeight = nEvt/(1.231*0.00191*0.10098*1000)
      if(mass is '160'): LumiXSWeight = nEvt/(1.185*0.00116*0.10098*1000)

    elif(sig is 'tth'):
      if(mass is '120'): LumiXSWeight = nEvt/(0.1470*0.00111*0.10098*1000)
      if(mass is '125'): LumiXSWeight = nEvt/(0.1302*0.00154*0.10098*1000)
      if(mass is '130'): LumiXSWeight = nEvt/(0.1157*0.00195*0.10098*1000)
      if(mass is '135'): LumiXSWeight = nEvt/(0.1031*0.00227*0.10098*1000)
      if(mass is '140'): LumiXSWeight = nEvt/(0.09207*0.00246*0.10098*1000)
      if(mass is '145'): LumiXSWeight = nEvt/(0.08246*0.00248*0.10098*1000)
      if(mass is '150'): LumiXSWeight = nEvt/(0.07403*0.00231*0.10098*1000)
      if(mass is '155'): LumiXSWeight = nEvt/(0.06664*0.00191*0.10098*1000)
      if(mass is '160'): LumiXSWeight = nEvt/(0.06013*0.00116*0.10098*1000)

    elif(sig is 'wh'):
      if(mass is '120'): LumiXSWeight = nEvt/(0.7966*0.00111*0.10098*1000*(1/0.100974))
      if(mass is '125'): LumiXSWeight = nEvt/(0.6966*0.00154*0.10098*1000*(1/0.100974))
      if(mass is '130'): LumiXSWeight = nEvt/(0.6095*0.00195*0.10098*1000*(1/0.100974))
      if(mass is '135'): LumiXSWeight = nEvt/(0.5351*0.00227*0.10098*1000*(1/0.100974))
      if(mass is '140'): LumiXSWeight = nEvt/(0.4713*0.00246*0.10098*1000*(1/0.100974))
      if(mass is '145'): LumiXSWeight = nEvt/(0.4164*0.00248*0.10098*1000*(1/0.100974))
      if(mass is '150'): LumiXSWeight = nEvt/(0.3681*0.00231*0.10098*1000*(1/0.100974))
      if(mass is '155'): LumiXSWeight = nEvt/(0.3252*0.00191*0.10098*1000*(1/0.100974))
      if(mass is '160'): LumiXSWeight = nEvt/(0.2817*0.00116*0.10098*1000*(1/0.100974))

    elif(sig is 'zh'):
      if(mass is '120'): LumiXSWeight = nEvt/(0.4483*0.00111*0.10098*1000*(1/0.100974))
      if(mass is '125'): LumiXSWeight = nEvt/(0.3943*0.00154*0.10098*1000*(1/0.100974))
      if(mass is '130'): LumiXSWeight = nEvt/(0.3473*0.00195*0.10098*1000*(1/0.100974))
      if(mass is '135'): LumiXSWeight = nEvt/(0.3074*0.00227*0.10098*1000*(1/0.100974))
      if(mass is '140'): LumiXSWeight = nEvt/(0.2728*0.00246*0.10098*1000*(1/0.100974))
      if(mass is '145'): LumiXSWeight = nEvt/(0.2424*0.00248*0.10098*1000*(1/0.100974))
      if(mass is '150'): LumiXSWeight = nEvt/(0.2159*0.00231*0.10098*1000*(1/0.100974))
      if(mass is '155'): LumiXSWeight = nEvt/(0.1923*0.00191*0.10098*1000*(1/0.100974))
      if(mass is '160'): LumiXSWeight = nEvt/(0.1687*0.00116*0.10098*1000*(1/0.100974))

    if (lepton=='mu'):
      LumiXSWeight = 19.6175/(LumiXSWeight)
    elif (lepton=='el'):
      LumiXSWeight = 19.6195/(LumiXSWeight)

  return LumiXSWeight


