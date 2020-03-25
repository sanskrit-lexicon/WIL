from __future__ import print_function
import sys, re,codecs
from preverb1 import init_entries,Entry

class Change(object):
 def __init__(self,metad,changes):
  self.metad = metad
  self.changes = changes

def compare(a,b):
 ans = []
 for i,xa in enumerate(a):
  xb = b[i]
  if xa != xb:
   ans.append((xa,xb))
 return ans

def find_changes(a,b):
 changes = []
 for i,ea in enumerate(a):
  eb = b[i]
  alines = [ea.metaline] + ea.datalines
  blines = [eb.metaline] + eb.datalines

  #c = compare(ea.datalines,eb.datalines)
  c = compare(alines,blines)
  if c == []:
   continue
  if ea.metaline != eb.metaline:
   print('WARNING metaline change at entry',i)
   print(ea.metaline)
   print(eb.metaline)
  
  change = Change(ea.metad,c)
  changes.append(change)
 return changes

def count_with(changes):
 n = 0
 for old,new in changes:
  if len(new)>(len(old) + 3):
   n = n + 1
 return n

def write(changes,fileout):
 mwith = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for ichange,change in enumerate(changes):
   outarr = []
   case = ichange+1
   carr = change.changes
   metad = change.metad
   n = len(carr)
   L = metad['L']
   k1 = metad['k1']
   nwith = count_with(carr)
   if nwith == 0:
    out = '; Case %03d: L=%s, k1=%s, #changes=%s' %(case,L,k1,n)
   else:
    mwith = mwith + 1
    out = '; Case %03d: L=%s, k1=%s, #changes=%s, #extra_withs=%d' %(case,L,k1,n,nwith)
   outarr.append(out)
   for i,c in enumerate(carr):
    old,new = c
    outarr.append(';')
    outarr.append('old: %s' %old)
    outarr.append('new: %s' %new)
   outarr.append('; -----------------------------------------------')
   for out in outarr:
    f.write(out + '\n')
 print(len(changes),"changed entries written to",fileout)
 print(mwith,"entries have 'with' additions")
if __name__=="__main__": 
 fileold = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filenew = sys.argv[2] #  new xxx.txt
 fileout = sys.argv[3] #  changes

 oldentries = init_entries(fileold)
 Ldictold = Entry.Ldict
 Entry.Ldict = {}
 newentries = init_entries(filenew)
 Ldictnew = Entry.Ldict
 changes = find_changes(oldentries,newentries)
 write(changes,fileout)
