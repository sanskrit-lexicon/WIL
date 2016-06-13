# coding=utf-8
"""
 step2/wil_mw.py  Feb 19, 2015
 Reads Wilson roots and MW roots and aims to find, for each
 Wilson root, the corresponding MW root.
 Wilson roots are from wil_rdot.txt.
 MW roots are from and verb_step0a.txt
 
 The format of the output is inspired by corr6_roots.txt
 
 python wil_mw.py ../wil_rdot.txt ../verb_step0a.txt corr6-roots.txt wil_mw.txt wil_mw_prob.txt

  Note: corr6-roots is used as a 'last resort':  it has some correspondences
    developed by Matthias and Peter in 2011.
 June 13, 2016.  There are in fact instances of this 'last resort' being
    taken.
 Thus, we remove 'corr6-roots.txt' from the inputs of the program. The usage is
 now

 python wil_mw.py ../wil_rdot.txt ../verb_step0a.txt wil_mw.txt wil_mw_prob.txt

  TODO:  
   1. use only cases of verb_step0a.txt where type=V or N
      This will (correctly) exclude MW Dana
   2. Possibly associate multiple MW with one Wilson. Examples:
      Jala <-> jala, jal
      Pulla <-> Pulla, Pull
      skaBa <-> skaB, skamB
   3. Associate (by 'force') laNG (not laGaya) with laGa
"""
import sys, re,codecs

class Counter(dict):
 def __init__(self):
  self.d = {}
 def update(self,l):
  for x in l:
   if not (x in self.d):
    self.d[x]=0
   self.d[x] = self.d[x] + 1


class Step0a(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  self.wilused = [] # wilson roots to which this corresponds
  try:
   (self.key1,self.L,self.H,self.type,self.key2,self.detail)=re.split(r':',line)
  except:
   print "Step0a error\n",line
   exit(1)

class Wil(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'<key1>(.*?)</key1>',line)
  if not m:
   print "Wil error at line=\n",line
   exit(1)
  self.wilkey = m.group(1)
  self.mwkey = None

mw_nasal_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',  # homorganic
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m',
 'y':'','r':'','l':'','v':'n',
 'S':'M','z':'M','s':'M','h':'M'
}
consonant_list = mw_nasal_data.keys()
consonant_string = ''.join(consonant_list)

def mw_nasal(c):
 """ return homorganic nasal for consonant 'c' if possible by mw_nasal_data,
   Otherwise, return empty string
 """
 if c in mw_nasal_data:
  return mw_nasal_data[c]
 else:
  return ''

def match_simple(wilkey,step0dict):
 """match returns a pair (reason,mwkey)
    where mwkey is the MW verb associated with wilkey,
    and reason is a string indicating the method of association.
    If no match is found, reason is None and mwkey is None
 """
 if wilkey in step0dict:
  # root is in MW with same spelling
  return ('ROOT',wilkey)
 if wilkey.endswith('a'):
  # Try dropping final 'a'
  mwkey = wilkey[0:-1]
  if mwkey in step0dict:
   #Wilson spelling has 'anubanDa' suffix 'a'
   return ('SPa-ROOT',mwkey)
  # Try replacing final 'a' with 'aya' (andola <-> andolaya)
  mwkey = "%s%s" %(wilkey[0:-1],'aya')
  if mwkey in step0dict:
   #Wilson spelling has 'anubanDa' suffix 'a'
   return ('SPb-ROOT',mwkey)
  # if wilkey has 'cC', try 'C' in MW
  if 'cC' in wilkey:
   mwkey = re.sub(r'cC','C',wilkey[0:-1])
   if mwkey in step0dict:
    #Wilson spelling has 'anubanDa' suffix 'a', and 'cC'
    return ('SPc-ROOT',mwkey)
 # return failure
 return (None,None)

