#-*- coding:utf-8 -*-
"""make_div.py
 
 
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
  
  self.marks = []  # verb markup markers, in order found, if any
  self.newlines = None

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
 return recs,lines

class Wilverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=(.*)$',line)
  self.L,self.k1 = m.group(1),m.group(2)
  self.entry = None

def init_wilverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Wilverb(x) for x in f if x.startswith('L=')]
 print(len(recs),"records read from",filein)
 return recs

def find_entries(wilverbs,entries):
 d = Entry.Ldict
 for rec in wilverbs:
  rec.entry = d[rec.L]

def find_upasargas(recs):
 nrec = 0
 nupa = 0
 upad = {}
 for rec in recs:
  entry = rec.entry
  upasargas = []
  lines = entry.datalines
  for iline,line in enumerate(lines):
   for m in re.finditer(u' With {#([^#]+)#}',line):
     upasarga = m.group(1)
     upasargas.append(upasarga)
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

def change_wil_entry_helper(line):
 # split on 'with upasarga'
 parts = re.split(r'( [wW]ith {#[^#]+#})',line)
 newlines = []
 for part in parts:
  if part.strip() == '':
   pass
  elif part.startswith((' w',' W')):
   newpart = '<div n="p">' + part.lstrip()
   newlines.append(newpart)
  elif newlines == []:
   newlines.append(part)
  else:
   x = newlines[-1] + part
   newlines[-1] = x
 # {#x,#} -> {#x#},
 newlines0 = newlines
 newlines = []
 for line in newlines0:
  line = line.replace(',#}','#},')
  newlines.append(line)
 # split on [Page..]
 newlines0 = newlines
 newlines = []
 for iline,line in enumerate(newlines0):
  parts = re.split(u'(\[Page.*?\])',line)
  newlines1 = []
  for part in parts:
   if part.strip() == '':
    pass
   elif part.startswith(u'[Page'):
    newlines1.append(part)
   elif newlines1 == []:
    newlines.append(part)
   else:
    x = newlines1[-1] + part
    newlines1[-1] = x
  newlines = newlines + newlines1

 # split on .²1
 newlines0 = newlines
 newlines = []
 for iline,line in enumerate(newlines0):
  parts = re.split(u'([.]²)',line)
  newlines1 = []
  for part in parts:
   if part.strip() == '':
    pass
   elif part.startswith(u'.²'):
    newlines1.append(part)
   elif newlines1 == []:
    newlines.append(part)
   else:
    x = newlines1[-1] + part
    newlines1[-1] = x
  newlines = newlines + newlines1

 # split on ^a
 newlines0 = newlines
 newlines = []
 for iline,line in enumerate(newlines0):
  parts = re.split(r'(\^)',line)
  newlines1 = []
  for part in parts:
   if part.strip() == '':
    pass
   elif part.startswith(u'^'):
    newlines1.append(part)
   elif newlines1 == []:
    newlines.append(part)
   else:
    x = newlines1[-1] + part
    newlines1[-1] = x
  newlines = newlines + newlines1

 return newlines

def change_wil_entry_helper1(newlines):
 # There are several cases (e.g. in kf, RI, where
 # the upasargas are numbered.
 # This results in line pairs like:
 # .²1
 # <div n="p">With {#ati#}, ({#atikurute#}) To exceed, to do more. 
 # .²2
 # <div n="p">With {#aDi#}, ({#aDikurute#}) 
 # change these to
 # <div n="p">1 With {#ati#}, ({#atikurute#}) To exceed, to do more. 
 # <div n="p">2 With {#aDi#}, ({#aDikurute#}) 
 newlines0 = newlines
 newlines = []
 iline = 0
 n0 = len(newlines0)
 while iline < n0:
  line = newlines0[iline]
  if not re.search(u'^[.]²[0-9]+$',line):
   newlines.append(line)
   iline = iline + 1
   continue
  if iline+1 == n0:
   newlines.append(line)
   iline = iline + 1
   continue   
  line1 = newlines0[iline+1]
  if not line1.startswith('<div n="p">'):
   newlines.append(line)
   iline = iline + 1
   continue
  # join line and line1
  linea = line[2:]  # the digits after .²
  newline = line1.replace('<div n="p">','<div n="p">' + linea + ' ')
  if False:
   print('helper1 check:',iline)
   print('    ',line)
   print('    ',line1)
   print('    ',newline)
  newlines.append(newline)
  iline = iline + 2
 return newlines

def change_wil_entry(entry):
 oldlines = entry.datalines
 # find index of line with first upasarga pattern
 iline0 = None
 for iline,line in enumerate(oldlines):
  if re.search(r' [wW]ith {#([^#]+)#}',line):
   iline0 = iline
   break
  if re.search(r' [wW]ith *$',line):
   iline0 = iline
   break
 line0 = oldlines[iline0]
 
 m = re.search(r'^(.*?)([.]²[0-9]+ [wW]ith.*)$',line0)
 if not m:
  m = re.search(r'^(.*?)( [wW]ith.*)$',line0)
 line0a = m.group(1)
 line0b = m.group(2)
 newlines = []
 for iline,line in enumerate(oldlines):
  if iline<iline0:
   newlines.append(line)
  elif iline == iline0:
   newlines.append(line0a)
   break
 endlines = [line0b] + oldlines[iline0+1:]
 endline = ' '.join(endlines)
 endlines1 = change_wil_entry_helper(endline)
 endlines2 = change_wil_entry_helper1(endlines1)
 newlines = newlines + endlines2
 newlines = [entry.metaline] + newlines + [entry.lend]
 return newlines
 
def change_wil_entries(wilverbs):
 for rec in wilverbs:
  # replacement for rec.entry.datalines
  rec.newlines = change_wil_entry(rec.entry)
  rec.entry.newlines = rec.newlines

def check_sorted(wilverbs):
 prev = 0
 for irec,wilrec in enumerate(wilverbs):
  if prev < wilrec.entry.linenum1:
   prev = wilrec.entry.linenum1
  else:
   print('check_sorted error:',prev,rec.line)
   exit(1)
 print('check_sorted works properly')

def write(fileout,all_lines,wilverbs):
 check_sorted(wilverbs)
 outlines = []
 nwil = len(wilverbs)
 iwil = 0
 wilrec = wilverbs[iwil]
 wil_linenum1 = wilrec.entry.linenum1
 wil_linenum2 = wilrec.entry.linenum2
 newlines = wilrec.newlines
 inewline = 0
 iline = 0
 iline_max = len(all_lines)
 while(iline < iline_max):
  linenum = iline+1
  if linenum < wil_linenum1:
   outlines.append(all_lines[iline])
   iline = iline + 1
   continue
  if linenum == wil_linenum1:
   for newline in newlines:
    outlines.append(newline)
   iline = wil_linenum2
   iwil = iwil + 1
   if (iwil < nwil):
    wilrec = wilverbs[iwil]
    wil_linenum1 = wilrec.entry.linenum1
    wil_linenum2 = wilrec.entry.linenum2
    newlines = wilrec.newlines
    inewline = 0
   else:
    wil_linenum1 = iline_max + 1
 with codecs.open(fileout,"w","utf-8") as f:
  for line in outlines:
   f.write(line + '\n')

def write_check(fileout,entries):
 case = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for entry in entries:
   if entry.newlines == None:
    continue
   case = case + 1
   outarr = []
   outarr.append('; Case %03d' %case)
   outarr.append('; OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD OLD')
   lines = [entry.metaline] + entry.datalines + [entry.lend]
   outarr = outarr + lines
   outarr.append('; NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW')
   outarr = outarr + entry.newlines
   outarr.append('; ===============================================')
   outarr.append(';')
   for out in outarr:
    f.write(out + '\n')
   
 print(case,"cases written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # wil_upasarga_ids.txt
 fileout = sys.argv[3] # 
 fileout1 = sys.argv[4] 
 entries,all_lines = init_entries(filein)
 wilverbs = init_wilverbs(filein1) # L,k1
 # assign entry to each wil verb record
 find_entries(wilverbs,entries)  
 change_wil_entries(wilverbs)
 write(fileout,all_lines,wilverbs)
 write_check(fileout1,entries)
