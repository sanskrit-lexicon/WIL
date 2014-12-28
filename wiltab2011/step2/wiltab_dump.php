<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
 step2/wiltab_dump.php
  creates wiltab_keys_dump.txt from wiltab mysql file
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
$sql = "select `key` from `$table` ORDER by `lnum`";
$result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
$nfound1=0;
$nkey=0;
$nbad=0;
while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
 $hk  = $line['key'];
 $slp = transcoder_processString($hk,'hk','slp1');
 if (!preg_match('/^[a-zA-Z]+$/',$hk)) {
  echo "$slp : $hk\n";
  $nbad++;
  continue;
 }
 if ($keyhash[$slp]) {continue;}
 $keyhash[$slp] = $hk;
 $nkey++;
}
uksort($keyhash,'slp_cmp'); // sort by value = slp transliteration
foreach($keyhash as $slp=>$hk) {
 fwrite($fpout,"$hk\t$slp\n");
}
fclose($fpout);
echo "$nkey keys read\n";
echo "$nbad bad keys\n";
exit();
function slp_cmp($a,$b) {
 $from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh";
 $to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw";
 $a1 = strtr($a,$from,$to);
 $b1 = strtr($b,$from,$to);
 return strcmp($a1,$b1);
}
?>
