<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
$m = "([aAiIuUfFeEoO])([kKgGNwWqQRtTdDnpPbBmyrlvSzsh])";
$r = "$1r$2";
$x = "vitaka";
$y = replace_each($m,$r,$x);
echo "$x => (" . join(' ',$y) . ")\n";
exit();
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
if (0 == 1) { // dbg
  echo "$pfx,$u => $v,$sfx\n";
  for($j=0;$j<count($matches);$j++) {
   $u = $matches[$j];
   echo "$i,$j: " . join(',',$u) . "\n";
  }
}
 }
 return $ans;
}
function version1_replace_each($m,$r,$x) {
// returns an array of strings based on input string $x.
// $m is a regexp, $r is replacement
// For each place in $x which matches $m, 
// apply the replacement $r just at this place.
// Assume that $m does NOT contain // delimiters.
 $pieces = preg_split("/$m/",$x,null,PREG_SPLIT_DELIM_CAPTURE);
 foreach($pieces as $piece) {
  echo "$piece\n";
 }
 return array($x);
}
?>
