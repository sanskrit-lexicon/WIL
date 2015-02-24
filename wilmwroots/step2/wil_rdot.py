# coding=utf-8
"""
 wil_rdot.py  Feb 12, 2015
 Reads Wilson roots and MW roots and aims to find, for each
 Wilson root, the corresponding MW root.
 Wilson roots are from wil_rdot.txt.
 MW roots are from and verb_step0a.txt
 
 The format of the output is inspired by corr6_roots.txt
 
 python wil_rdot.py wil.xml wil_rdot.txt
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
  line1 = line
  if not re.search(r'\Wr[.]\W',line1):
   continue
  line1 = re.sub(r'\WE[.].*$','',line)
  if not re.search(r'\Wr[.]\W',line1):
   print "Skipping as r. occurs only after E. in line#",n
   print line.encode('utf-8')
   print
   continue
  fout.write('%s\n' % line)
  nout = nout + 1
  if re.search(r'\W[mfn]+[.]',line):
   # this catches 2 cases
   print "Please check "
   print line.encode('utf-8')
   print
 f.close()
 fout.close()
 print n,"lines read from",filein
 print nout,"line written to",fileout

if __name__=="__main__":
 filein = sys.argv[1] # wil.xml
 fileout = sys.argv[2] # wil_rdot.txt
 main(filein,fileout)
