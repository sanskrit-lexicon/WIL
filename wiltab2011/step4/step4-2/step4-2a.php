<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
# step4-2a.php
# 12-03-2011
# convert wiltab_mw-4-1.txt to the xml structure of lex.dtd.
*/

$filein1 = $argv[1];
$fileout2 = $argv[2];
$fpin1 = fopen($filein1,"r") or die("Can't open $filein1\n");
$fpout2 = fopen($fileout2,"w") or die("Can't open $fileout2\n");


$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}
// Initial xml lines
$header = array('<?xml version="1.0" encoding="UTF-8"?>',
  '<!DOCTYPE LEX SYSTEM "lex.dtd" []>',
  '<LEX>');
foreach($header as $x) {
 fwrite($fpout2,"$x\n");
}
$n=0;
 while (!feof($fpin1)) {
  $x = fgets($fpin1);
  $x = trim($x);
  if ($x == ''){continue;}
  // There are two kinds of lines: those starting with <rule
  // and those starting with <c
  if (preg_match('|^<rule|',$x)) {
   $y = process_rule($x);
  }else if (preg_match('|^<c|',$x)) {
   $y = process_c($x);
  }else {
   echo "UNKNOWN: $x\n";
   continue;
  }
  fwrite($fpout2,"$y\n");
 }
fclose($fpin1);
// close root of xml document
fwrite($fpout2,"</LEX>\n");
fclose($fpout2);
echo "$n records in $filein1\n";
echo "$n records in $fileout2\n";
exit;
function process_rule($x) {
 $y = $x;
 $y = preg_replace('|></c>|','>___</c>',$y);
 $y = preg_replace('|<c(.*?)>|','<c\1 done="n">',$y);
 $y = "<r>$y</r>";
 if (preg_match('| conf="(.*)" class="(.*?)"|',$y,$matches)) {
  $conf=$matches[1];
  $class = $matches[2];
  $auth="MA";
  if (preg_match('|<c done="n">|',$y)) {
   if ($class == 'GRAMMAR') {
    $cclass='G';
   }else if ($class == 'VARIANT') {
    $cclass='V';
   }else if ($class == 'ERROR') {
    $cclass='E';
   }else if ($class == 'ISSUE') {
    $cclass='_';
   }else {
    $cclass='_';
   }
   if ($conf == "SURE") {$done="y";}else{$done="n";}
   $y = preg_replace('|<c done="n">|',"<c auth=\"MA\" cclass=\"$cclass\" done=\"$done\">",$y);
  }
 }
 return $y;
}
function process_c($x) {
 $rule = "<rule conf=\"_\" class=\"_\"></rule>";
 $y = $x;
 $y = "<r>" . $rule . $y . "</r>";
 $y = preg_replace('|cclass="[?]"|','cclass="_"',$y);
 $y = preg_replace('|<mw err="typo">|','<mw>',$y);
 $y = preg_replace('|></c>|','>___</c>',$y);
 $y = preg_replace('|<c>|','<c auth="SM" cclass="_">',$y);
 $y = preg_replace('|<c(.*?)>|','<c\1 done="n">',$y);
 if(preg_match('| class="_"|',$y)) {
  if (preg_match('| auth="MA" cclass="(.*?)"|',$y,$matches)) {
   $cclass=$matches[1];
   $class="_";
   if($cclass == 'G') {
    $class='GRAMMAR';
   }else if ($cclass == 'V') {
    $class='VARIANT';
   }else if ($cclass == 'E') {
    $class='ERROR';
   }else if ($cclass == 'R') {
    $class="ISSUE";
   }
   $y = preg_replace('| class="_"|'," class=\"$class\"",$y);
  }
 } else if (preg_match('| conf="(.*)" class="(.*?)"|',$y,$matches)) {
  $conf=$matches[1];
  $class = $matches[2];
  $auth="MA";
  if (preg_match('|<c done="n">|',$y)) {
   if ($class == 'GRAMMAR') {
    $cclass='G';
   }else if ($class == 'VARIANT') {
    $cclass='V';
   }else if ($class == 'ERROR') {
    $cclass='E';
   }else if ($class == 'ISSUE') {
    $cclass='_';
   }else {
    $cclass='_';
   }
   $y = preg_replace('|<c done="n">|',"<c auth=\"MA\" cclass=\"$cclass\" done=\"n\">",$y);
  }
 }
 return $y;
}
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
