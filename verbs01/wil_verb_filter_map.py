#-*- coding:utf-8 -*-
"""wil_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Wilverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
  self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  self.mw = None
 
def init_wilverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Wilverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

map2mw_special = {
 #wil:mw
 'andola':'andolaya',
 'Andola':'Andolaya',
 'AcCa':'AYC',  #preverb in MW
 # nasal inserts. About 70
 'aba':'amb',
 'aBa':'amB',
 'iga':'iNg',
 'ida':'ind',
 'iva':'inv',
 'Ita':'Int',
 'olaqa':'olaRq',
 'kAkza':'kANkz',
 'kAca':'kAYc',
 'kuWa':'kuRW',
 'kudra':'kundr',
 'kuba':'kumb',
 'kuBa':'kumB',
 'guWa':'guRW',
 'gudra':'gundr',
 'Gaza':'GaMz',
 'GiRa':'GiRR',
 'Capa':'Camp',
 'jiva':'jinv', #? 
 'juga':'juNg',
 'jfBa':'jfmB',
 'waka':'waNk',
 'qaba':'qamb',
 'qaBa':'qamB',
 'qiba':'qimb',
 'qiBa':'qimB',
 'Riva':'ninv',
 'Risa':'niMs',
 'taga':'taNg',
 'tatra':'tantraya',
 'tada':'tand',
 'tuba':'tumb',
 'traka':'traNk',
 'traga':'traNg',
 'trada':'trand',
 'triKa':'triNK',
 'tvaga':'tvaNg',
 'dava':'danv',
 'daSa':'daMS',
 'diBa':'dimB',
 'drAkza':'drANkz',
 'DmAkza':'DmANkz',
 'DrAkza':'DrANkz',
 'DvAkza':'DvANkz',
 'pija':'piYj',
 'maka':'maNk',
 'riga':'riNg',
 'riva':'riRv',
 'vuga':'vuNg',
 'vuDa':'vunD',
 'Saqa':'SaRq',
 'SiKa':'SiNK',
 'SiGa':'SiNG',
 'Sija':'SiYj',
 'Sraka':'SraNk',
 'Sraga':'SraNg',
 'Slaka':'SlaNk',
 'Slaga':'SlaNg',
 'Svaka':'SvaNk',
 'Svaga':'SvaNg',
 'Svida':'Svind',
 'zwaBa':'stamB',
 'skada':'skand',
 'skuda':'skund',
 'spada':'spand',
 'sPaqa':'sPaRq',
 'sraka':'sraNk',
 'svaga':'svaNg',
 'hiqa':'hiRq',
 'hiva':'hinv',
 'hisa':'hiMs',
 'caqa':'caRq',
 'cuba':'cumb',
 'Diva':'Dinv',
 'paqa':'paRq',
 'piqa':'piRq',
 'piva':'pinv',
 'Baqa':'BaRq',
 'Bada':'Band',
 'Buqa':'BuRq',
 'maga':'maNg',
 'maGa':'maNG',
 'maqa':'maRq',
 'matra':'mantr',
 'masja':'majj',
 'mAkza':'mANkz',
 'miva':'minv',
 'muWa':'muRW',
 'mruMca':'mruYc',
 'yatra':'yantr',
 'yuga':'yuNg',
 'raba':'ramb',
 'rava':'ramb',  #v/b
 'laba':'lamb',
 'larvva':'larb', #v/b
 'lAcCa':'lAYC',
 'liga':'liNg',
 'luca':'luYc',
 'luja':'luYj',
 'luTa':'lunT',
 'luba':'lumb',
 'vaga':'vaNg',
 'vaGa':'vaNG',
 'vaqa':'vaRq',
 'vAkza':'vANkz',
 'vAcCa':'vAYC',
 'vuwa':'vuRw',  #? not marked as 'i'.
 'kapa':'kamp',
 'garDa':'gfD', # causal
 'Carda':'Cfd',  # causal
 'jurva':'jUrv',  # u/U
 'daridrA':'drA', # intensive
 'mATa':'mAnT',
 '':'',

 # -------------------------
 'uYJa':'ujJ',  
 'udJa':'ujJ',
 'Sura':'SUr',
 'pUra':'pF',
 'durvva':'durv',
 'Una':'Unaya',
 'kakva':'kaK',  # wil mis-spelling?
 'kAla':'kAlaya',
 'kuwumba':'kuwumbaya',
 'kfba':'kF',  #?
 'kfvi':'kfv', #?
 'kzida':'kzvid',  # or kzviq
 'Ceda':'Cid',  # causal
 'jYapa':'jYA', # causal
 'Jarja':'JarJ',  # wil also has JarJ
 'trA':'trE',
 'durvva':'durv',
 'DrU':'Dru',  # also, Dru
 'nf':'nF',
 'puzpa':'puzpya',  # wil shows 4th cl. 'puzpati', which are inconsistent.
 'bana':'van',  # wil has both. MW only van
 'bahi':'baMh',
 'bahla':'balh',
 'byuza':'byus',
 'BAja':'Baj', # causal.
 'Brasja':'Brajj',
 'meqf':'meq',
 'lasja':'lajj',
 'vusa':'bus',  # wil has b/v-usa, mw only bus
 'zaRa':'san',
 'zarjja':'sarj',
 'zasja':'sajj',
 'zasti':'sas',
 'zwaka':'stak',
 'zwana':'stan',
 'zwiGa':'stiG',
 'zwipa':'stip',
 'zwima':'stim',
 'zwIma':'stIm',
 'zwu':'stu',
 'zwuca':'stuc',
 'zwuBa':'stuB',
 'zwUpa':'stUp',
 'zwfkza':'stfkz',
 'zwfha':'stfh',
 'zwFha':'stFh',
 'zwepa':'step',
 'zwE':'stE',
 'zwyE':'styE',
 'zWaga':'sTag',
 'zWala':'sTal',
 'zWA':'sTA',
 'zRasa':'snas',
 'zRA':'snA',
 'zRiha':'snih',
 'zRu':'snu',
 'zRuca':'snuc',
 'zRusa':'snus',
 'zRuha':'snuh',
 'zRE':'snE',
 'zvartta':'svart',
 'saNgrAma':'saMgrAm',
 'spardDa':'sparD',
 'hroqa':'hrOq', # o/O ?
 'vara':'vf',  # causal
 'varza':'vfz',  # also vfza -> vfz
 'zwama':'stam',
 'sbf':'sbF',   # f/F
 '':'',
 '':'',

 
}
"""
 WIL corrections
