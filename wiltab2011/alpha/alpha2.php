<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
 alpha.php

*/
$fileout = $argv[1];
$fpout = fopen($fileout,"w") or die("Can't open $fileout\n");

$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}
$keyhash = array();
$keyarr = array();
$table = 'wiltab';
$sql = "select `key`,`lnum` from `$table` ORDER by `lnum`";
$result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
$nfound1=0;
$nkey=0;
$nbad=0;
$nonmw=0;
while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
 $hk  = $line['key'];
 $slp = transcoder_processString($hk,'hk','slp1');
 $lnum = $line['lnum'];
 // $lnum is a decimal number
 $lnum = intval($lnum);
 $lnum1 = sprintf('%05d',$lnum);
 $keyarr[]=array($slp,$lnum1);
 $nkey++;
}
$nerr=0;
for($i=1;$i<$nkey;$i++) {
 list($keyprev,$lnumprev)=$keyarr[$i-1];
 list($key,$lnum) = $keyarr[$i];
 $icmp = slp_cmp($keyprev,$key);
 if ($icmp <= 0) {
  // these are in proper alphabetical order
  fwrite($fpout,"$lnum:$key\n");
  continue;
 }
 $nerr++;
 $mwkey=''; if (!find_mwkey($key)){$mwkey='?';}
 $mwkeyprev=''; if (!find_mwkey($keyprev)){$mwkeyprev='?';}
 $out = "$lnum:$key$mwkey:alpha-err:$keyprev$mwkeyprev";
 $mwkey1='';
 if (($i+1) < $nkey) {
  list($key1,$lnum1) = $keyarr[$i+1];
  if (!find_mwkey($key1)){$mwkey1='?';}
  $out .= ",$key1$mwkey1";
 }
 if (($mwkey . $mwkeyprev . $mwkey1) != '') {
  $nonmw++;
  $out = preg_replace('/-err/','-err1',$out);
 }
 fwrite($fpout,"$out\n");
}
fclose($fpout);
echo "$nkey keys read\n";
echo "$nerr alphabetization errors noted\n";
echo "$nonmw of these involved a non-match to MW\n";
exit();
function slp_cmp($a,$b) {
 $from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh";
 $to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw";
 $a1 = strtr($a,$from,$to);
 $b1 = strtr($b,$from,$to);
 return strcmp($a1,$b1);
}
function find_mwkey($root) {
    $table = 'monier';
    $root = preg_replace("|'|","\\'",$root);
    $sql = "select `key`,`lnum`,`data` from `$table` where `key`='$root'";
    $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
    $nfound1=0;
    $lines = array();
    while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
	$key1 = $line['key'];
	if ($key1 != $root) {continue;}
	$data1 = $line['data'];
	$lnum1 = $line['lnum'];
	$lines[] = array($lnum1,$data1);
    }
    if (count($lines) == 0) {return false;}else{return true;}
}

?>
