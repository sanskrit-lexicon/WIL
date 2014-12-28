# coding=utf-8
""" compare.py
 Reads/Writes utf-8
 Dec 25, 2014
 Compares wiltabkeys.txt and ../wilhw2.txt
"""
import sys, re,codecs
sys.path.insert(0,"../")  # where transcoder resides

import transcoder
transcoder.transcoder_set_dir(""); # use local non-standard transcoder files


def compare1(filein,filein1,fileout):
 # get wilkeys array
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  wilkeys=[]
  for line in f:
   (n,key)=re.split(r':',line.rstrip('\r\n'))
   wilkeys.append(key)
 # get wilhw2 array
 with codecs.open(filein1,encoding='utf-8',mode='r') as f:
  wilhw2=[]
  for line in f:
   (page,key,l12)=re.split(r':',line.rstrip('\r\n'))
   wilhw2.append(key)

 fout = codecs.open(fileout,'w','utf-8')
 n1 = len(wilkeys)
 n2 = len(wilhw2)
 print n1,n2
 n = max(n1,n2) 
 ifirst=-1
 ilast = -1
 for i in xrange(0,n):
  if i >= n1:
   key1 == 'NONE'
  else:
   key1 = wilkeys[i]
  if i >= n2:
   key2 == 'NONE'
  else:
   key2 = wilhw2[i]
  if key1 == key2:    
   fout.write("%d:%s == %s\n"%(i+1,key1,key2))
   ilast = i+1
  elif ("%sa"%key1) == key2:
   fout.write("%d:%s =a %s\n"%(i+1,key1,key2))
  else:
   if ifirst == -1:
    ifirst = i+1
   fout.write("%d:%s != %s\n"%(i+1,key1,key2))
 fout.close()
 print "ifirst =",ifirst
 print "ilast = ",ilast

if __name__=="__main__":
 option = sys.argv[1]
 filein = sys.argv[2] # wiltab
 filein1 = sys.argv[3] # wilhw2
 fileout = sys.argv[4] #
 if option == '1':
  compare1(filein,filein1,fileout)
 else:
  print "Bad option = ",option
  print "option must be 1 or 2"

