#-*- coding:utf-8 -*-
"""cat.py
 
 
"""
from __future__ import print_function
import sys, re,codecs

def write(fileout,d):
 n = 0
 recs = []
 for k in d.keys():
  recs.append((k,d[k]))
 recs = sorted(recs,key = lambda x: x[0].lower())
 with codecs.open(fileout,"w","utf-8") as f:
  tot = 0  # total of count

  for rec in recs:
   k,c =rec
   n = n + 1
   tot = tot + d[k]
   out = '%s\t%d' %(k,c)
   f.write(out + '\n')
 print(tot,"instances in",n,"records written to",fileout)


def init_bot(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f if not line.startswith(';')]
 d = {}
 for idx,line in enumerate(lines):
  parts = line.split('\t')
  if len(parts) != 2:
   print('init_bot: bad line',line)
   continue
  part,count = parts
  #partlo = part.lower()
  partlo = part
  if partlo not in d:
   d[partlo] = 0
  d[partlo] = d[partlo] + int(count)
 print(len(d.keys()),"records found in",filein)
 return d


def merge(d1,d2):
 d = {}
 for k in d1:
  d[k] = d1[k]
 for k in d2:
  if k in d:
   d[k] = d[k] + d2[k]
   print('merge duplicate:',k)
  else:
   d[k] = d2[k]
 print(len(d.keys()),"merged text fragments")
 return d

if __name__=="__main__": 
 filein = sys.argv[1]   # wil_mwbot.txt
 filein1 = sys.argv[2] #  wil_not_mwbot.txt
 fileout = sys.argv[3] # wil_bot.txt
 d1 = init_bot(filein)
 d2 = init_bot(filein1)
 d = merge(d1,d2)
 write(fileout,d)
