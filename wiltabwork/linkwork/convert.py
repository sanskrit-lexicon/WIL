""" convert.py
 Dec 27, 2014
 convert a file from compare2.txt (Cologne: WILSCAN/2014/pywork/wiltabwork/)
  Into two forms:
  1.  For input to faultfinder3a-html.php
  2.  For work while using the result of 1
 python convert.py compare2-case02.txt case02_ff.txt case02.txt

"""
import sys, re
import codecs

import string
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)
def slp_cmp(a,b):
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)


def generate(inrecs,fileout1,fileout2):
 fout1 = codecs.open(fileout1,'w','utf-8')
 fout2 = codecs.open(fileout2,'w','utf-8')

 # read inrecs, and generate output
 n = 0 # count of lines read
 lnum = 0 # generate record number for xml records constructed
 nout = 0
 for inrec in inrecs:
  nout = nout + 1
  fout1.write("%s:VCV=XXX:WIL\n" %(inrec.wilhw2))
  fout2.write("%s %s -> %s : %s\n" %(inrec.n,inrec.wilhw2,inrec.wiltab,inrec.comment))

 # close output
 fout1.close()
 fout2.close()
 # informational message
 print nout,"records written to ",fileout1
 print nout,"records written to ",fileout2

class Compare2(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  line = line.rstrip() # remove trailing blanks
  self.line = line # the text
  parts = re.split(r':',line)
  if len(parts) != 2:
   print "Compare2 ERROR 1:",line
   exit(1)
  head = parts[0]
  self.comment = parts[1]
  parts = re.split(' ',head)
  if len(parts) != 5:
   print "Compare2 ERROR 2:",line
   exit(1)
  (self.case,self.n,self.wiltab,self.relation,self.wilhw2) = parts

if __name__=="__main__":
 fileinrec = sys.argv[1] 
 with codecs.open(fileinrec,encoding='utf-8',mode='r') as f:
  inrecs = [Compare2(line) for line in f]
 fileout1 = sys.argv[2] #
 fileout2 = sys.argv[3] #
 generate(inrecs,fileout1,fileout2)

