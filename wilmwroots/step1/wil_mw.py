# coding=utf-8
"""
 wil_mw.py  Feb 12, 2015
 Reads Wilson roots and MW roots and aims to find, for each
 Wilson root, the corresponding MW root.
 Wilson roots are from wil_rdot.txt.
 MW roots are from and verb_step0a.txt
 
 The format of the output is inspired by corr6_roots.txt
 
 python wil_mw.py ../wil_rdot.txt ../verb_step0a.txt corr6-roots.txt wil_mw.txt wil_mw_prob.txt

  Note: corr6-roots is used as a 'last resort':  it has some correspondences
    developed by Matthias and Peter in 2011.
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

class Corr6(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  m = re.search(r'^<c>(.*?)</c> *<wil>(.*?)</wil> *<mw>(.*?)</mw>',line)
  if not m:
   print "Problem with",line
   exit(1)
  (self.c,self.wil,self.mw) = (m.group(1),m.group(2),m.group(3))
  self.used = False 


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

def match(wilkey,step0dict,dcorr6):
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

 # WIlson usually doubles consonants after 'r'
 wilkey1 = re.sub(r'[r](.)\1',r'r\1',wilkey)
 if wilkey1 != wilkey: 
  if wilkey1 in step0dict:
   return ('ROOT-r',wilkey1)
  if wilkey1.endswith('a'):
   mwkey = wilkey1[0:-1]
   if mwkey in step0dict:
    return ('SPa-ROOT-r',mwkey)
 # Try dcorr6
 if wilkey in dcorr6:
  mwkey = dcorr6[wilkey]
  ans = ('SPma-ROOT',mwkey)
  # check that mwkey is in step0dict:
  if not (mwkey in step0dict):
   print wilkey,'matches',mwkey,'by Corr6, but',mwkey,'is not in step0a verbs'
  return ans
 # no luck
 return (None,None)

def main(filein,filein1,filein2,fileout,fileout1):
 # read verb_step0a.txt into array of records
 with codecs.open(filein1,'r') as f:
  step0arecs= [Step0a(line) for line in f]
 print len(step0arecs),"records read from",filein1

 # read corr6_roots.txt into array of records
 with codecs.open(filein2,'r') as f:
  corr6recs= [Corr6(line) for line in f]
 print len(corr6recs),"records read from",filein1

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
 # make dictionary from corr6recs
 # with the key
 dcorr6 = {}
 for r in corr6recs:
  wilkey = r.wil
  if key in dcorr6:
   print "corr6 unexpected duplicate wilkey",wilkey
  dcorr6[wilkey]=r.mw

 # generate output
 f = codecs.open(fileout,"w","utf-8")
 f1 = codecs.open(fileout1,"w","utf-8")
 nout = 0
 nout1 = 0
 # initialize counter of reaons for matches
 reason_counter=Counter()
 for wilrec in wilrecs:
  wilkey = wilrec.wilkey
  (reason,mwkey) = match(wilkey,d,dcorr6)
  reason_counter.update([reason])
  if reason:
   out = "<c>%s</c> <wil>%s</wil> <mw>%s</mw>" %(reason,wilkey,mwkey)
   f.write("%s\n" % out)
   nout = nout + 1
   # Feb 13, 2015.  Update wilused for all step0a records
   if mwkey in d:
    for step0arec in d[mwkey]:
     step0arec.wilused.append(wilkey)
   # Feb 14, 2015. Check if dcorr6 gives same answer where applicable
   if wilkey in dcorr6:
    mwkey1=dcorr6[wilkey]
    if mwkey != mwkey1:
     print "WARNING: For wilkey=%s, mwkey(%s) != dcorr6(%s)"%(wilkey,mwkey,mwkey1)
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
 filein2 = sys.argv[3] # corr6-roots.txt
 fileout = sys.argv[4] # matched
 fileout1 = sys.argv[5] # not found
 main(filein,filein1,filein2,fileout,fileout1)
