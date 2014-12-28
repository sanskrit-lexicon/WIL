<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#likely.php
# 03-03-2011
#reads file like wiltab_mw-3-3.txt and creates
# (a) an xml file
# (b) an html file
# Filters on 'conf="LIKELY"' (just shows these records).
# Based on example from Matthias Ahlborn.
*/

$filein = $argv[1];
$fileout1 = $argv[2];
$fileout2 = $argv[3];
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
$fpout1 = fopen($fileout1,"w") or die("Can't open $fileout1\n");
$fpout2 = fopen($fileout2,"w") or die("Can't open $fileout2\n");

$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}
$more= 1;
$dbg=0; #0 for no dbg, 1 for dbg
$nfound=0;
$notfound=0;
$nspellchg=0;
$nauto=0;
$ncorr=0;
$nout1=0;
$nbadkey=0;
$nkey=0;
$lines=array();
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  $nkey++;
  if (!preg_match('/<rule conf="LIKELY"/',$x)) {continue;}
  $nkey++;
  $lines[]=$x;
 }
fclose($fpin);
// generate xml
fwrite($fpout1,'<?xml version="1.0" encoding="UTF-8"?>' . "\n");
fwrite($fpout1,'<!DOCTYPE LEX SYSTEM "lex.dtd" []>' . "\n");
fwrite($fpout1,'<LEX>' . "\n");
foreach($lines as $x) {
 fwrite($fpout1,"<r>$x</r>\n");
}
fwrite($fpout1,'</LEX>' . "\n");
fclose($fpout1);
// generate html
$hrefwil = 'http://www.sanskrit-lexicon.uni-koeln.de/scans/WILScan/disp3/index.php?filter=SktDevaUnicode&translit=SLP1&key='; 
$hrefmw = 'http://www.sanskrit-lexicon.uni-koeln.de/monier/indexcaller.php?filter=SktDevaUnicode&translit=SLP1&key=';
fwrite($fpout2,"<html>\n");
fwrite($fpout2,"<head>\n");
$title = preg_replace('|[.].*$|','',$filein);
fwrite($fpout2,"<title>$title</title>\n");
$css = "<style type='text/css'>\n";
$css .= "table, th, td{border: 1px solid black;}\n";
$css .= "td, th{text-align:left; padding:15px}\n";
$css .= "table {border-collapse:collapse;}\n";
$css .= "th {background-color: lightgrey;}\n";
$css .= "</style>\n";
fwrite($fpout2,"$css");
fwrite($fpout2,"</head>\n");
fwrite($fpout2,"<body>\n");
fwrite($fpout2,"<table>\n");
fwrite($fpout2,"<tr><th>count</th><th>rule</th><th>class</th><th>Wilson</th><th>MW</th></tr>\n");
$nx=0;
foreach($lines as $x) {
 $nx++;
 if (!preg_match('|<rule .*? class="(.*?)".*?>([^<]*)</rule>.*<wil.*?>(.*?)</wil>.*<mw>(.*?)</mw>|',$x,$matches)) {
  echo "error (html) in: $x\n";
  continue;
 }
 $class = $matches[1];
 $rule = $matches[2];
 $wil = $matches[3];
 $mw = $matches[4];
 if (!find_wilkey_basic($wil)) {
  echo "Not in wiltab: '$wil' : $x\n";
  continue;
 }
 if (!find_mwkey_basic($mw)) {
  echo "Not in monier: '$mw' : $x\n";
  continue;
 }
 $href = $hrefwil . $wil;
 $awil = "<a target=\"WIL\" href=\"$href\">$wil</a>";
 $href = $hrefmw . $mw;
 $amw = "<a target=\"MW\" href=\"$href\">$mw</a>";
 $out = "<tr><td>$nx</td><td>$rule</td><td>$class</td><td>$awil</td><td>$amw</td></tr>";
 fwrite($fpout2,"$out\n");
}
fwrite($fpout2,"</table>\n");
fwrite($fpout2,"</body>\n");
fwrite($fpout2,"</html>\n");
fclose($fpout2);

echo "$nkey keys processed from $filein\n";
$nout = count($lines);
echo "$nout records written to $fileout1\n";
echo "$nout records written to $fileout2\n";
exit;
function find_mwkey_basic($slp) {
    $table = 'monier';
    $slp1 = preg_replace("|'|","\\'",$slp);
    $sql = "select `key`,`data` from `$table` where `key`='$slp1'";
    $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
    $nfound1=0;
    while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
	$data1 = $line['data'];
	$key1 = $line['key'];
	if ($key1 == $slp) {
	    $nfound1++;
	}
    }
    if ($nfound1>0) {
	return $slp;
    }
    return '';
}
function find_wilkey_basic($slp) {
// assume $slp is SLP transliteration. 'Native' keys in wiltab are in hk.
    $hk = transcoder_processString($slp,'slp1','hk');
    $table = 'wiltab';
    $hk1 = preg_replace("|'|","\\'",$hk);
    $sql = "select `key`,`data` from `$table` where `key`='$hk1'";
    $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
    $nfound1=0;
    while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
	$data1 = $line['data'];
	$key1 = $line['key'];
	if ($key1 == $hk) {
	    $nfound1++;
	}
    }
    if ($nfound1>0) {
	return $slp;
    }
    return '';
}
?>
