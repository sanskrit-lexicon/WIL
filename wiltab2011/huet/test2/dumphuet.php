<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
$filein = $argv[1];
$fileout = $argv[2];
$fp = fopen($filein,"r") or die("Can't open input file $filein\n");
$fpout = fopen($fileout,"w") or die("Can't open output file $fileout\n");
$max=false;
if (!($max)) {
    $max = 100000000;
}

$ch = curl_init();
//return the transfer as a string
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// MA suggestion:
// http://sanskrit.inria.fr/cgi-bin/sktreader?t=SL&st=f&us=f&cp=t&text=akarmakft&topic=&mode=p

$urlpfx = "http://sanskrit.inria.fr/cgi-bin/sktreader?t=SL&st=f&us=f&cp=t&text=";
$urlsfx = "&topic=&mode=p";

$numlines=0;
$nfoundtab1 = 0;
$nfoundtab2 = 0;
$nerr=0;
$nfound=0;
$more=true;
$header = '';
while ($more and (!feof($fp))){
 $x = fgets($fp);
 $x = trim($x);
 if($x==""){continue;}
 // filter on <c></c>
 if(!preg_match('|<c></c>.*<wil>(.*?)</wil>|',$x,$matches)) {
  continue;
 }
 $word = $matches[1];
 if (($numlines % 1000) == 0) {echo "\n$numlines:";}
 $numlines++;

 if (($numlines % 50) == 0) {echo ".";}
 $found=false;
 // incorporate spelling rule changes: (suggested by MA)
 $word1 = preg_replace('/r(.)\1/','r$1',$word);
 $url = $urlpfx . $word1 . $urlsfx;
  curl_setopt($ch, CURLOPT_URL, $url);
  // $output contains the output string
  $output = curl_exec($ch);
  $found=!preg_match('/No solution to chunk/',$output);
  $outputlines = preg_split('/\n/',$output);
//  echo "# lines in output = " . count($outputlines) . "\n";
  if ($numlines == 1) {
   for($i=0;$i<count($outputlines);$i++) {
    $header .= $outputlines[$i] . "\n";
    if(preg_match('/^(.*<body.*?>)/',$output,$matches)) {
     $i = count($outputlines); // break loop
    }
   }
   fwrite($fpout,"$header\n");
  }
  if ($word1 == $word) {
   $wordalt = '';
  }else {
   $wordalt = "(used spelling $word1)";
  }
  if ($found) {
   fwrite($fpout,"<p>$word $wordalt: FOUND</p>\n");
   $nfound++;
  }else {
   fwrite($fpout,"<p>$word $wordalt: NOTFOUND</p>\n");
   $nerr++;
  }
  $output1 = parse_output($output);
  fwrite($fpout,"$output1\n");
  fwrite($fpout,"<br><hr><br>\n");
  if ($max < $numlines) {$more = false;} 
}
  fwrite($fpout,"<br><hr><br>\n");
  fwrite($fpout,"</body></html>\n");

echo "$numlines records processed\n";
echo "$nfound words found\n";
echo "$nerr words not found \n";
fclose($fp);
fclose($fpout);

curl_close($ch);
exit(0);
function parse_output($x) {
 $out="";
 $lines = preg_split('/\n/',$x);
 $nlines = count($lines);
 $start = false;
 for($i=0;$i<$nlines;$i++) {
  $u = $lines[$i];
  if (preg_match('/<body/',$u)) {
   $start=true;
  }else if (preg_match('/<table border="0"/',$u)) {
   $i=$nlines; // force loop end
   continue;
  }else if ($start) {
   if (preg_match('/The Sanskrit Reader Companion/',$u)) {
   }else {
    $u = preg_replace("/<hr.*?>/","",$u);
    $out .= $u . "\n";
   }
  }
 }
 return $out;
}
function old_parse_output($xin){
 $x = $xin;
 $x = preg_replace('/^(.*<body.*?>)/u','',$x);
 $x = preg_replace('/<table border="0".*$/u','',$x);
 if ($x == $xin) {echo "parse_output: no change " . strlen($x) . "\n";}
 return $x;
}
?>
