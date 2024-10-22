Aug 13, 2011
These notes describe updates to wiltab and monier tables on Cologne server
based upon the file wilSStil722PMStil946.xml provided by pms.
Overview:
Some changes were made to wilSStil722PMStil946.xml to make it a well-formed
xml file and to reflect the correction of some mw errors.
Then, the records in the file were assigned to one of two files:
  filter1-3.txt contains records requiring corrections to wiltab database
  rest3.txt  contains other kinds of records.
             Note: rest-sort.txt is simply an alphabetical sort of rest3.txt;
                   this means alphabetical in the non-sanskrit text-editor
                   sense.
Finally, the records from filter1-3.txt were used to generate updates to
  the wiltab database.  In this process, a few observations in 'notes.txt'
  were generated, which may suggest a few remapping records be added to
  rest3 (but these additions were not done by ejf).

The balance of this file contains notes written during the implementation
just described in the overview.
Note:  wiltab corrections on Cologne server in directory
   scans/WILScan/mysql/wiltab/update/maprep/step4

ejf changes to file wilSStil722PMStil946.xml 
1. removed 2 lines
This was an mw error, now corrected.
<rule conf="LIKELY" class="ERROR">CA/Co</rule> <c auth="PS" cclass="Q">MW 1205a bottom 4SAma has sAmayoni</c> <wil>sAmayoni</wil> <mw>somayoni</mw>

This was an mw error, now corrected:
<rule conf="LIKELY" class="GRAMMAR">tA</rule> <c auth="PS" cclass="Q">Printed MW has the form on p. 1198, col. 1 under sAkzi2.</c> <wil>sAkzitA</wil> <mw>sAkzitA</mw>

2. changed a couple of lines with xml errors, discovered by Oxygen.
3. commented out dtd line so oxygen would confirm xml well-formed.
Note 1: the original is in subdirectory old.  
Note 2: a 'diff' on the original and changed confirms (1-3) just mentioned
  account for the differences introduced by ejf.

file parts:

1.  input = full file wilSStil722PMStil946.xml  
      (942 rule lines, 946 total lines)
    selection:  class="ERROR".*cclass="_">y
    output = filter1.txt  (162 lines)
1a. input = wilSStil722PMStil946.xml
    selection (exclude): class="ERROR".*cclass="_">y
    output = rest1.txt  (778 lines)
(So now the starting file (wilSS....xml) is partitioned into two
  parts filter1.txt and rest1.txt)
2.  input = rest1.txt
    selection: cclass="E"
    output = filter2.txt (63 lines)

2a.  input = rest1.txt
    selection (exclude): cclass="E"
    output = rest2.txt  (717 lines)
(so now rest1 is partitioned into filter2.txt and rest2.txt)

3.  input = rest2.txt
    selection:   corr="
    output = filter3.txt (9 lines)

3a.  input = rest2.txt
    selection (exclude):   corr="
    output = rest3.txt  (708 lines)
(now rest2 is partitioned into filter3 and rest3)
--------------------------------------------------------
Notes of Aug 13, 2011:
1a. (filter1)
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="SS" cclass="_">y</c> <wil>gurupatra</wil> <mw>gurupattra</mw>

This type of difference is treated differently elsewhere

2a. In filter1, for those (12) records which have a 'corr' attribute for <wil>
element, the value of the corr attribute is identical to the contents of the
<mw> element.  (i.e., the 'corr' attribute is redundant and could be ignored)


2b. In filter2, the above generally holds, except:
2b1. mw has *  here, we definitely need to use the corr attribute.
nil<rule conf="LIKELY" class="ERROR">Ca/Cf</rule> <c auth="SS" cclass="E">Additionally correct udB to udJ in the def.  Probably need to correct entry uYBa m. to uYJa m.</c> <wil err="scan" corr="udJa">udBa</wil> <mw>*</mw>

2b2.  this looks wrong.  ejf to look again
  do we really correspond KastanI and KelanI ?
  no: mw has KastanI.   We need to use the corr attribute value.
      ejf changed filter2 to have mw field = KastanI
<rule conf="LIKELY" class="ERROR">Ca/Ce</rule> <c auth="PS" cclass="E">different words,KalanI not there in Wil scan. PMS: The etymology of the word in the definition and the alphabetic order reveal the error.</c> <wil err="typo" corr="KastanI">KalanI</wil> <mw>KelanI</mw>

2b3. ejf: Do we really correspond mahIyas and sahIyas?
 no:  mw has mahIyas.  ejf changed mw field to mahIyas
<rule conf="LIKELY" class="ERROR">m/s</rule> <c auth="PS" cclass="E">SS: entry should have been mahIyas. PMS: right, but algorithm mad two substitutions instead of just one. Added attributes.</c> <wil err="typo" corr="mahIyas">mahIyam</wil> <mw>sahIyas</mw>


2b4. ejf note: mw key here is the masculine: sUkzmamakzika.  which shows f(A) form.  ejf change mw element from 'sUkzma--makzikA' to sUkzmamakzika.
<rule conf="LIKELY" class="ERROR">Ca/Ce</rule> <c auth="PS" cclass="E">MW has correct entry too [L=250964] but not found upon ordinary search; only found with prefix search in advanced search.</c> <wil err="typo" corr="sUkzmamakzikA">sUkzmakzikA</wil> <mw>sUkzmamakzika</mw>

This little mosquito points up a subtle point regarding the correspondence
implied by having <wil>sUkzmamakzikA</wil> and <mw>sUkzmamakzika</mw> shown
as corresponding.
The correspondence appropriately joins two headwords from the two lexica.
After the corrections, the entry should probably be reinserted into 'rest3', 
with a different class.

