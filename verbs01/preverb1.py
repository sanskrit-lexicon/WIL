#-*- coding:utf-8 -*-
"""preverb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.marks = []  # verb markup markers, in order found, if any
  
def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
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
 recs = [r for r in recs if r.cat == 'preverb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d


class Wilverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',line)
  self.L,self.k1,self.k2,self.code,self.mw = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  self.upasargas = []
  self.entry = None
  self.preverbs = []
  self.mwpreverbs = []
  self.mwpreverbs_found = []
  self.mwpreverbs_parse = []

def init_wilverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Wilverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  d[entry.metad['L']]= entry
 # 
 for irec,rec in enumerate(recs):
  L = rec.L
  try:
   entry = d[L]
   rec.entry = entry
   entry.marked = True
  except:
   print('find_entries. bad L=',rec.L)
   print('record # ',irec+1)
   print('  line = ',rec.line)
   exit(1)

def find_upasargas_normalize(u):
 mapping = {
  'sama':'sam',
  'saM':'sam',
  'AN':'A',
  'ut':'ud',
  'nira':'nir',
 }
 if u in mapping:
  return mapping[u]
 return u # no change

def combine_upasargas(u0,v0):
 u = find_upasargas_normalize(u0)
 v = find_upasargas_normalize(v0)
 u1,u2 = (u[0:-1],u[-1])
 v1,v2 = (v[0],v[1:])
 if (u2,v1) in sandhimap:
  w = sandhimap[(u2,v1)]
  if (u,v) == ('sam','pra'):
   return 'sampra'  # sandhimap gives saMpra, but MW uses sampra
  return u1 + w + v2
 return u + v

upasarga_manual = {
'{#ni#} or {#aBi#} and {#ni#}, ':['ni','aBini'],
'{#ut#} or {#sama#} and {#ut#}, To be high or elevated.':['ud','samud'],
'{#vi, apa#}, and {#AN#}, ':['vyapA'],
'{#aBi, vi#}, and {#AN#}, To utter, to pronounce.':['aBivyA'],
'{#sam, aBi, vi#} and {#AN#}, To speak in concert.':['samaBivyA'],
'{#sam, ut#} and {#AN#}, To relate.':['samudA'],
'{#upa, ni, vi#} or {#sam#} the verb is deponent ({#upahnayate#}); also':['upa','ni','vi','sam'],
'{#anu, ava, AN, pari#}, or {#sam#} prefixed, it is deponent, as {#anukrIqate#}, &c. unless {#anu#} requires the accusative case, and the compound':
  ['anu','ava','A','pari','sam']
}

def find_upasargas_line(line):
 # 0.  map the line directly
 if line in upasarga_manual:
  upasargas = upasarga_manual[line]
  return upasargas,'0'
 # 1. {#x#},
 m = re.search(r'^{#([^#,]+)#}[,.]',line)
 if m:
  u1 = m.group(1)
  upasargas = list(map(find_upasargas_normalize,[u1]))
  #print('check1:',u1,upasargas)
  return upasargas,'1'
 # 1a. {#x#} prefixed
 m = re.search(r'^{#([^#,]+)#} prefixed',line)
 if m:
  u1 = m.group(1)
  upasargas = list(map(find_upasargas_normalize,[u1]))
  #print('check1a:',u1,upasargas)
  return upasargas,'1a'
 # 1b. {#x#} ({#y#})
 m = re.search(r'^{#([^#,]+)#} \({#[^#]+#}\)',line)
 if m:
  u1 = m.group(1)
  upasargas = list(map(find_upasargas_normalize,[u1]))
  #print('check1a:',u1,upasargas)
  return upasargas,'1b'
 # 1c. {#x#} VARIOUS
 m = re.search(r'^{#([^#,]+)#}( to | in | implies | if | changed | $)',line)
 if m:
  u1 = m.group(1)
  upasargas = list(map(find_upasargas_normalize,[u1]))
  #print('check1a:',u1,upasargas)
  return upasargas,'1c'
 # 2. {#x#} and {#y#}
 m = re.search(r'^{#([^#,]+)#} and {#([^#,]+)#}[,. ]',line)
 if m:
  u1,u2 = m.group(1),m.group(2)
  u = combine_upasargas(u1,u2)
  upasargas = [u]
  #print('check2:',u1,u2,upasargas)
  return upasargas,'2'
 # 3. {#x#} or {#y#}
 m = re.search(r'^{#([^#,]+)#} or {#([^#,]+)#}[,]',line)
 if m:
  u1 = m.group(1)
  u2 = m.group(2)
  upasargas = list(map(find_upasargas_normalize,[u1,u2]))
  #print('check3:',u1,u2,upasargas)
  return upasargas,'3'
 # 3a. {#x#} or {#y#} prefixed
 m = re.search(r'^{#([^#,]+)#} or {#([^#,]+)#} prefixed',line)
 if m:
  u1 = m.group(1)
  u2 = m.group(2)
  upasargas = list(map(find_upasargas_normalize,[u1,u2]))
  #print('check3:',u1,u2,upasargas)
  return upasargas,'3a'
 # 3b. {#x#} or {#y#} ({#z#})
 m = re.search(r'^{#([^#,]+)#} or {#([^#,]+)#} \({#[^#]+#}',line)
 if m:
  u1 = m.group(1)
  u2 = m.group(2)
  upasargas = list(map(find_upasargas_normalize,[u1,u2]))
  #print('check3:',u1,u2,upasargas)
  return upasargas,'3b'
 # 4. {#x#} or {#y#} or {#z#}
 m = re.search(r'^{#([^#,]+)#} or {#([^#,]+)#} or {#([^#,]+)#}',line)
 if m:
  u1 = m.group(1)
  u2 = m.group(2)
  u3 = m.group(3)
  upasargas = list(map(find_upasargas_normalize,[u1,u2,u3]))
  #print('check4:',u1,u2,u3,upasargas)
  return upasargas,'4'
 print('find_upasargas_line problem:',line)
 return [],'NONE'

class Upasarga(object):
 def __init__(self,upasargas,line,entry):
  self.upasargas = upasargas
  self.line = line
  self.entry = entry

def update_ucodedict(ucodedict,upasargas_line,ucode,line0,entry):
 if ucode not in ucodedict:
  ucodedict[ucode] = []
 ucodedict[ucode].append(Upasarga(upasargas_line,line0,entry))

def write_upasarga_lines(fileout,ucodedict):
 keys = sorted(ucodedict.keys())
 with codecs.open(fileout,"w","utf-8") as f:
  for code in keys:
   recs = ucodedict[code]
   out = '; code = %s, %3d cases'%(code,len(recs))
   outarr = [out]
   for irec,rec in enumerate(recs):
    icase = irec+1
    upasarga_str = ','.join(rec.upasargas)
    line = rec.line
    entry = rec.entry
    L = entry.metad['L']
    k1 = entry.metad['k1']
    out = '%5s:%6s:%10s:%s' %(L,k1,upasarga_str,line)
    if len(out) > 70:
     out = out[0:70] + ' ...'
    outarr.append(out)
   for out in outarr:
    f.write(out + '\n')
 print('upasarga parsing in file',fileout)

def find_upasargas(recs):
 nrec = 0
 nupa = 0
 upad = {}
 ucodedict = {} # for debugging
 for rec in recs:
  entry = rec.entry
  upasargas = []
  lines = entry.datalines
  for iline,line in enumerate(lines):
   m = re.search(r'^<div n="p">[0-9 ]*[wW]ith (.*)$',line)
   if m:
    line0 = m.group(1)
    upasargas_line,ucode = find_upasargas_line(line0)
    upasargas = upasargas+upasargas_line
    update_ucodedict(ucodedict,upasargas_line,ucode,line0,entry)
    for upasarga in upasargas_line:
     if upasarga not in upad:
      upad[upasarga] = 0
     upad[upasarga] = upad[upasarga] + 1
  rec.upasargas = upasargas
  if len(upasargas) > 0:
   nrec = nrec + 1
   nupa = nupa + len(upasargas)
 print(nupa,"upasargas found in",nrec,"entries")
 filetemp = 'temp_wil_upasargas.txt'
 with codecs.open(filetemp,"w","utf-8") as f:
  keys = sorted(upad.keys())
  for upasarga in keys:
   f.write("%4d '%s'\n" %(upad[upasarga],upasarga))
  print(len(keys),"upasargas written to",filetemp)
 file_upasargas='wil_upasarga_lines.txt'
 write_upasarga_lines(file_upasargas,ucodedict)

def non_verb_upasargas(entries):
 nrec = 0
 nupa = 0
 ans = []
 for entry in entries:
  if entry.marked:  # skip verb entries
   continue
  upasargas = []
  lines = entry.datalines
  for iline,line in enumerate(lines):
   m = re.search(u'<div n="p">— {#([a-zA-Z]+)#}',line)
   if m:
    upasarga = m.group(1)
    upasargas.append(upasarga)
  #rec.upasargas = upasargas
  if len(upasargas) > 0:
   nrec = nrec + 1
   nupa = nupa + len(upasargas)
   entry.upasargas = upasargas
   ans.append(entry)

 print(nupa,"upasargas found in",nrec,"non-verb entries")
 fileout = 'preverb1_tempupa.txt'
 with codecs.open(fileout,'w','utf-8') as f:
  for ientry,entry in enumerate(ans):
   L = entry.metad['L']
   k1 = entry.metad['k1']
   upasargas = entry.upasargas
   out = ';; Case %04d: L=%s, k1=%s, #upasargas=%s' %(ientry+1,L,k1,len(upasargas))
   f.write(out+'\n')
  print(len(ans),"records written to",fileout)

sandhimap = {
 ('i','a'):'ya',
 ('i','A'):'yA',
 ('i','i'):'I',
 ('i','I'):'I',
 ('i','u'):'yu',
 ('i','U'):'yU',
 ('i','f'):'yf',
 ('i','F'):'yF',
 ('i','e'):'ye',
 ('i','E'):'yE',
 ('i','o'):'yo',
 ('i','O'):'yO',

 ('u','a'):'va',
 ('u','A'):'vA',
 ('u','i'):'vi',
 ('u','I'):'vI',
 ('u','u'):'U',
 ('u','U'):'U',
 ('u','f'):'vf',
 ('u','F'):'vF',
 ('u','e'):'ve',
 ('u','E'):'vE',
 ('u','o'):'vo',
 ('u','O'):'vO',

 ('a','a'):'A',
 ('a','A'):'A',
 ('A','a'):'A',
 ('A','A'):'A',
 
 ('a','i'):'e',
 ('A','i'):'e',
 ('a','I'):'e',
 ('A','I'):'e',
 
 ('a','u'):'o',
 ('A','u'):'o',
 ('a','U'):'o',
 ('A','U'):'o',
 
 ('a','f'):'Ar',
 ('A','f'):'Ar',
 ('a','e'):'e',
 ('d','s'):'ts',
 ('a','C'):'acC', # pra+Cad = pracCad
 ('i','C'):'icC',
 ('d','q'):'qq',  # ud + qI
 ('d','k'):'tk',
 ('d','K'):'tK',
 ('d','c'):'tc',
 ('d','C'):'tC',
 ('d','w'):'tw',
 ('d','W'):'tW',
 ('d','t'):'tt',
 ('d','T'):'tT',
 ('d','p'):'tp',
 ('d','P'):'tP',
 ('d','s'):'ts',
 ('d','n'):'nn',

 ('i','st'):'izw',
 ('s','h'):'rh', # nis + han -> nirhan
 ('m','s'):'Ms', # sam + saYj -> saMsaYj
 ('m','S'):'MS',
 ('m','k'):'Mk',
 ('m','K'):'MK',
 ('m','c'):'Mc',
 ('m','C'):'MC',
 ('m','w'):'Mw',
 ('m','W'):'MW',
 ('m','t'):'Mt',
 ('m','T'):'MT',
 ('m','p'):'Mp',
 ('m','P'):'MP',

 ('m','v'):'Mv',
 ('m','l'):'Ml',
 ('m','r'):'Mr',
 ('m','y'):'My',
 ('m','n'):'Mn',
 
 ('s','k'):'zk', # nis + kf -> nizkf
 ('s','g'):'rg',
 ('s','G'):'rG',
 ('s','j'):'rj',
 ('s','q'):'rq',
 ('s','d'):'rd',
 ('s','D'):'rD',
 ('s','b'):'rb',
 ('s','B'):'rB',
 ('s','m'):'rm',
 ('s','n'):'rn',
 ('s','y'):'ry',
 ('s','r'):'rr',
 ('s','l'):'rl',
 ('s','v'):'rv',

 ('d','l'):'ll',
 ('d','h'):'dD',
 ('d','S'):'cC',

}
def join_prefix_verb(pfx,root):
 if pfx.endswith('ud') and (root == 'sTA'):
  return pfx[0:-2] + 'ut' + 'TA'  # ud + sTA = utTA
 if (pfx == 'saMpra') and (root in ['nad','nam','naS']):
  pfx = 'sampra'
  root = 'R' + root[1:]
  return pfx + root
 if (pfx == 'pra') and (root == 'nakz'):
  return 'pranakz' # odd, since mw has aBipraRakz
 pfx1,pfx2 = (pfx[0:-1],pfx[-1])
 root1,root2 = (root[0],root[1:])
 if (pfx2,root1) in sandhimap:
  return pfx1 + sandhimap[(pfx2,root1)] + root2
 if len(root) > 1:
  root1,root2 = (root[0:2],root[2:])
  if (pfx2,root1) in sandhimap:
   return pfx1 + sandhimap[(pfx2,root1)] + root2
 if root == 'i':
  if pfx == 'dus':
   return 'duri'
  if pfx == 'nis':
   return 'niri'
 if 'saMpra' in pfx:
  pfx = pfx.replace('saMpra','sampra')
  return pfx + root
 if  pfx.endswith(('pari','pra')) and root.startswith('n'):
  return pfx + 'R' + root[1:]  # pra + nad -> praRad
 if pfx.endswith('nis') and root.startswith(('a','I','u','U')):
  pfx = pfx.replace('nis','nir')
  return pfx + root
 ans = pfx + root
 d = {'duscar':'duScar'}
  
 if ans in d:
  ans = d[ans]
 return ans

mwpreverb_adjustments = {
 'apAYc':'apAc',
 'parAn':'parAR',
 'nisf':'nirf',
 'nisfC':'nirfC',
 'atyarj':'atyfj',
 'nirnI':'nirRI',
 'parAnI':'parARI',
 'paryAnI':'paryARI',
 'pratiparAnI':'pratiparARI',
 'vinirnI':'vinirRI',
 'sampranI':'sampraRI',
 'aByutci':'aByucci',
 'aByujji':'aByujji',
 'niscft':'niScft',
 'nissic':'niHzic',
 'nissiD':'niHziD',
 'sampratisiD':'sampratiziD',
 'nizkzip':'niHkzip',
 'antarcar':'antaScar',
 'niscar':'niScar',
 'protcar':'proccar',
 'viniscar':'viniScar',
 'niscat':'niScat',
 'nisci':'niSci',
 'vinisci':'viniSci',
 'prodhA':'prodDA',
 'antarCid':'antaSCid',
 'anuCid':'anucCid',
 'apotCad':'apocCad',
 'ACad':'AcCad',
 'samACad':'samAcCad',
 'ACid':'AcCid',
 'avACid':'avAcCid',
 'samACid':'samAcCid',
 'ACfd':'AcCfd',
 'anuCo':'anucCo',
 'ACo':'AcCo',
 'nisstan':'niHzwan',
 'vinisstan':'vinizwan',
 'anustu':'anuzwu',
 'anustuB':'anuzwuB',
 'avastamB':'avazwamB',
 'utstamB':'uttamB',
 'paryavastamB':'paryavazwamB',
 'pratyutstamB':'pratyuttamB',
 'aBizwf':'aBistf',
 'nizwf':'nistf',
 'anUtsTA':'anUtTA',
 'upotsTA':'upotTA',
 'nissTA':'niHzWA',
 'protsTA':'protTA',
 'sampratisTA':'sampratizWA',
 'aByarj':'aByfYj',
 'Arj':'ArYj',
 'nyarj':'nyfYj',
 'aByasUy':'aByasUya',
 'samAkarRaya':'samAkarR',
 'acCe':'acCAi',  # mw doesn't show sandhi, but he should!
 'anvinD':'anviD', # mw has both spellings, but digitization only has anviD
 'en':'env',
 'pren':'prenv',
 'pratIn':'pratInv',
 'samin':'saminv',
 'AdaSasy':'AdaSasya',
 'samdaSasya':'saMdaSasya',
 'parisvaYj':'parizvaj',
 'saMparisvaYj':'samparizvaYj',
 'Akuc':'AkuYc',
 'nikuc':'nikuYc',
 'vikuc':'vikuYc',
 'acCagam':'acCAgam',
 'aramgam':'araMgam',
 'AgraT':'AgranT',
 'udgraT':'udgranT',
 'upagraT':'upagranT',
 'nigraT':'nigranT',
 'samudgraT':'samudgranT',
 'anUdji':'anUjji',
 'atinistan':'atinizwan',
 'upadaB':'upadamB',
 'apidfB':'pidfB',
 'uddfh':'uddfMh',
 'anUddfh':'anUddfMh',
 'samdaSasya':'saMdaSasya',
 '':'',
 'ADam':'ADmA',
 'upADam':'upADmA',
 'samADam':'samADmA',
 'udDam':'udDmA',
 'upaDam':'upaDmA',
 'parADam':'parADmA',
 'praDam':'praDmA',
 'tirarDA':'tiroDA',
 'acCanakz':'acCAnakz',
 'pariRand':'parinand',
 'nirnam':'nirRam',
 'pariRft':'parinft',
 'praRft':'pranft',
 'acCanaS':'acCAnaS',
 'paryAnah':'paryARah',
 'nirnij':'nirRij',
 'parinirnij':'parinirRij',
 'acCanI':'acCAnI',
 'acCanu':'acCAnu',
 'nirnud':'nirRud',
 'aBinirnud':'aBinirRud',
 'parAnud':'parARud',
 'sampranud':'sampraRud',
 'udbfh':'udvfh',
 'prabfh':'pravfh',
 'upaprabfh':'upapravfh',
 'aBibfh':'aBivfh',
 'paribfh':'parivfh',
 'aBimaT':'aBimanT',
 'aBivimaT':'aBivimanT',
 'aByatyarj':'aByatyfj',
 'pratisaMkf':'pratisaMskf',
 'pariKaRq':'pariKaRqaya',  # no 'KaRqaya' in mw
 'protcal':'proccal',
 'nirjf':'nirjF',
 'parijf':'parijF',
 'prajf':'prajF',
 'niswaNk':'nizwaNk',
 'nimf':'nimF',
 'acCavac':'acCAvac',
 'acCavaYc':'acCAvaYc',
 'acCavad':'acCAvad',
 'acCavft':'acCAvft',
 'pariSIlaya':'pariSIl',
 'aBiskaB':'aBiskamB',
 'upaskaB':'upaskamB',
 'viskaB':'viskamB',
 'vizwf':'viswf',
 'nissyand':'niHzyand',
 'acCasyand':'acCAsyand',
 'nissyand':'niHsyand',# or niHzyand
 'nissvap':'niHzvap',
 'prodjval':'projjval',
 'praniDA':'praRiDA',  # see mw praRi for Panini list
 'pranipat':'praRipat',
 'tirazkf':'tiraskf',
 'nirkram':'nizkram',
 'nirci':'niSci',
 'vinirci':'viniSci',
 'nirtF':'nistF',
 'udmUl':'unmUla',  # mw denominative
 'nirSvas':'niHSvas',
 'vizwf':'vistf',
 '':'',
 '':'',
 '':'',
 #'':'',xxx

}
def adjust_mwpreverb(preverb,mwdict):
 #if preverb == 'aByasUy':print('adjust_mwpreverb 1',preverb)
 if preverb in mwpreverb_adjustments:
  x = mwpreverb_adjustments[preverb]
  if x in mwdict:
   return x
 #if preverb == 'aByasUy':print('adjust_mwpreverb 2',preverb)
 if preverb in mwdict:
  return preverb # no adjustment needed
 if re.search(r'sa[mM]p',preverb):
  x = preverb.replace('saMp','samp')
  if x in mwdict:
   return x
  x = preverb.replace('samp','saMp')
  if x in mwdict:
   return x
  return preverb
 if re.search(r'.*r.*n$',preverb):  #parAn -> paraR, etc
  x = preverb[0:-1]+'R'
  if x in mwdict:
   return x
 if 'samh' in preverb:
  x = preverb.replace('samh','saMh')
  if x in mwdict:
   return x
 if 'utc' in preverb:
  x = preverb.replace('utc','ucc')
  if x in mwdict:
   return x
 if 'utC' in preverb:
  x = preverb.replace('utC','ucC')
  if x in mwdict:
   return x
 if 'udj' in preverb:
  x = preverb.replace('udj','ujj')
  if x in mwdict:
   return x
 if preverb.endswith('isad'):
  x = re.sub(r'isad$','izad',preverb)
  if x in mwdict:
   return x
 if re.search(r'is',preverb):
  x = re.sub(r'is',r'iz',preverb)
  if x in mwdict:
   return x
 if re.search(r'isT',preverb):
  x = re.sub(r'isT',r'izW',preverb)
  if x in mwdict:
   return x
 if re.search(r'us',preverb):
  x = re.sub(r'us',r'uz',preverb)
  if x in mwdict:
   return x
 if re.search(r'usT',preverb):
  x = re.sub(r'usT',r'uzW',preverb)
  if x in mwdict:
   return x
 if re.search(r'niss',preverb):
  x = re.sub(r'niss',r'niHs',preverb)
  if x in mwdict:
   return x
 if re.search(r'nisS',preverb):
  x = re.sub(r'nisS',r'niHS',preverb)
  if x in mwdict:
   return x
 if re.search(r'niszW',preverb):
  x = re.sub(r'niszW',r'niHzW',preverb)
  if x in mwdict:
   return x
 if re.search(r'nisv',preverb):
  x = re.sub(r'nisv',r'nirv',preverb)
  if x in mwdict:
   return x
 if re.search(r'udm',preverb):
  x = re.sub(r'udm',r'unm',preverb)
  if x in mwdict:
   return x
 if re.search(r'udh',preverb):
  x = re.sub(r'udh',r'udD',preverb)
  if x in mwdict:
   return x
 if re.search(r'sam[gGjJdDbByrlvSzs]',preverb):
  x = re.sub(r'sam([gGjJdDbByrlvSzs])',r'saM\1',preverb)
  if x in mwdict:
   return x
 if re.search(r'antar',preverb):
  x = re.sub(r'antar',r'antaH',preverb)
  if x in mwdict:
   return x
 if preverb.endswith(('kf','df','pf')):
  x = preverb[0:-1]+'F'
  if x in mwdict:
   return x
 return preverb

def join_upasargas(recs,mwpreverbs_dict):
 for rec in recs:
  upasargas = rec.upasargas
  if len(upasargas) == 0:
   continue
  if rec.mw == '?':
   print(len(upasargas),'upasargas, but no mw root',rec.line)
   continue
  
  #mwrec = rec.mwrec
  k1 = rec.k1
  kmw = rec.mw
  rec.mwpreverbs = []
  rec.preverbs = []
  rec.mwpreverbs_found = []
  rec.mwpreverbs_parse = []
  for u in upasargas:
   wil_preverb = join_prefix_verb(u,k1)
   if False and (k1 == 'asUy'):
    print('wil',u,k1,wil_preverb)
   rec.preverbs.append(wil_preverb)
   mw_preverb0 = join_prefix_verb(u,kmw)
   mw_preverb = adjust_mwpreverb(mw_preverb0,mwpreverbs_dict)
   if False and (k1 == 'asUy'):
    print('mw',u,kmw,mw_preverb0,mw_preverb)
   rec.mwpreverbs.append(mw_preverb)
   if mw_preverb in mwpreverbs_dict:
    mwprerec = mwpreverbs_dict[mw_preverb]
    mwprerec.used = True
    rec.mwpreverbs_found.append(True)
    rec.mwpreverbs_parse.append(mwprerec.parse)
   else:
    rec.mwpreverbs_found.append(False)
    rec.mwpreverbs_parse.append(None)

def skipmw_unused(rec):
 if rec.line.endswith(('+kf','+BU')):
  return True
 if rec.k1 == rec.parse.replace('+',''):
  return True
 return False
def write_mw_unused(mwrecs):
 fileout = 'preverb1_temp_mw_unused.txt'
 n = 0
 with codecs.open(fileout,'w','utf-8') as f:
  for rec in mwrecs:
   if not rec.used:
    out = rec.line
    if skipmw_unused(rec):
     continue
    n = n + 1
    f.write(out+'\n')
 print(n,"records written to",fileout)

def yesno(flag):
 if flag:
  return 'yes'
 else:
  return 'no'

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 nyes = 0
 nno = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   upasargas = rec.upasargas
   preverbs = rec.preverbs
   mwpreverbs = rec.mwpreverbs
   mwpreverbs_found = rec.mwpreverbs_found
   mwpreverbs_parse = rec.mwpreverbs_parse
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   code = rec.code
   if rec.mw== '?': #None:
    mw = '?'
   elif rec.mw== k1:
    mw = rec.mw+ ' (same)'
   else:
    mw = rec.mw+ ' (diff)'
   out1 = ';; Case %04d: L=%s, k1=%s, k2=%s, code=%s, #upasargas=%s, mw=%s' %(irec+1,L,k1,k2,code,len(upasargas),mw)
   """
   ## temporary code
 
   if len(upasargas) != 0:
    out1 = 'L=%s, k1=%s'%(L,k1)
    f.write(out1+'\n')
    continue
   continue
   ## end temporary code
   """
   if len(upasargas) == 0:
    f.write(out1+'\n')
    continue
   #add 1 more field to first line
   iyes = len([mwfound for mwfound in mwpreverbs_found if mwfound])
   ino  = len([mwfound for mwfound in mwpreverbs_found if not mwfound])
   out1 = ';; Case %04d: L=%s, k1=%s, k2=%s, code=%s, #upasargas=%s (%s/%s), mw=%s' %(irec+1,L,k1,k2,code,len(upasargas),iyes,ino,mw)
   outarr = []
   outarr.append(out1)
   # one line for each upasarga
   for iupa,upa in enumerate(upasargas):
    icase = iupa + 1
    preverb = preverbs[iupa]
    mwpreverb = mwpreverbs[iupa]
    mwfound = mwpreverbs_found[iupa]
    if mwfound:
     nyes = nyes + 1
     parse = mwpreverbs_parse[iupa]
    else:
     nno = nno + 1
     parse = ''
    outarr.append('%02d %10s %10s %20s %20s %s %s'%(icase,upa,k1,preverb,mwpreverb,yesno(mwfound),parse))
   outarr.append(';')
   for out in outarr:
    f.write(out + '\n')
   n = n + 1
 print(n,"records written to",fileout)
 print(nyes,"mwpreverb spellings found")
 print(nno,"mwpreverb spellings NOT found")

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[3] # wil_verb_filter_map.txt
 filein2 = sys.argv[4] # mwverbs1
 fileout = sys.argv[5] # 
 entries = init_entries(filein)
 dhatus = init_wilverbs(filein1)
 mwrecs,mwdict = init_mwverbs(filein2)  # mw preverbs
 find_entries(dhatus,entries)  # assign entry to each wil verb record
 find_upasargas(dhatus)  # get list of upasargas
 non_verb_upasargas(entries)  # debug logic
 join_upasargas(dhatus,mwdict)
 write(fileout,dhatus,tranout)
 write_mw_unused(mwrecs)
