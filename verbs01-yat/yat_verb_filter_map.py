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

map2mw_special = {
 #yat:mw
 'andola':'andolaya',
 'Andola':'Andolaya',
 'AcCa':'AYC',  #preverb in MW
 # nasal inserts. About 70
 'ab':'amb',
 'aB':'amB',
 'ig':'iNg',
 'id':'ind',
 'iva':'inv',
 'It':'Int',
 'olaqa':'olaRq',
 'kAkza':'kANkz',
 'kAc':'kAYc',
 'kuW':'kuRW',
 'kudr':'kundr',
 'kub':'kumb',
 'kuB':'kumB',
 'guW':'guRW',
 'gudr':'gundr',
 'Gaz':'GaMz',
 'GiR':'GiRR',
 'Cap':'Camp',
 'jiv':'jinv', #? 
 'jug':'juNg',
 'jfBa':'jfmB',
 'wak':'waNk',
 'qab':'qamb',
 'qaB':'qamB',
 'qib':'qimb',
 'qiB':'qimB',
 'Riv':'ninv',
 'Ris':'niMs',
 'tag':'taNg',
 'tatr':'tantraya',
 'tad':'tand',
 'tub':'tumb',
 'trak':'traNk',
 'trag':'traNg',
 'trad':'trand',
 'triK':'triNK',
 'tvag':'tvaNg',
 'dav':'danv',
 'daS':'daMS',
 'diBa':'dimB',
 'drAkz':'drANkz',
 'DmAkz':'DmANkz',
 'DrAkz':'DrANkz',
 'DvAkza':'DvANkz',
 'pij':'piYj',
 'mak':'maNk',
 'rig':'riNg',
 'riv':'riRv',
 'vug':'vuNg',
 'vuD':'vunD',
 'Saq':'SaRq',
 'SiKa':'SiNK',
 'SiG':'SiNG',
 'Sij':'SiYj',
 'Sraka':'SraNk',
 'Sraga':'SraNg',
 'Slak':'SlaNk',
 'Slag':'SlaNg',
 'Svaka':'SvaNk',
 'Svaga':'SvaNg',
 'Svida':'Svind',
 'zwaB':'stamB',
 'skada':'skand',
 'skud':'skund',
 'spad':'spand',
 'sPaqa':'sPaRq',
 'srak':'sraNk',
 'svaga':'svaNg',
 'hiqa':'hiRq',
 'hiv':'hinv',
 'his':'hiMs',
 'caq':'caRq',
 'cub':'cumb',
 'Div':'Dinv',
 'paq':'paRq',
 'piq':'piRq',
 'piv':'pinv',
 'Baq':'BaRq',
 'Bad':'Band',
 'Buq':'BuRq',
 'mag':'maNg',
 'maG':'maNG',
 'maq':'maRq',
 'matr':'mantr',
 'masj':'majj',
 'mAkz':'mANkz',
 'miv':'minv',
 'muW':'muRW',
 'mruMc':'mruYc',
 'yatr':'yantr',
 'yug':'yuNg',
 'rab':'ramb',
 'rav':'ramb',  #v/b
 'lab':'lamb',
 'larvv':'larb', #v/b
 'lAcCa':'lAYC',
 'liga':'liNg',
 'luc':'luYc',
 'luj':'luYj',
 'luT':'lunT',
 'lub':'lumb',
 'vag':'vaNg',
 'vaG':'vaNG',
 'vaq':'vaRq',
 'vAkz':'vANkz',
 'vAcC':'vAYC',
 'vuw':'vuRw',  #? not marked as 'i'.
 'kap':'kamp',
 'garD':'gfD', # causal
 'Carda':'Cfd',  # causal
 'jurva':'jUrv',  # u/U
 'daridrA':'drA', # intensive
 'mAT':'mAnT',
 'kaRqU':'kaRqUya',
 'kuwumb':'kuwumbaya',
 'kusm':'kusmaya',
 'kfb':'kF',
 'ket':'ketaya',
 'gudra':'gundr',
 'gom':'gomaya',
 'GiMR':'GiRR',
 'caqa':'caRq',
 'QuQ':'QuRQ',
 'tucC':'tucCaya',
 'tutT':'tutTaya',
 'duHK':'duHKaya',
 'pIv':'pIva',
 'puzp':'puzpya',

 # -------------------------
 'uYJ':'ujJ',  
 'udJ':'ujJ',
 'Sur':'SUr',
 'pUr':'pF',
 'durbba':'durv',
 'Una':'Unaya',
 'kakva':'kaK',  # yat mis-spelling?
 'kAla':'kAlaya',
 'kuwumba':'kuwumbaya',
 'kfba':'kF',  #?
 'kfvi':'kfv', #?
 'kzida':'kzvid',  # or kzviq
 'Ceda':'Cid',  # causal
 'jYap':'jYA', # causal
 'Jarj':'JarJ',  # yat also has JarJ
 'trA':'trE',
 'durvva':'durv',
 'DrU':'Dru',  # also, Dru
 'nf':'nF',
 'puzpa':'puzpya',  # yat shows 4th cl. 'puzpati', which are inconsistent.
 'bana':'van',  # yat has both. MW only van
 'bah':'baMh',
 'bahl':'balh',
 'byuza':'byus',
 'BAj':'Baj', # causal.
 'Brasja':'Brajj',
 'meqf':'meq',
 'lasj':'lajj',
 'vusa':'bus',  # yat has b/v-usa, mw only bus
 'zaR':'san',
 'zarjja':'sarj',
 'zasja':'sajj',
 'zasti':'sas',
 'zwaka':'stak',
 'zwan':'stan',
 'zwiG':'stiG',
 'zwip':'stip',
 'zwim':'stim',
 'zwIm':'stIm',
 'zwu':'stu',
 'zwuc':'stuc',
 'zwuB':'stuB',
 'zwUpa':'stUp',
 'zwfkza':'stfkz',
 'zwfha':'stfh',
 'zwFh':'stFh',
 'zwep':'step',
 'zwE':'stE',
 'zwyE':'styE',
 'zWag':'sTag',
 'zWal':'sTal',
 'zWA':'sTA',
 'zRasa':'snas',
 'zRA':'snA',
 'zRih':'snih',
 'zRu':'snu',
 'zRuc':'snuc',
 'zRus':'snus',
 'zRuh':'snuh',
 'zRE':'snE',
 'zvartta':'svart',
 'saNgrAma':'saMgrAm',
 'spardDa':'sparD',
 'hroq':'hrOq', # o/O ?
 'vara':'vf',  # causal
 'varza':'vfz',  # also vfza -> vfz
 'zwam':'stam',
 'sbf':'sbF',   # f/F
 'Buqa':'BuRq',
 'mlecCa':'mleC',
 'laG':'laNG',
 'larva':'larb', #v/b
 'vAC':'vAYC',
 'saNketa':'saMketaya',
 'stfMha':'stfh',   # yat also has stfha
 '':'',
 '':'',
 '':'',
 '':'',
 '':'',
 '':'',
 '':'',
 '':'',

 
}
"""
 YAT corrections
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