2c. This record removed from filter2.
    avAcIna  appears as headword in both Wilson and MW
<rule conf="LIKELY" class="ERROR">VC/VrC</rule> <c auth="SS" cclass="E">word missing from digital MW, appears in printed text on p. 106, col. 3 bottom</c> <wil>avAcIna</wil> <mw>avAcIna</mw>

2d. This record removed from filter2.
   sammAda appears as headword in both Wilson and MW.
<rule conf="LIKELY" class="ERROR">CA/Co</rule> <c auth="PS" cclass="E">MW entry missing.  MW p. 1180a has sam-mAda, but digital edition doesn't.</c> <wil>sammAda</wil> <mw>sammAda</mw>

2e.  ejf added headword 'hrUq' to MW.
<rule conf="LIKELY" class="ERROR">Ca/Cu</rule> <c auth="PS" cclass="E">Delete final 'a' from Wilson entry, since final marker is 'f'.  MW has 'hruq' or 'hrUq' so should add 'hrUq'</c> <wil err="fac" corr="hrUq">hrUqa</wil> <mw>hrUq</mw>

2f. 'apsa' in MW has been removed as a headword.
  This record removed from filter2.txt
<rule conf="LIKELY" class="ERROR">Ca/Cu</rule> <c auth="SS" cclass="E">It's not a headword!  Continuation of previous entry apsaras.</c> <wil err="scan" corr="apsu">apsa</wil> <mw>apsu</mw>


3. filter3
3a.
<rule conf="LIKELY" class="ERROR">Ca/Cu</rule> <c auth="PS" cclass="G">SS: very similar but diff words. PMS: remapped to MW root; participle: prap of causative of prAR.</c> <wil err="scan" corr="prARayat">prARayata</wil> <mw>prAR</mw>

 This is an example of a word which, after correction of an error,
require a remapping (i.e.:  a record for this should be added to rest3.txt;
 perhaps with class="V" or class="GRAMMAR"

3b. This removed from filter2 after ejf made correction to mw.
<rule conf="LIKELY" class="ERROR">VC/VrC</rule> <c auth="PS" cclass="MW">SS: both words are right. PMS: MW correction; Wilson is correct.</c> <wil>parapAkanivftta</wil> <mw err="typo" corr="parapAkanivftta">parapAkanirvftta</mw>

4.  Merged filter1.txt, filter2.txt and filter3.txt into filter1-3.txt.
4a.  account for lines:
  filter1-3.txt has 230 data lines (plus 3 comment lines -- filter1.txt--- etc)
  rest3.txt has 708 lines
 
  (+ 231 708) = 939
  wilSStil722PMStil946.xml had 942 rule lines
  4 lines were removed:
   avAcIna (see 2c above)
   sammAda (see 2d above)
   apsa (se 2f above)
   parapAkanivftta (see 3b above)

So, all lines are accounted for.

4b.  Note on pattra types.
  There are 8 'errors' in filter1-3 of the 'pattra' type.
  in rest3, perhaps similar records (like hrasvapatraka) have been 
  given cclass="W".  
  I chose to process the 8 from filter1-3 as errors, 
  but, we may want to change these back in Wilson, and move these
  records to rest3 with a reclassification.

<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="SS" cclass="_">y</c> <wil>aBIrupatrI</wil> <mw>aBIrupattrI</mw>
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="SS" cclass="_">y</c> <wil>elApatra</wil> <mw>elApattra</mw>
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="SS" cclass="_">y</c> <wil>gurupatra</wil> <mw>gurupattra</mw>
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="PS" cclass="_">y</c> <wil>SyAmapatra</wil> <mw>SyAmapattra</mw>
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="PS" cclass="_">y</c> <wil>sapatrAkaraRa</wil> <mw>sapattrAkaraRa</mw>
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="PS" cclass="_">y</c> <wil>sapatrAkfti</wil> <mw>sapattrAkfti</mw>
<rule conf="LIKELY" class="ERROR">t/tt</rule> <c auth="PS" cclass="_">y</c> <wil>sarapatrikA</wil> <mw>sarapattrikA</mw>
<rule conf="LIKELY" class="ERROR">Ca/Cu</rule> <c auth="PS" cclass="E">SS: diff words,diff meanings. PMS: remapped t/tt</c> <wil>tripatra</wil> <mw>tripattra</mw>

5. Technical sva-ejf-note:
  The details of batch processing the records of filter1-3.txt appears in
  Cologne, in directory
  /afs/rrz.uni-koeln.de/vol/www/projekt/sanskrit-lexicon/http/docs/scans/WILScan/mysql/wiltab/update/maprep/step4/


Notes on corrections:
1. in filter1:   The wilson record is 'ciraRQI'  so this correction as
   written doesn't function.  It should  be re-examined.
  To make it work, ejf changed filter2 to have old wilson key of
  'ciraRQI':
  old record:
<rule conf="LIKELY" class="ERROR">q/w</rule> <c auth="PS" cclass="_">y SS: from scan doesn't look like error. PMS: yes, error</c> <wil err="typo" corr="ciraRwI">ciraRqI</wil> <mw>ciraRwI</mw>

 new record:
<rule conf="LIKELY" class="ERROR">q/w</rule> <c auth="PS" cclass="_">y SS: from scan doesn't look like error. PMS: yes, error</c> <wil err="typo" corr="ciraRwI">ciraRQI</wil> <mw>ciraRwI</mw>
