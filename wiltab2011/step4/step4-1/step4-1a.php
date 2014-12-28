<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
# step4-1a.php
# 12-02-2011
#
*/

$filein1 = $argv[1];
$filein2 = $argv[2];
$fpin1 = fopen($filein1,"r") or die("Can't open $filein1\n");
$fpin2 = fopen($filein2,"r") or die("Can't open $filein2\n");


$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}
// construct hash on wil of lines in wilss-3-3d.xml
$wilsshash = array();
$n=0;
 while (!feof($fpin1)) {
  $x = fgets($fpin1);
  $x = trim($x);
  if ($x == ''){continue;}
  if (!preg_match('|<rule.*?</rule>|',$x)) {continue;}
  if (!preg_match('|<wil.*?>(.*?)</wil>|',$x,$matches)) {
   echo "Prob in $filein1\n$x\n";
   exit(0);
  }
  $n++;
  $key=$matches[1];
  $wilsshash[$key]=$x;
 }
fclose($fpin1);
echo "$n records in $filein1\n";
// construct hash on wil of lines in wiltab_mw-3.3.txt
// just consider LIKELY lines.
$wiltabhash = array();
$n=0;
 while (!feof($fpin2)) {
  $x = fgets($fpin2);
  $x = trim($x);
  if ($x == ''){continue;}
  $nkey++;
  if (!preg_match('|<rule.*?</rule>|',$x)) {continue;}
  if (!preg_match('|conf="LIKELY"|',$x)) {continue;}
  if (!preg_match('|<wil.*?>(.*?)</wil>|',$x,$matches)) {
   echo "Prob in $filein1\n$x\n";
   exit(0);
  }
  $n++;
  $key=$matches[1];
  $wiltabhash[$key]=$x;
 }
fclose($fpin2);
echo "$n records in $filein2\n";

//  are all records from file1 in file2?
$n=0;
foreach($wilsshash as $key=>$wilss) {
 if (!$wiltabhash[$key]) {
  $n++;
  echo "$n : $wilss\n";
 }
}
echo "The above $n records are in $filein1, but not in $filein2 \n";
//  are all records from file2 in file1?
$n=0;
foreach($wiltabhash as $key=>$wiltab) {
 if (!$wilsshash[$key]) {
  $n++;
  echo "$n : $wiltab\n";
 }
}
echo "The above $n records are in $filein2, but not in $filein1 \n";
exit(0);
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
// generate html
$hrefwil = 'http://www.sanskrit-lexicon.uni-koeln.de/scans/WILScan/disp3/index.php?filter=SktDevaUnicode&translit=SLP1&key='; 
$hrefmw = 'http://www.sanskrit-lexicon.uni-koeln.de/monier/indexcaller.php?filter=SktDevaUnicode&translit=SLP1&key=';
fwrite($fpout1,"<html>\n");
fwrite($fpout1,"<head>\n");
$title = preg_replace('|[.].*$|','',$filein);
fwrite($fpout1,"<title>$title</title>\n");
$css = "<style type='text/css'>\n";
$css .= "table, th, td{border: 1px solid black;}\n";
$css .= "td, th{text-align:left; padding:15px}\n";
$css .= "table {border-collapse:collapse;}\n";
$css .= "th {background-color: lightgrey;}\n";
$css .= "</style>\n";
fwrite($fpout1,"$css");
fwrite($fpout1,"</head>\n");
fwrite($fpout1,"<body>\n");
fwrite($fpout1,"<table>\n");
fwrite($fpout1,"<tr><th>count</th><th>rule</th><th>class</th><th>Wilson</th><th>MW</th><th>Comment</th></tr>\n");
$nx=0;
foreach($lines as $x) {
 $nx++;
 if (!preg_match('|<rule([^>]*)>(.*?)</rule> *<c([^>]*)>(.*?)</c> *<wil([^>]*)>(.*?)</wil> *<mw([^>]*)>(.*?)</mw>|',$x,$matches)) {
  echo "error (html) in: $x\n";
  continue;
 }
 $ruleattr=$matches[1];
 $ruletext = $matches[2];
 $cattr=$matches[3];
 $ctext=$matches[4];
 $wilattr=$matches[5];
 $wiltext=$matches[6];
 $mwattr=$matches[7];
 $mwtext=$matches[8];
 if (preg_match('|class="(.*?)"|',$ruleattr,$matches)) {
  $class=$matches[1];
 }else {
  echo "PROGERR: $x\n";
  exit(0);
 }
 if (preg_match('|corrected="(.*?)"|',$ruleattr,$matches)) {
  $corrected=true;
  $class = $class . "<br/>CORRECTED";
 }else {
  $corrected=false;
 }
 $rule = $ruletext;
 $wil = $wiltext;
 $mw = $mwtext;

 // get $awil
 if ($corrected) {
  if (preg_match('/ corr="(.*?)"/',$wilattr,$matches)) {
   // prefer the corr attribute if it is there.
   $wilcorr = $matches[1];
  }else if ($mw == '*') {
   echo "ERROR : no correction!\n$x\n\n";
   exit(0);
  }else {
   $wilcorr = $mw;
  }
  if (find_wilkey_basic($wilcorr)) {
   $awil = "$wil<br/><a target=\"WIL\" href=\"$href\">$wilcorr</a>";
  }else {
   $awil = "$wil<br/><span color=\"RED\">$wilcorr</span>";
  }
 }else {
  // not a correction
  if (find_wilkey_basic($wil)) {
   $href = $hrefwil . $wil;
   $awil = "<a target=\"WIL\" href=\"$href\">$wil</a>";
  }else {
   $awil = "<span color=\"RED\">$wil</span>";
  }
 }
 
// get $amw
 if (find_mwkey_basic($mw)) {
  $href = $hrefmw . $mw;
  $amw = "<a target=\"MW\" href=\"$href\">$mw</a>";
 }else {
  $amw = "<span color=\"RED\">$mw</span>";
 }

 // get $acomment
 $cauth = "?";
 $cclass= "?";
 $cdone= "?";
 if(preg_match('| auth="(.*?)"|',$cattr,$matches)) {
  $cauth = $matches[1];
 }
 if(preg_match('| cclass="(.*?)"|',$cattr,$matches)) {
  $cclass = $matches[1];
 }
 if(preg_match('| done="(.*?)"|',$cattr,$matches)) {
  $cdone = $matches[1];
 }
 $acomment = "$cauth:$cclass:$cdone $ctext";
 // construct table row and output
 $out = "<tr><td>$nx</td><td>$rule</td><td>$class</td><td>$awil</td><td>$amw</td><td>$acomment</td></tr>";
 fwrite($fpout1,"$out\n");
}
fwrite($fpout1,"</table>\n");
fwrite($fpout1,"</body>\n");
fwrite($fpout1,"</html>\n");
fclose($fpout1);

echo "$nkey keys processed from $filein\n";
$nout = count($lines);
echo "$nout records written to $fileout1\n";
echo "$nout records written to $fileout1\n";
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
