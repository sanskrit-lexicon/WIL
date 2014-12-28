<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
 make3d.php
 12-01-2011  add done="y" attrib to 3c.  Change "y" text to ___
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
 // add done="y" to c elt
 $x = preg_replace('|<c([^>]*)>(.*?)</c>|','<c\1 done="y">\2</c>',$x);

 // If 'y' is contents of c element, replace it with triple underscore
 $x = preg_replace('|>y</c>|','>___</c>',$x);
 // if 'y ' starts c element, remove the 'y '
 $x = preg_replace('|>y ([^<]*)</c>|','>\1</c>',$x);
 if (preg_match('|>y(.*?)</c>|',$x,$matches)) {
   echo "y WARN: $x\n";
 }
  // if cclass = _, change cclass to correspond to class
  if (preg_match('|<mw(.*?)>[*]</mw>|',$x)) {
   // but don't do this if mwkey is '*'
  }else if (preg_match('| class="(.*?)".* cclass="_"|',$x,$matches)) {
   $class=$matches[1];
   
   if ($class == "GRAMMAR") {
    $cclass="G";
   }else if ($class == "ERROR") {
    $cclass="E";
   }else if ($class == "VARIANT") {
    $cclass="V";
   } else {
     $cclass="_"; // default
   }
   $x = preg_replace('| cclass="_"|'," cclass=\"$cclass\"",$x);
  }
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