"""
def map2mw(d,k1):
 if k1 in map2mw_special:
  return map2mw_special[k1]
 if k1 in d:
  return k1
 ans = '?'

 if k1.endswith('a'):
  k = k1[0:-1] # remove final 'a'
  if k in d:
   return k
  k2 = k.replace('cC','C')
  if k2 in d:
   return k2
  k2 = re.sub(r'r(.)\1',r'r\1',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^R','n',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^z','s',k)
  if k2 in d:
   return k2
  k2 = k1 + 'ya'
  if k2 in d:
   return k2

 else:
  k = k1
  k2 = k.replace('cC','C')
  if k2 in d:
   return k2
  k2 = re.sub(r'r(.)\1',r'r\1',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^R','n',k)
  if k2 in d:
   return k2
  k2 = re.sub(r'^z','s',k)
  if k2 in d:
   return k2

 return ans

def wilmap(recs,mwd):

 for rec in recs:
  # try mw spelling directly
  rec.mw = map2mw(mwd,rec.k1)


def write(fileout,recs):
 n = 0
 nomw = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add mw
   out = '%s, mw=%s' %(line,rec.mw)
   f.write(out + '\n')
   if rec.mw =='?':
    nomw = nomw + 1
 print(n,"records written to",fileout)
 print(nomw,"verb have no mw match")
if __name__=="__main__": 
 filein = sys.argv[1] #  wil_verb_filter.txt
 filein1 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_wilverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)
 wilmap(recs,mwverbsd)
 write(fileout,recs)
