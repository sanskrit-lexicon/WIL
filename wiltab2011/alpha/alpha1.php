<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
 alpha1.php

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
if (0 == 1) {
// say orderar[$i] is true if (i=0) or (elt[i] <= elt[i+1]);
// otherwise it is false.
$orderar=array();
$orderar[]=true;
for($i=1;$i<$nkey;$i++) {
 list($keyprev,$lnumprev)=$keyarr[$i-1];
 list($key,$lnum) = $keyarr[$i];
 $icmp = slp_cmp($keyprev,$key);
 if ($icmp <= 0) {
  // these are in proper alphabetical order
  $orderar[]=true;
 }else {
  $orderar[]=false;
 }
}
}
$nerr=0;
$nkey1 = $nkey - 1;
for($i=0;$i<$nkey1;$i++) {
 list($key,$lnum) = $keyarr[$i];
 list($key1,$lnum1) = $keyarr[$i+1];
 $icmp = slp_cmp($key,$key1);
 if ($icmp <= 0) {
  // these are in proper alphabetical order
  fwrite($fpout,"$lnum:$key\n");
  continue;
 }
 $nerr++;
 if (1<=$i) {
  list($keyprev,$lnumprev)=$keyarr[$i-1];
 }else {
  $keyprev="";
 }

 $out = "$lnum:$key:alpha-err:$keyprev,$key1";
 fwrite($fpout,"$out\n");
}
fclose($fpout);
echo "$nkey keys read\n";
echo "$nerr alphabetization errors noted\n";
exit();
function slp_cmp($a,$b) {
 $from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh";
 $to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw";
 $a1 = strtr($a,$from,$to);
 $b1 = strtr($b,$from,$to);
 return strcmp($a1,$b1);
}
?>
