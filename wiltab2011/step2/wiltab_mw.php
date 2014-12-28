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
$filecorr = $argv[2];
$fileout1 = $argv[3];
$fileregexp = $argv[4];
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
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
init_regexparr($fileregexp);
$rulecount_hash = array();
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
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($wilkey,$slp1,$nwilkey)=preg_split('/\t/',$x);
  $slp1a = preg_replace('/[^a-zA-Z]/','',$slp1);
  if ($slp1a != $slp1) {
     echo "ill-formed key: $slp1\n";
     $nbadkey++;
     continue;
  }
  $nkey++;
  // if there is a correction, process it
  $corr = $corr_hash[$slp1];
  if ($corr) {
   if(preg_match('/<mw.*?>(.*?)<\/mw>/',$corr,$matches)) {
    $mw = $matches[1];
    if ($mw == '') {
     $nout1++;
     if (!preg_match('/^C/',$corr)) {
      $corr = "C" . $corr;
     }
     fwrite($fpout1,"$corr\n");
    }else {
     $mw1 = find_mwkey_basic($mw);
     if ($mw1 == $mw) {
      $nfound++;
      if (!preg_match('/^C/',$corr)) {
       $corr = "C" . $corr;
      }
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
fclose($fpin);
//fclose($fpout);
fclose($fpout1);
echo "$nkey keys processed\n";
echo "$nbadkey keys were ill-formed\n";
echo "$nfound keys found with no spelling change\n";
echo "$nspellchg keys found after spelling change\n";
echo "$notfound records not found yet \n";
$nc=0;
foreach($rulecount_hash as $rule=>$count) {
 echo "spelling rule $rule solved $count problems\n";
 $nc += $count;
}
echo "(nc = $nc)\n";
exit;
function find_mwkey($slp) {
global $regexparr;
    $ans=find_mwkey_basic($slp);
    if ($ans != ''){
	return array($ans,'');
    }
    $slp1=$slp;
    $more=TRUE;
    foreach($regexparr as $regexp) {
	list($rname,$rtype,$x,$y) = $regexp;
	if ($rtype == 'SIMPLE') {
	 $slp1 = preg_replace("/$x/","$y",$slp);
	 if ($slp1 == $slp) {continue;}
	 $ans = find_mwkey_basic($slp1);
	 if ($ans != '') return array($slp1,"AUTO($rname)");
	} else if ($rtype == 'LOOP') {
	 $variants = replace_each($x,$y,$slp);
	 foreach ($variants as $slp1) {
	  $ans = find_mwkey_basic($slp1);
	  if ($ans != '') return array($slp1,"AUTO($rname)");
	 }
	}else {
	 die ("regexp internal error\n");
	}

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
function init_regexparr($filein){
global $regexparr;
$regexparr = array();
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
$typearr = array();
$typearr["SIMPLE"]=true;
$typearr["LOOP"]=true;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($rname,$rtype,$x,$y) = preg_split('/\t/',$x);
  $regexparr[] = array($rname,$rtype,$x,$y);
  if (!$typearr[$rtype]) {
   die("Unknown regexp type ($rtype): $x\n");
  }
 }
fclose($fpin);
}
function replace_each($m,$r,$x) {
// returns an array of strings based on input string $x.
// $m is a regexp, $r is replacement
// For each place in $x which matches $m, 
// apply the replacement $r just at this place.
// Assume that $m does NOT contain // delimiters.
 $ans = array();
 preg_match_all("/$m/",$x,$multimatch,PREG_PATTERN_ORDER +PREG_OFFSET_CAPTURE);
 $matches0 = $multimatch[0];
 for($i=0;$i<count($matches0);$i++) {
  $matches = $multimatch[0][$i];
  $matchbeg = $matches[1]; // where this match starts
  $pfx = substr($x,0,$matchbeg); // preceding this 
  $u = $matches[0];  // this matching string
  $matchend = $matchbeg + strlen($u);
  $sfx = substr($x,$matchend);  // part after match
  $v = preg_replace("/$m/",$r,$u); //alteration of matched string
  $y = $pfx . $v . $sfx;
  $ans[] = $y;
 }
 return $ans;
}
?>
