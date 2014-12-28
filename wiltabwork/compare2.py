# coding=utf-8
""" compare2.py
 Reads/Writes utf-8
 Dec 26, 2014
 
"""
import sys, re,codecs
from operator import itemgetter
sys.path.insert(0,"../")  # where transcoder resides

import transcoder
transcoder.transcoder_set_dir(""); # use local non-standard transcoder files

class Wilhw1(object): # for wilhw1
 def __init__(self,line):
  line = line.rstrip('\r\n')
  line = line.rstrip() # remove trailing blanks
  self.line = line # the text
  parts = re.split(r'[ >-]+',line)
  try:
   (self.id,self.old,self.new) = parts
  except:
   print "Input ERROR: Wrong # of parts: %s" % len(parts)
   for i in xrange(0,len(parts)):
    out = "part#%s='%s'" %(i+1,parts[i])
    print out.encode('utf-8')
   exit(1)
  self.hwrec = None # filled in later


class Compare1(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (n,x)=re.split(':',line)
  (self.wiltab,self.relation,self.wilhw2) = re.split(r' +',x)
  self.wiltaberrors = [] # allow for multiple associations 

class WiltabError(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'^<r><rule conf="(.*?)">(.*?)</rule> *<c>(.*?)</c> *<wil(.*?)>(.*?)</wil> *<mw>(.*?)</mw> *</r>$',line)
  if not m:
   print "WiltabError ERROR parsing line\n",line
   exit(1)
  self.conf=m.group(1)
  self.rule=m.group(2)
  self.c=m.group(3)
  self.wilkey=m.group(5)
  self.mwkey = m.group(6)
  attrs = m.group(4) # attributes of 'wil' tag, if any
  self.wilerrcode=None
  self.wilcorr=None
  m = re.search(r'err="(.*?)"',attrs)
  if m:
   self.wilerrcode=m.group(1)
  m = re.search(r'corr="(.*?)"',attrs)
  if m:
   self.wilcorr=m.group(1)

def match_mwhw1(recs3,key,which):
 for rec in recs3:
  if (which == 'old') and (key == rec.old):
   return rec
  elif (which == 'new') and (key == rec.new):
   return rec
 return None

def compare2(filein,filein1,filein2, fileout):
 # get compare2
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs1 = [Compare1(x) for x in f]
 # get wiltab_mw_error.txt
 with codecs.open(filein1,encoding='utf-8',mode='r') as f:
  recs2 = [WiltabError(x) for x in f]
 # get wilmw1
 with codecs.open(filein2,encoding='utf-8',mode='r') as f:
  recs3 = [Wilhw1(x) for x in f]
 
 # try to associate each recs2 with 1 or more recs1
 for rec2 in recs2:
  nfound=0
  for rec1 in recs1:
   if rec1.wiltab in [rec2.wilkey,rec2.wilcorr,rec2.mwkey]:
    rec1.wiltaberrors.append(rec2)
    nfound = nfound + 1
   elif rec1.wilhw2 in [rec2.wilkey,rec2.wilcorr,rec2.mwkey]:
    rec1.wiltaberrors.append(rec2)
    nfound = nfound + 1
  if nfound == 0:
   print "NO MATCH:",rec2.line
 # print an extract of recs1
 fout = codecs.open(fileout,'w','utf-8')
 n = 0
 outrecs=[] # collect output records. Will later sort and print to fout
 for rec1 in recs1:
  n = n + 1
  matches = rec1.wiltaberrors
  nmatches = len(matches)
  rec3 = match_mwhw1(recs3,rec1.wilhw2,'new')
  outarr = []
  out = "%s %s %s: " %(rec1.wiltab,rec1.relation,rec1.wilhw2)
  outarr.append(out)
  if (nmatches == 0) and (rec1.relation == '!='):
   if rec3 and (rec3.old == rec1.wiltab):
    outarr.append("WILHW1 CORRECTION MISSED BY WILTAB")
    icase = 7
   else:
    outarr.append("UNEXPLAINED DIFFERENCE")
    icase = 5
   out = ''.join(outarr)
   outrecs.append((icase,n,out))
  elif (nmatches == 0):
   pass  # skip this in output
  elif (nmatches == 1):
   rec2 = matches[0]
   if (rec1.relation == '!=') and (rec1.wiltab == rec2.wilcorr) and\
      (rec1.wilhw2 == rec2.wilkey):
    outarr.append("CORRECTION(A)")
    if rec1.wiltab == rec2.mwkey:
     outarr.append(", MW=WILTAB" )
    else:
     outarr.append(", MW=%s" % rec2.mwkey)
    out = ''.join(outarr)
    icase = 2
    outrecs.append((icase,n,out))
   elif (rec1.relation == '!=') and (rec2.wilcorr == None):
    outarr.append("CORRECTION(B)" )
    if rec1.wiltab == rec2.mwkey:
     outarr.append(", MW=WILTAB" )
    else:
     outarr.append(", MW=%s" % rec2.mwkey)
    out = ''.join(outarr)
    icase = 3
    outrecs.append((icase,n,out))
   elif (rec1.relation == '=a'):
    outarr.append("a-AGREE")
    if rec1.wiltab == rec2.mwkey:
     outarr.append(", MW=WILTAB" )
    else:
     outarr.append(", MW=%s" % rec2.mwkey)
    out = ''.join(outarr)
    icase = 6
    outrecs.append((icase,n,out))   
   elif (rec1.relation == '==') and (rec1.wiltab == rec2.wilkey):
    if ('ttr' in rec2.mwkey) and ('ttr' not in rec2.wilkey):
     icase = 19
     mwalt = re.sub(r'ttr','tr',rec2.mwkey)
     if mwalt == rec1.wiltab:
      outarr.append(", MW has *ttr*" )
     else:
      outarr.append(", MW=%s" % rec2.mwkey)
    elif ('ttr' not in rec2.mwkey) and ('ttr' in rec2.wilkey):
     icase = 20
     outarr.append("AGREE-tt/t")
     wilkeyalt = re.sub(r'ttr','tr',rec2.wilkey)
     if rec2.mwkey == wilkeyalt:
      outarr.append(", MW has *tr*" )
     else:
      outarr.append(", MW=%s" % rec2.mwkey)
    else:
     outarr.append("AGREE-misc")
     icase = 14
     outarr.append(", MW=%s" % rec2.mwkey)
    out = ''.join(outarr)
    outrecs.append((icase,n,out))
   elif (rec1.relation == '==') and (rec1.wiltab != rec2.wilkey) and\
        (rec1.wiltab == rec2.wilcorr):
    outarr.append("AGREE CORRECTION")
    outarr.append(", MW=%s" % rec2.mwkey)
    out = ''.join(outarr)
    icase = 22
    outrecs.append((icase,n,out))
   elif rec1.relation == '!=':
    outarr.append("%s" % rec2.line)
    out = ''.join(outarr)
    icase = 9
    outrecs.append((icase,n,out))  
   elif rec1.relation == '!=':
    outarr.append("%s" % rec2.line)
    out = ''.join(outarr)
    icase = 90
    outrecs.append((icase,n,out))  
  else: # nmatches>1. Rare or never
   for i in xrange(0,nmatches):
    rec2 = matches[i]
    outarr.append("(%d) " % (i+1))
    outarr.append("%s" % rec2.line)
   out = ''.join(outarr)
   icase = 99
   outrecs.append((icase,n,out))  
 # sort outrecs 
 # ref = https://wiki.python.org/moin/HowTo/Sorting
 outrecs=sorted(outrecs, key=itemgetter(0,1))
 # print outrecs
 icase0 = -1
 for outrec in outrecs:
  (icase,ndummy,out)=outrec
  if icase != icase0:
   n = 0
   fout.write("\n%s\ncase %s\n" %("-"*70,icase))
   icase0 = icase
  n = n + 1
  fout.write("%02d %03d %s\n" % (icase,n,out))
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # compare1.txt
 filein1 = sys.argv[2] # wiltab_mw_error.txt
 filein2 = sys.argv[3] # wilmw1.txt (corrections to wil.txt)
 fileout = sys.argv[4] # compare2.txt
 compare2(filein,filein1,filein2,fileout)
