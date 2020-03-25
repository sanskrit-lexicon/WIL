
Analysis of shs verbs and upasargas, revised
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/shs/.

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

* shs_verb_filter.

python shs_verb_filter.py ../shs.txt shs_verb_exclude.txt shs_verb_include.txt shs_verb_filter.txt

shs_verb_exclude.txt contains metalines for records that are NOT verbs,
but that have some of the patterns for roots.  
shs_verb_include.txt contains metalines for records that are believed to be
verbs, but that are not identified by the verb patterns.
For shs, the exclude file has one entry, the include file is empty.

Patterns for roots: (same pattern as Wilson)
r '¦ +r[.] '    # r. appears just after the broken bar
s '¦.* r[.] '   # r. appears in the broken bar line, but later in the line.

This is the only pattern for verbs that is currently known.

Counts of total patterns:
1783 r
  15 s
1798 verbs written to shs_verb_filter.txt

Format of file shs_verb_filter.txt:
;; Case 0001: L=4, k1=aMSa, k2=aMSa, code=r

* The odd case of Danva
Danva in shs has both a nominal part and a root part.
I initially thought to break this into two records, but then decided not
to do this at this time.
Here is how the old (unchanged) and new (proposed change) would look in shs.txt:
old: Danva
<L>20359<pc>365-a<k1>Danva<k2>Danva
{#Danva#}¦ n. ({#-nvaM#}) A bow: see {#Danvan#}.{# Danva gatO sO0 BvA0 pa0 saka0 sew .#} r. 1st cl.
<>({#Danvati#}) To go.
<LEND>

new:
<L>20359<pc>365-a<k1>Danva<k2>Danva
{#Danva#}¦ n. ({#-nvaM#}) A bow: see {#Danvan#}.
<LEND>
<L>20359.1<pc>365-a<k1>Danva<k2>Danva
{#Danva#}¦ {# Danva gatO sO0 BvA0 pa0 saka0 sew .#} r. 1st cl. ({#Danvati#}) To go.
<LEND>

* shs_verb_filter_map
python shs_verb_filter_map.py shs_verb_filter.txt mwverbs1.txt shs_verb_filter_map.txt

Get correspondences between shs verb spellings and
 - shs verb spellings
 - mw verb spellings

Format of shs_verb_filter_map.txt:
 Adds a field mw=xxx to each line of shs_verb_filter.txt,
indicating the MW root believed to correspond to the SHS root.
For example, aMSa in SHS is believed to correspond to aMS in MW.
;; Case 0001: L=4, k1=aMSa, k2=aMSa, code=r, mw=aMS

In 44 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0056: L=6356, k1=iBa, k2=iBa, code=r, mw=?

These matches are determined by various empirical methods that seem
right to me at the time of this work.  I hope others will critique this work.


* preverb1.txt
python preverb1.py slp1 ../shs.txt shs_verb_filter_map.txt mwverbs1.txt shs_preverb1.txt shs_preverb1_dbg.txt

For each of the entries of shs_verb_filter_map.txt, the program analyzes the
text of SHS looking for upasargas.  An upsarga is identified by the pattern
`' [wW]ith [^.;]*#}'`, and then parsing the matches.  (see function 
find_upasargas).  The process is rather complicated.  
For debugging purposes, see shs_preverb1_dbg.txt.



In shs_preverb1.txt,
The number of upasargas found is reported on a line for the verb entry.
The first SHS verb entry has no upasargas:
;; Case 0001: L=4, k1=aMSa, k2=aMSa, code=r, #upasargas=0, mw=aMS (diff)

The root 'kala' has 1  preverb.  The MW spelling is 'kal'.
Three of the prefixed forms are found in MW, and one is not found.
```
;; Case 0148: L=9477, k1=kala, k2=kala, code=r, #upasargas=4 (3/1), mw=kal (diff)
01          A       kala                Akala                 Akal yes A+kal
02       pari       kala             parikala              parikal yes pari+kal
03         vi       kala               vikala                vikal no 
04        sam       kala              saMkala               saMkal yes sam+kal
```

Altogether, there are currently 920 'yes' cases, and 97 'no' cases.


There are many varied (sandhi) spelling changes which occur when certain combinations of upasargas
are combined with certain roots.  My derivation of these changes is empirical, by which
I mean a mis-mash of rules which lead to as many correspondences as possible.  Also, 
some of the spelling conventions of MW come into play.

1017 upasargas found in 261 SHS entries

---------------------------------------------------------------
shs_preverb1_deva.txt  Devanagari version of shs_preverb1.txt.
Most sanskrit words are transcoded into Devanagari, but parts of k2
are still in slp1.

python transcode_preverb1.py deva shs_preverb1.txt shs_preverb1_deva.txt





