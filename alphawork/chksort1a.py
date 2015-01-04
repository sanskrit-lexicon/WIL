"""chksort1a.py  ejf Jan 3, 2015
 read chksort1.txt and sanhw1.txt
 filter into 
   chksort1a.txt  (one or the other headword not found in
      another dictionary)
   chksor1a_rest.txt  (both headwords found in another dictionary).

 usage: python26 chksort1a.py chksort1.txt ../../../../awork/sanhw1/sanhw1.txt chksort1a.txt chksort1a_rest.txt chksort1a_singletons.txt

"""
import re
import sys

class Chksort(object):
    def __init__(self,line):
        line = line.rstrip('\r\n')
        self.line =line
        (hw1,hw2) = re.split(' !< ',line)
        (self.page1,self.hw1,self.lines1) = re.split(':',hw1)
        (self.page2,self.hw2,self.lines2) = re.split(':',hw2)
        self.dicts1=[] # list of dictionaries containing hw1
        self.dicts2=[] # ... hw2
    #def __repr__(self):
    #    return "Sanhw[%s]"%self.line

def parse_chksort1(filename):
 with open(filename,'r') as f:
  recs = [Chksort(x) for x in f ] 
 return recs

class Sanhw(object):
    def __init__(self,line):
        line = line.rstrip('\r\n')
        self.line =line
        self.n = None # subscript . Filled in later
        (self.key,self.dictstr)=re.split(r':',line)
        self.dicts = re.split(',',self.dictstr)
    def __repr__(self):
        return "Sanhw[%s]"%self.line

def init_sanhws(filename):
 with open(filename,'r') as f:
  sanhws = [Sanhw(x) for x in f if (not x.startswith(':'))]  # skip ':AP90'
 return sanhws
 
def main1():
 filein = sys.argv[1] #chksort1.txt
 filein1 = sys.argv[2] #sanhw1.txt
 fileout = sys.argv[3] #chksort1a.txt
 fileout1 = sys.argv[4] #chksort1a_rest.txt
 fileout2 = sys.argv[5] #chksort1a_singletons.txt
 recs = parse_chksort1(filein)
 sanhws = init_sanhws(filein1)
 # make dictionary on sanhws
 sanhws_dict = {}
 for sanhw in sanhws:
  sanhws_dict[sanhw.key] = sanhw
 # generate output
 nout=0
 nout1=0
 nout2=0
 singles={}
 fout = open(fileout,'w')
 fout1 = open(fileout1,'w')
 fout2 = open(fileout2,'w')
 for rec in recs:
  if rec.hw1 in sanhws_dict:
   rec.dicts1 = sanhws_dict[rec.hw1].dicts
  if rec.hw2 in sanhws_dict:
   rec.dicts2 = sanhws_dict[rec.hw2].dicts
  # 
  if (len(rec.dicts1) > 1) and (len(rec.dicts2) > 1):
   fout1.write("%s\n" %rec.line)
   nout1 = nout1+ 1
  else:
   outarr=[]
   outarr.append('%02d' % len(rec.dicts1))
   outarr.append('%02d' % len(rec.dicts2))
   outarr.append(' %s' % rec.line)
   out = ''.join(outarr)
   fout.write("%s\n" % out)
   nout = nout + 1
   if (len(rec.dicts1) == 1) and (rec.hw1 not in singles):
    singles[rec.hw1]=True
    nout2=nout2+1
    fout2.write("%s\n" % rec.hw1)
   if (len(rec.dicts2) == 1) and (rec.hw2 not in singles):
    singles[rec.hw2]=True
    nout2=nout2+1
    fout2.write("%s\n" % rec.hw2)
 fout.close()
 fout1.close()
 fout2.close()
 print nout,"lines written to ",fileout
 print nout1,"lines written to ",fileout1
 print nout2,"lines written to ",fileout2

if __name__=="__main__":
 main1()
