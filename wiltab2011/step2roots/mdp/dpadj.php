<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#step2roots/mdp/dpadj.php
# 02-26-2011
#reads file like update input (log_...txt) for wiltab
# performs some adjustments on the 'dp' element.

*/
//
$filein = $argv[1];  // the input log file
$fileout = $argv[2]; // the adjusted output log file
$filespell = $argv[3];
$filemwmdp= $argv[4]; // specialized input associating mw with mdp
$filemdp = $argv[5];  // specialized input with mdp data.
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
$mdp_hash = init_mdp($filemdp);
$mwmdp_hash = init_mwmdp($filemwmdp);
$nkey=0;
$nadj=0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  if (!preg_match('/^<H1>.*?<key1>(.*?)<\/key1>.*<dp(.*?)>(.*?)<\/dp>/',$x,$matches)) {
   fwrite($fpout,"$x\n");
   continue;
  }
  $nkey++;
  $hk = $matches[1];
  $hkattr = $matches[2];
  $slp = transcoder_processString($hk,'hk','slp1');
  $slpattr = transcoder_processString($hkattr,'hk','slp1');
  $slpattr1 = adjust($slpattr,$slp,$mdp_hash,$mwmdp_hash,$spell_hash);
  $hkattr1 = transcoder_processString($slpattr1,'slp1','hk');
  if ($hkattr1 != $hkattr) {
   $nadj++;
   $y = preg_replace('/<dp(.*?)><\/dp>/',"<dp$1 mdp=\"$hkattr1\"></dp>",$x);
   fwrite($fpout,"$y\n");
   echo "$slp: '$slpattr' => '$slpattr1'\n";
  }
}
fclose($fpin);
fclose($fpout);
echo "$nadj dp adjustments for $nkey keys\n";
exit;
function adjust($attr,$keyin,$mdp_hash,$mwmdp_hash,$spell_hash) {
 $key = $spell_hash[$keyin];
 if (!$key) {$key = $keyin;}
 $sidarr = $mwmdp_hash[$key];
 if (!$sidarr) {
  $ans = "mdp=\"NA\"";
  return $ans;
 }
 $ansarr=array();
 foreach($sidarr as $sid) {
  $mdp_data = $mdp_hash[$sid];
  $premarker='';
  if (preg_match('/<premarker>(.*)<\/premarker>/',$mdp_data,$matches)) {
   $premarker=$matches[1];
  }
  $marker='';
  if(preg_match('/<marker>(.*)<\/marker>/',$mdp_data,$matches)) {
   $marker=$matches[1];
  }
  $norm='';
  if(preg_match('/<root(.*?)>(.*)<\/root>/',$mdp_data,$matches)) {
   $a = $matches[1];
   $r = $matches[2];
   if (preg_match('/normal="(.*?)"/',$a,$matches)) {
    $r = $matches[1];
   }
   $norm = $r;
  }
  $arr=array();
  $arr[]=$premarker;
  $arr[]=$norm;
  $arr[]=$marker;
  $ans1 = join('-',$arr);
  $ansarr[]="$sid,$ans1";
 }
 $ans = join(';',$ansarr);
 return $ans;
}
function init_mdp($file){
 $h = array(); // hash, returned
$fp = fopen($file,"r") or die("Can't open $file\n");
 while (!feof($fp)) {
  $x = fgets($fp);
  $x = trim($x);
  if ($x == '') {continue;}
  if(!preg_match('/<entry[^>]* sid="(.*?)"/',$x,$matches)) {continue;}
  $sid = $matches[1];
  $h[$sid]=$x;
 }
 fclose($fp);
 return $h;
}
function init_mwmdp($file){
 $h = array(); // hash, returned
 $fp = fopen($file,"r") or die("Can't open $file\n");
 while (!feof($fp)) {
  $x = fgets($fp);
  $x = trim($x);
  if ($x == '') {continue;}
  $vals = preg_split('/\t/',$x);
  $norm = $vals[0];
  if ($norm == 'NOMDP') {continue;}
  $sid = $vals[1];
  $mwkey = $vals[2];
  if ($mwkey == 'NOMW') {continue;}
  $old = $h[$mwkey];
  if (!$old) {$old = array();}
  $old[] = $sid;
  $h[$mwkey]=$old;
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
