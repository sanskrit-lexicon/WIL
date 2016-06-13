<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
 step2/wiltab_dump_key2.php
  creates wiltab_dump_keys.txt from wiltab file
*/
$filein = $argv[1];  # wiltabxml text file
$fileout = $argv[2];
 $fpin = fopen($filein,"r") or die("Can't open $filein\n");
$fpout = fopen($fileout,"w") or die("Can't open $fileout\n");
require_once('utilities/transcoder.php');
transcoder_set_dir("utilities/transcoder");
$keyhash = array();
$keyarr = array();

$nfound1=0;
$nkey=0;
$nbad=0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($hk,$L,$data)=preg_split('/\t/',$x);
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
