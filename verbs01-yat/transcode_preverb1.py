#-*- coding:utf-8 -*-
"""transcode_preverb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs

import transcoder
transcoder.transcoder_set_dir('transcoder')

def init_lines(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip('\r\n') for x in f ]
 print(len(recs),"records read from",filein)
 return recs


def transcode_line(x,tranin,tranout):
 """ x a line from preverb1.txt
 """
 def transcode1(m):
  a = m.group(1)
  b = m.group(2)
  c = m.group(3)
  b1 = transcoder.transcoder_processString(b,tranin,tranout)
  return a+b1+c

 if x.startswith(';'):
  # a 'verb' line
  ## transcode k1, k2, mw values
  for regex in [
        r'(k1=)(.*?)([, ])',
        r'(k2=)(.*?)([, ])',
        r'(mw=)(.*?)([, ])' ]:
   x = re.sub(regex,transcode1,x)
  return x
 # otherwise, x is a 'preverb' line, with 6 or 7 fields separated by spaces
 # 01   anu   as  anvas anvas yes anu+as
 # 02   vyati as  vyatyad vyatyad no
 parts = re.split(r'( +)',x)
 newparts = []
 for part in parts:
  if part == None:
   pass
  elif part.startswith(' '):
   newparts.append(part)
  elif part in ['yes','no']:
   newparts.append(part)
  elif re.search(r'^[0-9]',part):
   newparts.append(part)
  else:
   newpart = transcoder.transcoder_processString(part,tranin,tranout)
   newparts.append(newpart)
 y = ''.join(newparts)
 return y

def write(fileout,recs,tranout):
 tranin = 'slp1'
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   out = transcode_line(rec,tranin,tranout)
   f.write(out+'\n')
 print(len(recs),"%s-transcoded written to %s"%(tranout,fileout))

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  preverb1.txt
 fileout = sys.argv[3] # 
 lines = init_lines(filein)
 write(fileout,lines,tranout)
