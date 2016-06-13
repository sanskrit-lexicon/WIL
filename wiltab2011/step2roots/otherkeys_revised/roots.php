<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#step2roots/otherkeys/roots.php
# 02-22-2011
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
$nfoundspa=0; //found, with standard spelling change (drop 'a')
$nfoundspb=0; // found, with non-standard spelling change
$nfoundnosp=0; // found, no spelling change
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($hk,$slp)=preg_split('/\t/',$x);
  $root0 = $slp;
  if (preg_match('/^(.*)a$/',$root0,$matches)) {
   $root1 = $matches[1];
  }else {
   $root1 = $root0;
  }
  $root = $root1;
  $rootinit = $root;
  $nkey++;
  $mwflag = find_mwroot($root);
  if($mwflag) {
   $nfound++;
   if ($root != $slp) {
    $nfoundspa++;
    fwrite($fpout,"<c>SPa-ROOT</c> <wil>$slp</wil> <mw>$root</mw>\n");
   }else {
    fwrite($fpout,"<c>ROOT</c> <wil>$slp</wil> <mw>$root</mw>\n");
    $nfoundnosp++;
   }
   continue;
  }
  $roota = alt_spell($root,$spell_hash);
  if ($roota  != $root) {
   // try new spelling
   $mwflag = find_mwroot($roota);
  }
  if($mwflag) {
   $root=$roota;
   $nfound++;
   if ($root != $slp) {
    fwrite($fpout,"<c>SPb-ROOT</c> <wil>$slp</wil> <mw>$root</mw>\n");
    $nfoundspb++;
   }else {
    fwrite($fpout,"<c>ROOT</c> <wil>$slp</wil> <mw>$root</mw>\n");
    echo "UNEXPECTED occurrence: $root == $slp \n";
    $nfoundnosp++;
   }
   continue;
  }
  // not found echo to log file
  if ($root1 != $root) {
   echo "$root1 (spelled as $root): Wilson slp key=$slp\n";
  }else {
   $out = "<c>?</c> <wil err=\"fact\" corr=\"$rootinit\">$slp</wil> <mw>$rootinit</mw>\n";
//   echo "$root1: Wilson slp key=$slp\n";
   echo "$out";
  }
  $notfound++;
}
fclose($fpin);
fclose($fpout);
echo "$nkey keys processed\n";
echo "$notfound keys not identified as mw roots \n";
echo "$nfound keys identified as roots\n";
echo "of these, $nfoundspa were found with dropping final 'a'\n";
echo "of these, $nfoundspb were found other spelling change 'a'\n";
echo "of these, $nfoundnosp were found with no spelling change\n";

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
function find_mwroot($root) {
    $table = 'monier';
    $sql = "select `key`,`lnum`,`data` from `$table` where `key`='$root'";
    $result=mysql_query($sql) or die('mysql query failed $table: ' . mysql_error());
    $nfound1=0;
    $lines = array();
    while ($line = mysql_fetch_array($result,MYSQL_ASSOC)) {
	$key1 = $line['key'];
	if ($key1 != $root) {continue;}
	$data1 = $line['data'];
	if (preg_match('/<vlex type="root">/',$data1)) {
	}else if (preg_match('/<vlex>Nom[.]<\/vlex>/',$data1)) {
	}else { // not identified as root
	 continue;
	}
	$lnum1 = $line['lnum'];
	$lines[] = array($lnum1,$data1);
    }
    if (count($lines) == 0) {return false;}else{return true;}
}
function alt_spell($root,$spell_hash) {
 // get from table, if possible
 $x = $spell_hash[$root]; 
 if ($x) {return $x;}
 if (preg_match('/r(.)\1/',$root)) {
  $ans = preg_replace('/r(.)\1/',"r$1",$root);
  return $ans;
 }
 if (preg_match('/cC$/',$root)) {
  $ans = preg_replace('/cC/',"C",$root);
  return $ans;
 }
 
 // try homorganic nasal
 if (preg_match('/([kKgG])$/',$root)) {
  $ans = preg_replace('/([kKgG])$/',"N$1",$root);
 }else if (preg_match('/([cCjJ])$/',$root)) {
  $ans = preg_replace('/([cCjJ])$/',"Y$1",$root);
 }else if (preg_match('/([wWqQ])$/',$root)) {
  $ans = preg_replace('/([wWqQ])$/',"R$1",$root);
 }else if (preg_match('/([tTdD])$/',$root)) {
  $ans = preg_replace('/([tTdD])$/',"n$1",$root);
 }else if (preg_match('/([pPbB])$/',$root)) {
  $ans = preg_replace('/([pPbB])$/',"m$1",$root);
 }else {
  $ans=$root;
 }
 return $ans;
}
?>