def match(wilkey,step0dict):
 """match returns a pair (reason,mwkey)
    where mwkey is the MW verb associated with wilkey,
    and reason is a string indicating the method of association.
    If no match is found, reason is None and mwkey is None
 """
 (reason,mwkey) = match_simple(wilkey,step0dict)
 if reason:
  return (reason,mwkey)

 # WIlson usually doubles consonants after 'r'
 wilkey1 = re.sub(r'[r](.)\1',r'r\1',wilkey)
 if wilkey1 != wilkey: 
  (reason1,mwkey) = match_simple(wilkey1,step0dict)
  if reason1:
   reason = '%s-r'%reason1
   return (reason,mwkey)
 # similarly for rdD <-> rD
 if 'rdD' in wilkey:
  wilkey1 = re.sub(r'rdD',r'rD',wilkey)
  (reason1,mwkey) = match_simple(wilkey1,step0dict)
  if reason1:
   reason = '%s-rdD'%reason1
   return (reason,mwkey)

 # Feb 21, 2015 if wilkey has 'sj', try 'jj' in MW
 if 'sj' in wilkey:
  wilkey1 = re.sub(r'sj',r'jj',wilkey)
  (reason1,mwkey) = match_simple(wilkey1,step0dict)
  if reason1:
   reason = '%s-sj'%reason1
   return (reason,mwkey)

 # Feb 19. If root starts with 'z', try search with 
 #   that 'z' replaced by 's'  (zw -> st, zW -> sT)
 if wilkey.startswith('z'):
  if wilkey.startswith('zw'):
   wilkey1 = re.sub(r'^zw','st',wilkey)
  elif wilkey.startswith('zW'):
   wilkey1 = re.sub(r'^zW','sT',wilkey)
  elif wilkey.startswith('zR'):
   wilkey1 = re.sub(r'^zR','sn',wilkey)
  else:
   wilkey1 = re.sub(r'^z','s',wilkey)
   if 'rtt' in wilkey1: # zvartta -> svartta -> svarta. Feb 21, 2015
    wilkey1 = re.sub(r'rtt','rt',wilkey1)
  (reason1,mwkey) = match_simple(wilkey1,step0dict)
  if reason1:
   reason = 'z-%s'%reason1
   return (reason,mwkey)
 # Feb 21. saN <-> saM
 if wilkey.startswith('saN'):
  wilkey1 = re.sub(r'^saN','saM',wilkey)
  (reason1,mwkey) = match_simple(wilkey1,step0dict)
  if reason1:
   reason = 'saN-%s'%reason1
   return (reason,mwkey)

 # 
 # Feb 19. If root starts with 'R', try 
 #   try search with that 'R' replaced by 'n'
 if wilkey.startswith('R'):
  wilkey1 = re.sub(r'^R','n',wilkey)
  (reason1,mwkey) = match_simple(wilkey1,step0dict)
  if reason1:
   reason = 'R-%s' % reason1
   return (reason,mwkey)

 # Feb 19.  Try with an inserted nasal
 if wilkey.endswith('a'):
  wilkey1 = wilkey[0:-1] # drop the final 'a'
  consonant_re = '^(.*?)([%s]+)$' % consonant_string
  m = re.search(consonant_re,wilkey1)
  start = m.group(1)
  cons = m.group(2)
  nasal = mw_nasal(cons[0]) # find corresponding nasal used by MW.
  wilkey2 = "%s%s%s%s" %(start,nasal,cons,'a') # key with inserted nasal
  (reason1,mwkey) = match_simple(wilkey2,step0dict)
  if reason1:
   reason = '%s-nasal' % reason1
   return (reason,mwkey)
 # Feb 
 # Feb 21. Wilson root is causal of an MW root
 causals = {'garDa':'gfD','Carda':'Cfd','Ceda':'Cid',
  'jYapa':'jYA', 'BAja':'Baj', 
   'vara':'vf' # vf-2
 }
 if wilkey in causals:
  mwkey = causals[wilkey]
  if mwkey in step0dict: # internal consistency check
   reason = 'Causal'
   return (reason,mwkey)

 # Feb 21. Wilson root is intensive of an MW root
 intensives={'daridrA':'drA'}
 if wilkey in intensives:
  mwkey = intensives[wilkey]
  if mwkey in step0dict: # internal consistency check
   reason = 'Intensive'
   return (reason,mwkey)

 # Feb 21. Likely, but not clear by a rule
 likelys = {
  'uYJa':'ujJ',
  'udJa':'ujJ',
  'uvja':'ubj',
  'Riva':'ninv',
  'riva':'riRv',
  'Risa':'niMs',
  'zaRa':'san',
  'trA':'trE',
  'durbba':'durv',
  'larvva':'larb',
  'meqf':'meq',
  'mruMca':'mruYc',
  'SvF':'svF',
  'zarjja':'sarj',
  'zasja':'sajj',
  'varza':'vfz',
  'bahi':'baMh',
  'bahla':'balh',
  'byuza':'vyuz',
  'rava':'ramb',
  'SuRa':'Sun',
  'Sura':'SUr',
  'zasti':'sas',
  'zwupa':'stUp',
  'sbf':'sbF'
  }
 if wilkey in likelys:
  mwkey = likelys[wilkey]
  if mwkey in step0dict: # internal consistency check
   reason = 'Likely'
   return (reason,mwkey)

 probables = {
  'kfba':'kfv',
  'kfvi':'kfv',
  'kzida':'kzvid',
  'tUra':'tur',
  'DrU':'Dru',
  'nf':'nF',
  'stfMha':'stfh',
  'hroqa':'hruq',
  'kUna':'kUR',
  'DUkza':'Dukz',
  'bana':'van',
  'vfca':'vfj',
  'zwaga':'sTag',
  'jurva':'jUrv',
  'qiba':'qip'
 }
 if wilkey in probables:
  mwkey = probables[wilkey]
  if mwkey in step0dict: # internal consistency check
   reason = 'Probable'
   return (reason,mwkey)


 return (None,None)

