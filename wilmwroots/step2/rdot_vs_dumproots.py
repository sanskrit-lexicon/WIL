""" rdot_vs_dumproots.py
    June 10, 2016
    compare wil_rdot.txt to the dumproots.txt file of wiltab2011 
"""
import codecs,re,sys

import string
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)
def slp_cmp(a,b):
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)
def slp_sortkey(a):
 return string.translate(a,trantable)

class Dumproot(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (self.hk,self.key1) = line.split('\t')
  self.key1 = str(self.key1)  # for sorting, need a string

def init_dumproots(filein):
 recs=[]
 with codecs.open(filein,"r","utf-8") as f:
  for line in f:
   rec = Dumproot(line)
   recs.append(rec)
 print len(recs),"records from",filein
 chksort(recs)
 return recs

class Rdot(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'<key1>(.*?)</key1>',line)
  if not m:
   print "Rdot error:",line.encode('utf-8')
   exit(1)
  self.key1 = str(m.group(1))

def chksort(recs):
 n = len(recs)
 for i in xrange(0,n-1):
  try:
   keya = recs[i].key1
   keyb = recs[i+1].key1
   c = slp_cmp(keya,keyb)
   if c > 0:
    print '%i: %s > %s' %(i,recs[i].key1,recs[i+1].key1)
    #print c
    #print recs[i].line.encode('utf-8')
    #print recs[i+1].line.encode('utf-8')
    
  except UnicodeDecodeError as err:
   print "problem comparing.",err
   out = '"%s" , "%s"' %(recs[i].key1,recs[i+1].key1)
   print out.encode('utf-8')
   exit(1)

def init_rdot(filein):
 recs=[]
 with codecs.open(filein,"r","utf-8") as f:
  for line in f:
   rec = Rdot(line)
   recs.append(rec)
 print len(recs),"records from",filein
 chksort(recs)
 # check for duplicates
 d = {}
 for rec in recs:
  if rec.key1 in d:
   print "Duplicate key:",rec.key1
  else:
   d[rec.key1]=True

 return recs

def merge_sortkey(rec):
 """ rec is a Merge record
 """
 return slp_sortkey(rec.key) + "-" + rec.type

class Merge(object):
 def __init__(self,rec):
  self.rec = rec
  self.key = rec.key1
  if isinstance(rec,Rdot):
   self.type="Rdot-Only"
  elif isinstance(rec,Dumproot):
   self.type = "Dumproot-Only"
  else:
   print "MERGE ERROR:"
  self.types = [self.type]

def  merge(rdots,dumproots):
 recs = []
 for rdot in rdots:
  recs.append(Merge(rdot))
 for dumproot in dumproots:
  recs.append(Merge(dumproot))
 # now sort
 recs1 = sorted(recs,key = merge_sortkey)
 recs2 = []
 recs2.append(recs1[0])
 for i in xrange(1,len(recs1)):
  rec = recs1[i]
  prevrec = recs1[i-1]
  if prevrec.key != rec.key:
   recs2.append(rec)
  elif rec.type not in prevrec.types:
   prevrec.types.append(rec.type)
  else:
   print "merge duplicate",rec.key,rec.type
 return recs2

if __name__ == "__main__":
 filein1 = sys.argv[1] # wil_rdot
 filein2 = sys.argv[2] # dumproots
 fileout = sys.argv[3] 
 rdots = init_rdot(filein1)
 dumproots = init_dumproots(filein2)
 allrecs = merge(rdots,dumproots)
 fout = codecs.open(fileout,"w","utf-8")
 n = 20
 n = len(allrecs)
 for i in xrange(0,n):
  rec = allrecs[i]
  if rec.types == ['Dumproot-Only','Rdot-Only']:
   t = 'BOTH'
  else:
   t = rec.types[0]
  fout.write('%s %s\n' %(rec.key,t))
  #print rec.key,t
 fout.close()
 print len(allrecs),"written to",fileout


