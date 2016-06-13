<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
#step2roots/otherkeys/roots.php
# 02-22-2011
# 06-13-2016
#reads a version of wiltabxml.txt (assumes this is in HK form for Sanskrit)
# determine records that can be identifed as roots in wiltab.
# writes the data records for these roots, in HK<tab>SLP1 form

*/
$fileinkeys = $argv[1];
$fileindata = $argv[2];
$fileout = $argv[3];
$fpin = fopen($fileinkeys,"r") or die("Can't open $fileinkeys\n");
$fpout = fopen($fileout,"w") or die("Can't open $fileout\n");

$dbg=0; #0 for no dbg, 1 for dbg
$nfound=0;
$notfound=0;
$nkey=0;
$nprob=0;

$wiltab = init_wiltab($fileindata);
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($hk,$slp)=preg_split('/\t/',$x);
  $root = $hk;
  $nkey++;
  $linesin = $wiltab[$hk];

    $lines = array();
    for($inline=0;$inline<count($linesin);$inline++) {
     $linein = $linesin[$inline];
     list($lnum,$data1) = $linein;
     if (!preg_match('/<body.*? r[.]/',$data1)) {continue;}
     $lines[] = $linein;
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
function init_wiltab($filein) {
 $wiltab = array();
 $fpin = fopen($filein,"r") or die("Can't open $filein\n");
 $n = 0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  list($hk,$L,$data)=preg_split('/\t/',$x);
  $prev = $wiltab[$hk];
  if (!$prev) {
   $prev = array();
   $n++;
  }
  $cur = array($L,$data);
  $prev[] = $cur;
  $wiltab[$hk]=$prev;
 }
 fclose($fpin);
 print "init_wiltab: $n lines read from $filein\n";
 return $wiltab;
}
?>
