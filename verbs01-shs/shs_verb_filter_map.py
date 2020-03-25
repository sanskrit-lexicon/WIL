#-*- coding:utf-8 -*-
"""yat_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Yatverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
  self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  self.mw = None
  #if self.k1 == 'kunT':
  # print('Yatverb:',line)

def init_yatverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Yatverb(x) for x in f if x.startswith(';; Case')]
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

map2mw_special_shs = {
 'andola':'andolaya',
 'aba':'amb',
 'aBa':'amB',
 'AcCa':'AYC',
 'Andola':'Andolaya',
 'iga':'iNg',
 'ida':'ind',
 'iva':'inv',
 'Ita':'Int',
 'uYJa':'ujJ',
 'udJa':'ujJ',
 'Una':'Unaya',
 'olaqa':'olaRq',
 'kakva':'kaK',
 'kapa':'kamp',
 'kAkza':'kANkz',
 'kAca':'kAYc',
 'kAla':'kAlaya',
 'kuwumba':'kuwumbaya',
 'kuWa':'kuRW',
 'kudra':'kundr',
 'kuba':'kumb',
 'kuBa':'kumB',
 'kfvi':'kfv',
 'kzida':'kzvid',
 'garDa':'gfD',
 'guWa':'guRW',
 'gudra':'gundr',
 'Gaza':'GaMz',
 'GiRa':'GiRR',
 'caqa':'caRq',
 'cuba':'cumb',
 'Capa':'Camp',
 'Carda':'Cfd',
 'Ceda':'Cid',
 'jiva':'jinv',
 'juga':'juNg',
 'jurva':'jUrv',
 'jfBa':'jfmB',
 'jYapa':'jYA',
 'Jarja':'JarJ',
 'waka':'waNk',
 'qaba':'qamb',
 'qaBa':'qamB',
 'qiba':'qimb',
 'qiBa':'qimB',
 'Riva':'ninv',
 'Risa':'niMs',
 'taga':'taNg',
 'tatra':'tantraya',
 'tad':'tand',
 'tuba':'tumb',
 'traka':'traNk',
 'traga':'traNg',
 'trada':'trand',
 'trA':'trE',
 'triKa':'triNK',
 'tvaga':'tvaNg',
 'daridrA':'drA',
 'dava':'danv',
 'daSa':'daMS',
 'diBa':'dimB',
 'durba':'durv',
 'drAkza':'drANkz',
 'Diva':'Dinv',
 'DmAkza':'DmANkz',
 'DrAkza':'DrANkz',
 'DrU':'Dru',
 'DvAkza':'DvANkz',
 'nf':'nF',
 'paqa':'paRq',
 'pija':'piYj',
 'piqa':'piRq',
 'piva':'pinv',
 'puzpa':'puzpya',
 'pUra':'pF',
 'bana':'van',
 'bahla':'balh',
 'byuz':'byus',
 'Baq':'BaRq',
 'Bad':'Band',
 'BAj':'Baj',
 'Buqa':'BuRq',
 'BranS':'BraMS',
 'Brasj':'Brajj',
 'mak':'maNk',
 'mag':'maNg',
 'maG':'maNG',
 'maq':'maRq',
 'matr':'mantr',
 'manj':'maYj',
 'masj':'majj',
 'mAkz':'mANkz',
 'mAT':'mAnT',
 'miva':'minv',
 'muW':'muRW',
 'mUtr':'mUtraya',
 'yatr':'yantr',
 'yug':'yuNg',
 'rab':'ramb',
 'rav':'ramb',
 'rig':'riNg',
 'riv':'riRv',
 'laG':'laNG',
 'lab':'lamb',
 'larvv':'larb',
 'lasj':'lajj',
 'lAcC':'lAYC',
 'lig':'liNg',
 'luc':'luYc',
 'luj':'luYj',
 'luT':'lunT',
 'lub':'lumb',
 'vag':'vaNg',
 'vaG':'vaNG',
 'vaq':'vaRq',
 'var':'vf',
 'vardD':'varD',
 'varza':'vfz',
 'valyul':'valyula',
 'vAkz':'vANkz',
 'vAcC':'vAYC',
 'vug':'vuNg',
 'vuw':'vuRw',
 'vuD':'vunD',
 'vus':'bus',
 'Saq':'SaRq',
 'SarD':'SfD',
 'SiK':'SiNK',
 'SiG':'SiNG',
 'Sij':'SiYj',
 'Sur':'SUr',
 'Srak':'SraNk',
 'Srag':'SraNg',
 'Slak':'SlaNk',
 'Slag':'SlaNg',
 'Svak':'SvaNk',
 'Svag':'SvaNg',
 'Svid':'Svind',
 'Svf':'SvF',
 'zaR':'san',
 'zarjj':'sarj',
 'zarD':'sfD',
 'zasj':'sajj',
 'zast':'sas',
 'zwak':'stak',
 'zwan':'stan',
 'zwaB':'stamB',
 'zwam':'stam',
 'zwiD':'sTiG',
 'zwip':'stip',
 'zwim':'stim',
 'zwIm':'stIm',
 'zwu':'stu',
 'zwuc':'stuc',
 'zwuB':'stuB',
 'zwUp':'stUp',
 'zwfkz':'stfkz',
 'zwfh':'stfh',
 'zwFh':'stFh',
 'zwep':'step',
 'zwE':'stE',
 'zwyE':'styE',
 'zWag':'sTag',
 'zWal':'sTal',
 'zWA':'sTA',
 'zRas':'snas',
 'zRA':'snA',
 'zRih':'snih',
 'zRu':'snu',
 'zRuc':'snuc',
 'zRus':'snus',
 'zRuh':'snuh',
 'zRE':'snE',
 'zvartta':'svart',
 'saNketa':'saMketaya',
 'saNgrAma':'saMgrAm',
 'skad':'skand',
 'skud':'skund',
 'stfMha':'stfh',
 'spad':'spand',
 'spardD':'sparD',
 'sPaq':'sPaRq',
 'srak':'sraNk',
 'svag':'svaNg',
 'svartt':'svart',
 'svurcC':'svUrC',
 'hiq':'hiRq',
 'hillol':'hillolaya',
 'hiv':'hinv',
 'his':'hiMs',
 'hroq':'hrOq',
}
def map2mw(d,k1):
 """
 if k1 in yat_map2mw_special:
  ans = yat_map2mw_special[k1]
  print('using yates mapping:',k1,ans)
  return ans
 if k1 in wil_map2mw_special:
  ans = wil_map2mw_special[k1]
  print('using wilson mapping:',k1,ans)
  return ans
 if k1 in shs_map2mw_special:
  ans = shs_map2mw_special[k1]
  print('using shs mapping:',k1,ans)
  return ans
 """
 if k1 in map2mw_special_shs:
  ans = map2mw_special_shs[k1]
  return ans

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

def yatmap(recs,mwd):

 for rec in recs:
  # try mw spelling directly
  rec.mw = map2mw(mwd,rec.k1)
  #if rec.k1 == 'kunT':
  # print('check:',rec.k1,rec.mw)

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
 filein = sys.argv[1] #  yat_verb_filter.txt
 filein1 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_yatverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)
 yatmap(recs,mwverbsd)
 write(fileout,recs)
