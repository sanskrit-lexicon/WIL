# coding=utf-8
""" transcode.py for WILson. Converts keys to SLP1
 Reads/Writes utf-8
 Dec 25, 2014
 
"""
import sys, re,codecs
sys.path.insert(0,"../")  # where transcoder resides

import transcoder
transcoder.transcoder_set_dir(""); # use local non-standard transcoder files


def convert(filein,fileout,tranin,tranout):
 # slurp txt file into list of lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
    inlines = f.readlines()
 fout = codecs.open(fileout,'w','utf-8')
 nchg=0
 mlines = len(inlines)
 for i in xrange(0,mlines):
  line=inlines[i].rstrip('\r\n')
  (n,hk) = re.split(r':',line)
  slp = transcoder.transcoder_processString(hk,tranin,tranout)
  out = "%s:%s" %(n,slp)
  fout.write("%s\n" %out)
 fout.close()

if __name__=="__main__":
 filein = sys.argv[1] # 
 fileout = sys.argv[2] #
 option = '1'
 if option == '1':
  convert(filein,fileout,'hk','slp1')
 elif option == '2':
  convert(filein,fileout,'slp1','hk')
 else:
  print "Bad option = ",option
  print "option must be 1 or 2"

