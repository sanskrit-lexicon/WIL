
Analysis of yat verbs and upasargas, revised
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/yat/.

The shell script redo.sh reruns 5 python programs, from mwverb.py to preverb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* yat_verb_filter.

python yat_verb_filter.py ../yat.txt yat_verb_exclude.txt yat_verb_include.txt yat_verb_filter.txt

yat_verb_exclude.txt contains metalines for records that are NOT verbs,
but that have some of the patterns for roots.  
yat_verb_include.txt contains metalines for records that are believed to be
verbs, but that are not identified by the verb patterns.
For yat, the exclude file has one entry, the include file is empty.


Patterns for roots: 
r '¦.*t[ie]#}'    # Yates shows 3s forms typically at start of verb entry

This is the only pattern for verbs that is currently known.

Counts of total patterns:
1738 r

1738 verbs written to yat_verb_filter.txt

Format of file yat_verb_filter.txt:
;; Case 0001: L=3, k1=aMSa, k2=aMSa, code=r

* yat_verb_filter_map
python yat_verb_filter_map.py yat_verb_filter.txt mwverbs1.txt yat_verb_filter_map.txt

Get correspondences between yat verb spellings and
 - yat verb spellings
 - mw verb spellings

Format of yat_verb_filter_map.txt:
 Adds a field mw=xxx to each line of yat_verb_filter.txt,
indicating the MW root believed to correspond to the YAT root.
For example, aMSa in YAT is believed to correspond to aMS in MW.
;; Case 0001: L=5, k1=aMSa, k2=aMSa, code=r, mw=aMS

In 45 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0065: L=4061, k1=asta, k2=asta, code=r, mw=?

These matches are determined by various empirical methods that seem
right to me at the time of this work.  I hope others will critique this work.


* preverb1.txt
python preverb1.py slp1 ../yat.txt yat_verb_filter_map.txt mwverbs1.txt yat_preverb1.txt yat_preverb1_dbg.txt

For each of the entries of yat_verb_filter_map.txt, the program analyzes the
text of YAT looking for upasargas.  An upsarga is identifed by the pattern
`' [wW]ith [^.;]*#}'`, and then parsing the matches.  (see function 
find_upasargas).  The process is rather complicated.

NOTE:  In root 'hf',  there are further complications for some of the
upasargas mentioned towards the end of the entry; these are known to
be handled improperly.
```
 Some of these
<>compounds again take preposi-
<>tions; thus {#A#} with {#aBi#} or {#vi#}
<>prefixed, to say, utter, converse;
<>with {#nira,#} to fast; with {#sama#} or
<>{#ut,#} to relate. So also {#sama,#} with
<>{#upa#} prefixed, to withhold; with
<>{#prati,#} to disregard, withdraw.
<>{#ava#} with {#vi#} prefixed, to litigate,
```


On yat_preverb1.txt,
The number of upasargas found is reported on a line for the verb entry.
The first YAT verb entry has no upasargas:
;; Case 0001: L=5, k1=aMSa, k2=aMSa, code=r, #upasargas=0, mw=aMS (diff)

The root 'kala' has 1  preverb.  The MW spelling is 'kal'.
Three of the prefixed forms are found in MW, and one is not found.
```
;; Case 0180: L=8916, k1=kala, k2=kala, code=r, #upasargas=4 (3/1), mw=kal (diff)
01          A       kala                Akala                 Akal yes A+kal
02       pari       kala             parikala              parikal yes pari+kal
03         vi       kala               vikala                vikal no 
04        sam       kala              saMkala               saMkal yes sam+kal
```

Altogether, there are currently 584 'yes' cases, and 70 'no' cases.


There are many varied (sandhi) spelling changes which occur when certain combinations of upasargas
are combined with certain roots.  My derivation of these changes is empirical, by which
I mean a mis-mash of rules which lead to as many correspondences as possible.  Also, 
some of the spelling conventions of MW come into play.

654 upasargas found in 170 YAT entries

---------------------------------------------------------------
yat_preverb1_deva.txt  Devanagari version of yat_preverb1.txt
python transcode_preverb1.py deva yat_preverb1.txt yat_preverb1_deva.txt
