* step4/step4-1 Dec 2, 2011

Originally, the list that Sampada/Peter corrected was based on the
records of wiltab_mw-3-3.txt that had conf="LIKELY".  For various reasons,
5 of these records are not represented in wilss-3-3d.xml.  Why?
The step4-1-notes.txt file explains the discrepancies.
files wiltab_mw-4-1.txt and wilss-4-1.xml correct the discrepancies.
There are approximately 8350 records in wiltab_mw-4-1.txt, representing
wilson headwords not found in mw.  
wilss-4-1.xml explains 943 of these.
It remains to explain the rest.
* step4/step4-2 Dec 3, 2011
Here the inputs are the two files wiltab_mw-4-1.txt and wilss-4-1.xml. 
Also, lex.dtd
No changes are anticipated in wilss-4-1.xml: this is completed work.
The objectives here are to:
(a) get all the records in wiltab_mw-4-1.txt into a form validateable
    by lex.dtd  (we'll call it wilmw-4-2.xml)
(b) Do an initial partition of wilmw-4-2.xml into various piles:
   (b1)  conf=LIKELY  -  these are the ones corresponding to wilss-4-1.xml
                         they are done
   (b2)  conf=SURE    -  MA marked these as sure -  after a brief
                         perusal to confirm MA's assessment, these will also
                         be done.
   (b3)  conf=ROOT    -  some root problems.  Will prob. need corrections to
                         wiltab headwords.
   (b4)  NO conf      -  This is the hard part. Slightly below 5000 of these.

The resulting files:
 wiltab_mw-4-2-likely.xml   943 records
 wiltab_mw-4-2-sure.xml    2447 records
 wiltab_mw-4-2-root.xml      92 records
 wiltab_mw-4-2-todo.xml    4869 records

Further, the 'todo' file has been separated into 5 files, based on the
 value of the 'class' attribute:

wiltab_mw-4-2-todo-error.xml     112 records
wiltab_mw-4-2-todo-variant.xml    61 records
wiltab_mw-4-2-todo-grammar.xml   249 records
wiltab_mw-4-2-todo-issue.xml       8 records
wiltab_mw-4-2-todo-todo.xml     4439 records

There are html files for all these xml files.

