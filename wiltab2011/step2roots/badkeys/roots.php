<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#wiltab_mw.php
# 02-21-2011
#reads file like wiltab_dump.txt (hk\tslp)
#if the slp1 matches a mw key, 
# write the line to wiltab_keys_mw.txt
# else write to wiltab_keys_nonmw.txt
*/

$filein = $argv[1];
$fileout = $argv[2];
$filespell= $argv[3]; // spelling changes
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
$spell_hash = init_spelling($filespell);

$dbg=0; #0 for no dbg, 1 for dbg
$nfound=0;
$notfound=0;
$nkey=0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  $y = preg_replace('/ : /',':',$x);
  list($slp,$hk)=preg_split('/:/',$y);
  if (!preg_match('/^(.*?)\(/',$slp,$matches)) {
   echo "line skipped: $x\n";
   continue;
  }
  $root0 = $matches[1];
  if (preg_match('/^(.*)a$/',$root0,$matches)) {
   $root1 = $matches[1];
  }else {
   $root1 = $root0;
  }
  $temp = $spell_hash[$root1];
  if ($temp) {$root=$temp;}else{$root=$root1;}
  $nkey++;
    $table = 'monier';
    $sql = "select `key`,`lnum`,`data` from `$table` where `key`='$root'";
    $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
    $nfound1=0;
    $lines = array();
    while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
	$key1 = $line['key'];
	if ($key1 != $root) {continue;}
	$data1 = $line['data'];
	if (!preg_match('/<vlex type="root">/',$data1)) {continue;}
	$lnum1 = $line['lnum'];
	$lines[] = array($lnum1,$data1);
    }
    if (count($lines) == 0) {
//     echo "NO MW ROOT: $root  ($y)\n";
     if ($root1 != $root) {
      echo "$root1 (spelled as $root): Wilson slp key=$slp\n";
     }else {
      echo "$root1: Wilson slp key=$slp\n";
     }
     $notfound++;
     continue;
    }
//    echo "FOUND: $root ($y)\n";
    $nfound++;
    fwrite($fpout,"<c>SP-ROOT</c> <wil>$slp</wil> <mw>$root</mw>\n");
    continue;
if (0 == 1) {
  list($mwkey,$rule)=find_mwkey($slp1a);
  if ($mwkey != '') {
   if ($mwkey == $slp1) {
   $nfound++;
//   fwrite($fpout,"$wilkey\t$slp1\t$mwkey\t$nwilkey\n");
   }else {
    $nspellchg++;
    fwrite($fpout1,"<c>$rule</c> <wil>$slp1</wil> <mw>$mwkey</mw>\n");
    $rulecount_hash[$rule]++;
    $nauto++;
   }
  }else {
   $notfound++;
   fwrite($fpout1,"<c></c> <wil>$slp1</wil> <mw>$slp1</mw>\n");   
  }
}
}
fclose($fpin);
fclose($fpout);
echo "$nkey keys processed\n";
echo "$nfound keys identified as roots\n";
echo "$notfound keys not identified as roots \n";
exit;
function init_spelling($file){
 $h = array(); // hash, returned
$fp = fopen($file,"r") or die("Can't open $file\n");
 while (!feof($fp)) {
  $x = fgets($fp);
  $x = trim($x);
  list($old,$new) = preg_split('/:/',$x);
  $h[$old]=$new;
 }
 fclose($fp);
 return $h;
}
?>
