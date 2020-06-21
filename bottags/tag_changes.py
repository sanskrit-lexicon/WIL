#-*- coding:utf-8 -*-
"""matchmw.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline

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
  self.tags = []
  self.newlines = []
  for iline,dataline in enumerate(self.datalines):
   self.tags.append([])
   self.newlines.append(None)
  self.sometag = False

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

def change_line_tag_part(part,tag,tagelt):
 ans = None
 parts = re.split(r'(<.*?>.*?</.*?>)',part)
 newparts = []
 found = False
 for part in parts:
  if part == None:
   newpart = ''
  elif part.startswith('<'):
   newpart = part
  elif tag in part:
   regex = r'\b' + tag + r'\b'
   tagpart = '<%s>%s</%s>' %(tagelt,tag,tagelt)
   newpart = re.sub(regex,tagpart,part)
   if newpart != part:
    found = True
  else:
   newpart = part
  newparts.append(newpart)
 if found:
  ans = ''.join(newparts)
 return ans
 
def change_line_tag(line,tag,tagelt):
 ans = None
 # {#xxx#}, {%...%}   sanskrit text and italic text exclude
 parts = re.split(r'({.*?})',line)
 newparts = []
 found = False
 for part in parts:
  if part == None:
   newpart = ''
  elif part.startswith('{'):
   newpart = part
  elif tag in part:
   newpart = change_line_tag_part(part,tag,tagelt)
   if newpart != None:
    found = True
   else:
    newpart = part
  else:
   newpart = part
  newparts.append(newpart)
 if found:
  ans = ''.join(newparts)
 return ans

def changes(entries,tags,tagelt):
 n = 0
 changelines = [] # return array of lines to be changed
 for entry in entries:
  marks = []
  for iline,line in enumerate(entry.datalines):
   for tag in tags:
    if tag in line:
     oldline = line
     if entry.newlines[iline] != None:
      oldline = entry.newlines[iline]
     newline = change_line_tag(oldline,tag,tagelt)
     if newline != None:
      entry.tags[iline].append(tag)
      entry.sometag = True
      entry.newlines[iline] = newline
   if entry.newlines[iline] != None:
    L = entry.metad['L']
    k1 = entry.metad['k1']
    linenum = entry.linenum1 + iline + 1
    outarr = []
    outarr.append('; k1=%s, L=%s'%(k1,L))
    out = '%s old %s' %(linenum,line)
    outarr.append(out)
    out = '%s new %s' %(linenum,entry.newlines[iline])
    outarr.append(out)
    if False:
     for out in outarr:
      print(out)
    changelines = changelines + outarr
  if entry.sometag:
   n = n + 1
   if False: # debug
    L = entry.metad['L']
    k1 = entry.metad['k1']
    alltags = []
    for tagsline in entry.tags:
     alltags = alltags + tagsline
    print(L,k1,alltags)
 print('changes finds',n,'entries that may have a change')
 return changelines

def mark_changes(entries,tags):
 for entry in entries:
  marks = []
  for iline,line in enumerate(entry.datalines):
   for m in re.finditer(regex,line):
    text = m.group(1)
    if text not in d:
     d[text] = 0
    d[text] = d[text] + 1
 return d

def write(fileout,outlines):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  tot = 0  # total of count
  for out in outlines:
   f.write(out + '\n')
 print(len(outlines),"lines written to",fileout)

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
 # sort the tags decreasing by length
 keys = sorted(d.keys(),key = lambda x: len(x), reverse=True)
 return keys

if __name__=="__main__": 
 tagelt = sys.argv[1]
 filein = sys.argv[2]   # wil_tag.txt
 filein1 = sys.argv[3] #  wil.txt
 fileout = sys.argv[4] # manualByLine_tag.txt
 entries = init_entries(filein1)
 tags = init_bot(filein)
 outlines = changes(entries,tags,tagelt)
 write(fileout,outlines)
