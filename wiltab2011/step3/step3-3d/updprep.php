<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
 updprep.php
 08-13-2011 ejf
 11-30-2011

 Reads records from a certain file format, which contains, in each line,
  - wilkey    current wilson key, in SLP spelling
  - wilcorr   correction to wilson key, in SLP spelling
First, these two data are changed to HK spelling: wilkey1, wilcorr1
A list of (possibly more than 1) records of wiltab for which the 'key'
column = wilkey1.  (An error if no such records found)
For each of these records, 
  the lnum is noted
  in the 'data' column, <key1>and <key2> elements are changed from
     wilkey1 to wilcorr1
  a triple of records in written to output file.
*/

$filein = $argv[1];
$fileout = $argv[2];
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
$fpout = fopen($fileout,"w") or die("Can't open $fileout\n");

// prepare for db access
$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}
$n=0;
$nchg=0;
while (!feof($fpin)) {
 $x = fgets($fpin);
 $x = preg_replace('|\r|','',$x);
 $x = trim($x);
 if ($x == ''){
 if(!feof($fpin)) {  fwrite($fpout,"$x\n");  }
  continue;
 }
 $n++;
 if(!preg_match('|<rule |',$x)) {
  fwrite($fpout,"$x\n");  
  continue;
 }
 // encapsulate with <r> element to satisfy dtd
 $x = "<r>$x</r>";
 // parse to get wilkey,wilcorr
 if(!preg_match('/<wil(.*?)>(.*?)<\/wil>.*?<mw>(.*?)<\/mw>/',$x,$matches)) {
//  echo "line skipped: $x\n";
  fwrite($fpout,"$x\n");
  continue;
 }
 $wilattr=$matches[1];
 $wilkey=$matches[2];
 $mwkey =$matches[3];
 $corrflag=false;
 if (preg_match('|class="ERROR".*cclass="_">y|',$x)) {
  $corrflag=true;
 }else if (preg_match('|cclass="E"|',$x)) {
  $corrflag=true;
 }else if (preg_match('|corr="|',$x)) {
  $corrflag=true;
 }
 if (!$corrflag) {
  // no further processing required
  fwrite($fpout,"$x\n");
  continue;
 }
 if (preg_match('/ corr="(.*?)"/',$wilattr,$matches)) {
  // prefer the corr attribute if it is there.
  $wilcorr = $matches[1];
 }else if ($mwkey == '*') {
  //echo "ERROR SKIPPING: no correction!\n$x\n\n";
  fwrite($fpout,"$x\n");
  continue;
 }else {
  $wilcorr = $mwkey;
 }
 // Make note to standard output if corrected wilson key differs from mwkey
 if ($wilcorr != $mwkey) {
  echo "Why is wilcorr != mwkey?:\n$x\n\n";
  fwrite($fpout,"$x\n");
  continue;
 }
 // double-check that mwkey is an mw headword
 $records = find_monier($mwkey);
 if (count($records) == 0) {
  if ($mwkey != '*') {
   echo "WARNING: MW key not found: $mwkey\n$x\n\n";
  }
 }

 // convert wilkey, wilcorr from SLP1 to HK
 $wilcorr1 = transcoder_processString($wilcorr,"slp1","hk");
 $wilkey1 =  transcoder_processString($wilkey,"slp1","hk");

 // get list of (old) records using wilkey1
 $records = find_wiltab($wilkey1);
 $records_corr = find_wiltab($wilcorr1);
 if ((count($records) == 0) and (count($records_corr) != 0)) {
  // correction has been made. Add attribute to rule
  $y = preg_replace("|(<rule .*?)>|","$1 corrected=\"y\">",$x);
  $nchg++;
  fwrite($fpout,"$y\n");
  continue;
 }
 if ((count($records) != 0) and (count($records_corr) != 0)) {
  echo "ERROR SKIPPING: old wilkey = $wilkey, corr wilkey = $wilcorr:  both are found\n$x\n\n";
  fwrite($fpout,"$x\n");
  continue;
 }
 if (count($records) == 0) {
  echo "ERROR SKIPPING: no records in wiltab for key=$wilkey1\n$x\n\n"; 
  fwrite($fpout,"$x\n");
  continue;
 }
 // Still an error
  fwrite($fpout,"$x\n");
  continue;
}
fclose($fpin);
fclose($fpout);
echo "$n records read from $filein\n";
echo "$nchg records altered\n";
exit;
function find_wiltab($key) {
 $table = 'wiltab';
 $sql = "select `key`,`lnum`,`data` from `$table` where `key`='$key'";
 $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
 $records = array();
 while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
  if ($line['key'] != $key) {continue;}
  $record = array($line['key'],$line['lnum'],$line['data']);
  $records[]=$record;
 }
 return $records;
}
function find_monier($key) {
 $table = 'monier';
 $sql = "select `key`,`lnum`,`data` from `$table` where `key`='$key'";
 $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
 $records = array();
 while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
  if ($line['key'] != $key) {continue;}
  $record = array($line['key'],$line['lnum'],$line['data']);
  $records[]=$record;
 }
 return $records;
}
?>
