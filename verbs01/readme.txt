
Analysis of wil verbs and upasargas, revised
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/wil/.

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

* wil_verb_filter.

python wil_verb_filter.py ../wil.txt wil_verb_exclude.txt wil_verb_include.txt wil_verb_filter.txt

wil_verb_exclude.txt contains metalines for records that are NOT verbs,
but that have some of the patterns for roots.  
wil_verb_include.txt contains metalines for records that are believed to be
verbs, but that are not identified by the verb patterns.
For wilson, the include and exclude files are empty.


Patterns for roots: 
r '¦ +r[.] '    # r. appears just after the broken bar
s '¦.* r[.] '   # r. appears in the broken bar line, but later in the line.

Counts of total patterns:
1340 r
0415 s
1755 verbs written to wil_verb_filter.txt

Format of file wil_verb_filter.txt:
;; Case 0001: L=5, k1=aMSa, k2=aMSa, code=r

* wil_verb_filter_map
python wil_verb_filter_map.py wil_verb_filter.txt mwverbs1.txt wil_verb_filter_map.txt

Get correspondences between wil verb spellings and
 - wil verb spellings
 - mw verb spellings
Uses pw_mw_map_edit.txt  , which contains some correspondences
developed by earlier work with PW dictionary.

Format of wil_verb_filter_map.txt:
 Adds a field mw=xxx to each line of wil_verb_filter.txt,
indicating the MW root believed to correspond to the WIL root.
For example, aMSa in WIL is believed to correspond to aMS in MW.
;; Case 0001: L=5, k1=aMSa, k2=aMSa, code=r, mw=aMS

In 41 cases, no correspondence could be found. These use 'mw=?'. For example:
;; Case 0056: L=6358, k1=iBa, k2=iBa, code=r, mw=?

* wil_upasarga_ids.txt
 A temporary version of preverb1.py was run to identify entries with upasargas.
The L and k1 of these entries is in file wil_upasarga_ids.txt
There are 157 such entries.

* wil_new.txt
A temporary new version of wil.txt was made, 
to add markup to the records with upasargas so they are easier to handle.
python make_div.py ../wil.txt wil_upasarga_ids.txt wil_new.txt make_div_check.txt
Later, this new version was made the current version of wil.txt.

* preverb1.txt
python preverb1.py slp1 ../wil.txt wil_verb_filter_map.txt mwverbs1.txt wil_preverb1.txt

For each of the entries of wil_verb_filter_map.txt, the program analyzes the
text of WIL looking for upasargas.  An upsarga is identifed by the pattern
`'^<div n="p">[0-9 ]*[wW]ith (.*)$'`

For example, under root sf, the following line matches:
`<div n="p">With {#anu#} prefixed, `
Then the program parses this line to determine the 'anu' is an upasarga.
The parsing gets rather complex. For checking, a file
wil_upasarga_lines.txt was generated which shows the results of parsing,
separated into cases identified by an arbitrary code.
code = 0 are 8 irregular cases
code = 1 are 356 simple 1-upasarga cases
And 8 other variations.

On wil_preverb1.txt,
The number of upasargas found is reported on a line for the verb entry.
The first WIL verb entry has no upasargas:
;; Case 0001: L=5, k1=aMSa, k2=aMSa, code=r, #upasargas=0, mw=aMS (diff)

The root 'kala' has 4 preverbs.  'kala' is spelled 'kal' in MW.
Three of the prefixed forms are found in MW, and one is not found.
```
;; Case 0149: L=9482, k1=kala, k2=kala, code=r, #upasargas=4 (3/1), mw=kal (diff)
01          A       kala                Akala                 Akal yes A+kal
02       pari       kala             parikala              parikal yes pari+kal
03         vi       kala               vikala                vikal no 
04        sam       kala              saMkala               saMkal yes sam+kal
```

Altogether, there are currently 613 'yes' cases, and 69 'no' cases.


There are many varied (sandhi) spelling changes which occur when certain combinations of upasargas
are combined with certain roots.  My derivation of these changes is empirical, by which
I mean a mis-mash of rules which lead to as many correspondences as possible.  Also, 
some of the spelling conventions of MW come into play.

682 upasargas found in 157 WIL entries

---------------------------------------------------------------
wil_preverb1_deva.txt  Devanagari version of wil_preverb1.txt
python transcode_preverb1.py deva wil_preverb1.txt wil_preverb1_deva.txt

