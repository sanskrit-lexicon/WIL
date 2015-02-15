# coding=utf-8
"""
 wil_rdot_key1_ne_key2.py  Feb 12, 2015
 Reads wil_rdot.txt and writes cases where key1 != key2
 The format of the output is inspired by corr6_roots.txt
 
 python wil_rdot_key1_ne_key2.py wil_rdot.txt wil_rdot_key1_ne_key2.txt
"""
import sys, re,codecs

def main(filein,fileout):
 f = codecs.open(filein,'r','utf-8')
 fout = codecs.open(fileout,"w","utf-8")
 n = 0 # number of input records
 nout = 0 # number of output records
 for line in f:
  line = line.rstrip('\r\n')
  n = n + 1
  m = re.search(r'<key1>(.*?)</key1>.*?<key2>(.*?)</key2>',line)
  if not m:
   print "Problem at line",n
   print line.encode('utf-8')
   print
   continue
  if m.group(1) == m.group(2): 
   continue
  nout = nout + 1
  fout.write('%s\n' % line)
 f.close()
 fout.close()
 print n,"lines read from",filein
 print nout,"line written to",fileout

if __name__=="__main__":
 filein = sys.argv[1] # wil.xml
 fileout = sys.argv[2] # wil_rdot.txt
 main(filein,fileout)
