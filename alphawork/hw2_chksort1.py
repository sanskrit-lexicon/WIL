"""hw2_chksort.py  ejf Oct 1, 2013
 Read  Xhw2.txt, whose lines were created with:
 out = "%s:%s:%s,%s" %(page,hw,l1,l2)

 Check alphabetical order. Write out exceptions
 usage: python26 hw2_chksort1.py wilhw2.txt hw2_chksort1.txt
"""
import re
import sys
import string
tranfrom="aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
tranto = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
trantable = string.maketrans(tranfrom,tranto)
def slp_cmp(a,b):
 a1 = string.translate(a,trantable)
 b1 = string.translate(b,trantable)
 return cmp(a1,b1)

filename=sys.argv[1] 
fileout =sys.argv[2] 
f = open(filename,'r')
fout = open(fileout,'w')
n = 0
nout = 0 # number of headword lines written to output
lines = []
for line in f:
 n = n+1
 line = line.strip() # remove starting or ending whitespace
 lines.append(line)
 # Standardization of AS spelling
# for debugging
f.close()
print "file %s has %s lines" % (filename,n)
# check for sort errors
nprob=0
for i in xrange(1,len(lines)):
 (page,hw1,lrange)  = re.split(':',lines[i-1])
 (page,hw2,lrange)  = re.split(':',lines[i])
 c = slp_cmp(hw1,hw2)
 if (c > 0):
  nprob=nprob+1
  fout.write("%s !< %s\n" %(lines[i-1],lines[i]))
fout.close()
print "%s sort errors written to  %s" % (nprob,fileout)

