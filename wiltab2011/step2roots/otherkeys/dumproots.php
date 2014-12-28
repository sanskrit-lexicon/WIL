<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#step2roots/otherkeys/roots.php
# 02-22-2011
#reads file like wiltab_dump.txt (hk\tslp)
# determine records that can be identifed as roots in wiltab.
*/

$filein = $argv[1];
$fileout = $argv[2];
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
$fpout = fopen($fileout,"w") or die("Can't open $fileout\n");

$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}

$dbg=0; #0 for no dbg, 1 for dbg
$nfound=0;
$notfound=0;
$nkey=0;
$nprob=0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($hk,$slp)=preg_split('/\t/',$x);
  $root = $hk;
  $nkey++;
    $table = 'wiltab';
    $sql = "select `key`,`lnum`,`data` from `$table` where `key`='$root'";
    $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
    $nfound1=0;
    $lines = array();
    $nline=0;
    while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
	$key1 = $line['key'];
	if ($key1 != $root) {continue;}
	$nline++;
	$data1 = $line['data'];
	if (!preg_match('/<body.*? r[.]/',$data1)) {continue;}
	$lnum1 = $line['lnum'];
	$lines[] = array($lnum1,$data1);
    }
    if ($nline == 0) { // should not happen
     echo "$x no record found\n";
     $nprob++;
    }
    if (count($lines) == 0) {
     continue; // not identified as root
    }
    $nfound++;
    fwrite($fpout,"$x\n"); // same format as input
    continue;
}
fclose($fpin);
fclose($fpout);
echo "$nkey keys processed\n";
echo "$nfound keys identified as roots\n";
exit;
?>