def main(filein,filein1,fileout,fileout1):
 # read verb_step0a.txt into array of records
 with codecs.open(filein1,'r') as f:
  step0arecs= [Step0a(line) for line in f]
 print len(step0arecs),"records read from",filein1
 # Feb 19, 2015.  Exclude cases where type is not V or N
 # F3b 23, 2015. Leave
 #step0arecs = [x for x in step0arecs if (x.type in ['V','N'])]
 #print len(step0arecs)," V,N records retained from step0a"

 # read wil_rdot.txt into array of records
 with codecs.open(filein,'r','utf-8') as f:
  wilrecs= [Wil(line) for line in f]
 print len(wilrecs),"records read from",filein

 # make dictionary from step0arecs, with key = MW key,
 # and value a list (usually of length 1) of the records of step0a
 # with the key
 d = {}
 for r in step0arecs:
  key = r.key1
  if key not in d:
   d[key]=[]
  d[key].append(r)

 # generate output
 f = codecs.open(fileout,"w","utf-8")
 f1 = codecs.open(fileout1,"w","utf-8")
 nout = 0
 nout1 = 0
 # initialize counter of reaons for matches
 reason_counter=Counter()
 for wilrec in wilrecs:
  wilkey = wilrec.wilkey
  (reason,mwkey) = match(wilkey,d)
  reason_counter.update([reason])
  if reason:
   out = "<c>%s</c> <wil>%s</wil> <mw>%s</mw>" %(reason,wilkey,mwkey)
   f.write("%s\n" % out)
   nout = nout + 1
   # Feb 13, 2015.  Update wilused for all step0a records
   if mwkey in d:
    for step0arec in d[mwkey]:
     step0arec.wilused.append(wilkey)
  else:
   nout1 = nout1 + 1
   out = "%03d %s" %(nout1,wilkey)
   f1.write("%s\n" % out)
   f1.write("%s\n" % wilrec.line)
   f1.write("\n")
 f.close()
 f1.close()
 print nout,"lines written to",fileout
 print nout1,"lines written to",fileout1
 # print cases where a step0a root matches more than 1 wilson root
 i = 0
 for step0arec in step0arecs:
  if len(step0arec.wilused) > 1:
   i = i + 1
   print "%s step0a record=%s" % (i,step0arec.line)
   wilkeys = ', '.join(step0arec.wilused)
   print "   Matches > 1 Wilson key:",wilkeys,"\n"
 # print the reason_counter
 print "Tabulation of reasons for matching"
 for reason in reason_counter.d.keys():
  print reason,reason_counter.d[reason]
if __name__=="__main__":
 filein = sys.argv[1] # wil_rdot.txt
 filein1 = sys.argv[2] #verb_step0a.txt
 fileout = sys.argv[3] # matched
 fileout1 = sys.argv[4] # not found
 main(filein,filein1,fileout,fileout1)
