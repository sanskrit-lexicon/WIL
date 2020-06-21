#-*- coding:utf-8 -*-
"""matchmw.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
#from parseheadline import parseheadline

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
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
  self.verb = None  # value of verb attribute root|genuineroot|pre|gati|nom
  self.parse = None  # string value of parse attribute (for pre/gati
  self.cps  = None  # string value of cp attribute
  
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

def gather_tags(entries,tag):
 #infokeys = ['verb','cp','parse']
 d = {} # dictionary of tag, with counts
 regex = '<%s>(.*?)</%s>' %(tag,tag)
 for entry in entries:
  marks = []
  for iline,line in enumerate(entry.datalines):
   for m in re.finditer(regex,line):
    text = m.group(1)
    if text not in d:
     d[text] = 0
    d[text] = d[text] + 1
 return d

def write(fileout,wilrecs,flag):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  tot = 0  # total of count
  for rec in wilrecs:
   if rec.mwbot == flag:
    n = n + 1
    tot = tot + 1
    out = '%s\t%d' %(rec.part,rec.count)
    f.write(out + '\n')
 print(tot,"instances in",n,"records written to",fileout)

class WILBOT(object):
 def __init__(self,part,count):
  self.part = part
  self.count = count
  self.mwbot = False

def init_wil_bot(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 d = {}
 for idx,line in enumerate(lines):
  parts = line.split(',')  
  for part in parts:
   if part not in d:
    d[part] = 0
   d[part] = d[part] + 1
 recs = []
 keys = sorted(d.keys(),key = lambda x: x.lower())
 for key in keys:
  recs.append(WILBOT(key,d[key]))
 return recs

def init_mw_bot(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 d = {}
 for idx,line in enumerate(lines):
  part,count = line.split('\t')
  partlo = part.lower()
  if partlo not in d:
   d[partlo] = 0
  d[partlo] = d[partlo] + int(count)
 return d

def mark_wilrecs(wilrecs,mwd):
 for rec in wilrecs:
  if rec.part.lower() in mwd:
   rec.mwbot = True

if __name__=="__main__": 
 filein = sys.argv[1]   # wil_botany
 filein1 = sys.argv[2] #  mw_bot
 fileout = sys.argv[3] # 
 fileout1 = sys.argv[4]
 wilrecs = init_wil_bot(filein)
 mwd = init_mw_bot(filein1)
 mark_wilrecs(wilrecs,mwd)
 write(fileout,wilrecs,True)
 write(fileout1,wilrecs,False)
