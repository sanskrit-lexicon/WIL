<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#wilson_mw.php
# 09-30-2009 ejf
# 02-14-2011
# 02-15-2011  changed to php program. Corrected error in mw_find_basic
#reads file like wilson_keys_dump.txt
#if the slp1 matches a mw key, 
# write the line to wilson_keys_mw.txt
# else write to wilson_keys_nonmw.txt
*/

$filein = $argv[1];
$filecorr = $argv[2];
$fileout = $argv[3];
$fileout1 = $argv[4];
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
$fpout = fopen($fileout,"w") or die("Can't open $fileout\n");
$fpout1 = fopen($fileout1,"w") or die("Can't open $fileout1\n");

$dir = dirname(__FILE__); //directory containing this php file
 $dirdocs = preg_replace('/docs\/.*$/','docs/',$dir);
 $dirphp = $dirdocs . 'php/';
require_once($dirphp . 'utilities.php');

$link = sanskrit_connect_mysql();
if (! $link) {
 die('mysql connection error: ' . mysql_error());
}
$corr_hash = init_corrections($filecorr);
$more= 1;
$dbg=0; #0 for no dbg, 1 for dbg
$nfound=0;
$notfound=0;
$nspellchg=0;
$nauto=0;
$ncorr=0;
$nout1=0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($wilkey,$slp1,$nwilkey)=preg_split('/\t/',$x);
  // if there is a correction, process it
  $corr = $corr_hash[$slp1];
  if ($corr) {
   if(preg_match('/<mw.*?>(.*?)<\/mw>/',$corr,$matches)) {
    $mw = $matches[1];
    if ($mw == '') {
     $nout1++;
     fwrite($fpout1,"$corr\n");
    }else {
     $mw1 = find_mwkey_basic($mw);
     if ($mw1 == $mw) {
      $nfound++;
      fwrite($fpout1,"$corr\n");
     }else {
      die("Correction not found: '$mw' : $corr\n");
     }
    }
    continue;
   }else {
    die( "correction error: $corr\n");
   }
  }
  $slp1a = preg_replace('/[^a-zA-Z]/','',$slp1);
  $mwkey='';
  $rule='';
  if ($slp1a == $slp1) {
     list($mwkey,$rule)=find_mwkey($slp1a);
  }
  if ($mwkey != '') {
   $nfound++;
   fwrite($fpout,"$wilkey\t$slp1\t$mwkey\t$nwilkey\n");
   if ($mwkey != $slp1) {
    $nspellchg++;
//    echo "spellchg: $wilkey $slp1 => $mwkey\n";
    fwrite($fpout1,"<c>$rule</c> <wil>$slp1</wil> <mw>$mwkey</mw>\n");
    $nauto++;
   }
  }else {
   $notfound++;
   if ($slp1a == $slp1) {
    fwrite($fpout1,"<c></c> <wil>$slp1</wil> <mw>$slp1</mw>\n");
   }else {
    fwrite($fpout1,"<c></c> <wilorig>$slp1</wilorig> <wil>$slp1a</wil> <mw>$slp1</mw>\n");
   }
  }
}
fclose($fpin);
fclose($fpout);
fclose($fpout1);
echo "$nfound records written to $fileout\n";
echo "$notfound records written to $fileout1\n";
echo "$nspellchg keys found after spelling change (also in $fileout1)\n";
exit;
function find_mwkey($slp) {
    $ans=find_mwkey_basic($slp);
    if ($ans != ''){
	return array($ans,'');
    }
    $regexps = array(array('r([a-zA-Z])\1','r$1'));
    $slp1=$slp;
    $more=TRUE;
    foreach($regexps as $regexp) {
	list($x,$y) = $regexp;
	$slp1 = preg_replace("/$x/","$y",$slp);
	if ($slp1 == $slp) {continue;}
	$ans = find_mwkey_basic($slp1);
	if ($ans != '') return array($slp1,"AUTO($x => $y)");
    }
    return array('',''); // failure
}
function find_mwkey_basic($slp) {
    $table = 'monier';
    $sql = "select `key`,`data` from `$table` where `key`='$slp'";
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
function init_corrections($file){
 $h = array(); // hash, returned
$fp = fopen($file,"r") or die("Can't open $file\n");
 while (!feof($fp)) {
  $x = fgets($fp);
  $x = trim($x);
  if ($x == ''){continue;}
  if (!preg_match('/<wil.*?>(.*?)<\/wil>/',$x,$matches)) {
   echo "Error in $file: $x\n";
   continue;
  }
  $key=$matches[1];
  $h[$key]=$x;
 }
 fclose($fp);
 return $h;
}
?>
