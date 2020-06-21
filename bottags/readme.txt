
The purpose here is to:
1. develop text fragments from the Wilson dictionary which should be 
   tagged as 'bot' or 'bio'.  These are the same MW tags used to tag
   scientific names of plants and animals, respectively.
2. Programmatically add the bot and bio tags to the instances of the
   text fragments in wil.txt.  

We start with:
1. wil_botany.txt.  a list of text fragments [ref: https://github.com/sanskrit-lexicon/WIL/issues/11]
2. mw_bot.txt and mw_bio.txt:  list of text fragments already marked as 
   'bot' or 'bio' in the Monier-Williams dictionary.
   Ref: https://github.com/sanskrit-lexicon/MWS/issues/74


First step is to categorize the distinct text fragments in wil_botany.txt 
  according to whether a fragment matches one of the plant names of mw.

python matchmw.py wil_botany.txt .3./../MWS/botbio/mw_bot.txt wil_mwbot.txt wil_not_mwbot.txt

Outputs:  
1. wil_mwbot.txt   Text fragments from wil_botany.txt that have a 'bot' tag in MW.  A count of # of occurences in wil_botany.txt is also shown.
2. wil_not_mwbot.txt The remaining text fragments from wil_botany.txt

Second step is to do a lengthy manual examination of fragments in
wil_not_mwbot.txt in light of their context in wil.txt.

This involves manual editing of both wil_mwbot.txt and wil_not_mwbot.txt.

There is also a wil_bio.txt,  which contain text fragments representing 
scientific names of animals in Wilson.

In these three files, lines that start with a semicolon are comment lines.
Occasionally, the first word of a scientific name was abbreviated.
    For example C. reclinata, Rox.  When noticed, such fragments were 
    added to wil_not_mwbot.txt



Numerous changes were made to the wil.txt digitization.  
A scientific name usually has two words.  Sometimes, the first word was
    at the end of one line, and the second word at the beginning of the 
    next line in wil.txt.  The change here moved the second word to the first
    line.  This was the most common kind of change to wil.txt.
For these changes, see this commit of csl-orig repository:
https://github.com/sanskrit-lexicon/csl-orig/commit/a7657a1b3ea82c79d6335142e1d4b1f78640c195

There still remain spelling variations which likely need to be corrected in
the scientific names.  


Step 3:  Aggregation of scientific names of plants: wil_bot.txt

python catbot.py  wil_mwbot.txt wil_not_mwbot.txt wil_bot.txt

386 records found in wil_mwbot.txt
350 records found in wil_not_mwbot.txt
merge duplicate: hedysarum lagopodioides
merge duplicate: capparis trifoliata
merge duplicate: sarcostema viminalis
merge duplicate: verbesina scandens
merge duplicate: achyranthes aspera
merge duplicate: acorus calamus
merge duplicate: boerhavia diffusa alata
merge duplicate: pentapetes phoenicea
merge duplicate: phaseolus mungo
merge duplicate: phaseolus radiatus
merge duplicate: trichosanthes dioeca
merge duplicate: wrightea antidysenterica
724 merged text fragments

2484 instances in 724 records written to wil_bot.txt

2484 is only a rough approximation of the number of
botany tag instances in wil.txt.


Next step is to tag the text fragments.
This is somewhat complicated by the fact that the fragments are not 'disjoint'.
For example, the two fragments 'Pistia' and 'Pistia stratiotes' have the
common word 'Pistia'.
We choose to generate a 'change' file  (a 'manualByLine') file.
Then we will use that file to make alterations to wil.txt.

python tag_changes.py bio wil_bio.txt ../../../cologne/csl-orig/v02/wil/wil.txt manualByLine_bio.txt

python updateByLine.py ../../../cologne/csl-orig/v02/wil/wil.txt manualByLine_bio.txt temp_bio_wil.txt

python tag_changes.py bot wil_bot.txt temp_bio_wil.txt manualByLine_bot.txt

python updateByLine.py temp_bio_wil.txt manualByLine_bot.txt temp_bot_wil.txt

Now, copy temp_bot_wil.txt to csl-orig/v02/wil/wil.txt
etc.  

This completes the installation of markup of 'bot' and 'bio' in Wilson 
Dictionary.
