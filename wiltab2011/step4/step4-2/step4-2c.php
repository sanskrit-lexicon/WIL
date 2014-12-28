<?php
error_reporting(E_ALL ^ E_NOTICE); // all errors except 'PHP Notice:'
/**
# step4-2c.php
# 12-04-2011
# Partition wiltab_mw-4-2-todo.xml into 5 files, based on value of "class"
*/

$filein = $argv[1];
$classvals = array("ERROR","VARIANT","GRAMMAR","ISSUE","_");  // agrees with dtd
$classhash = array();
$fpin = fopen($filein,"r") or die("Can't open $filein\n");
foreach($classvals as $class) {
 $classlow = strtolower($class);
 if($classlow == "_") {$classlow = "todo";}
 $filename = "wiltab_mw-4-2-todo-$classlow.xml";
 $fpout = fopen($filename,"w") or die("Can't open $filename\n");
 $count=0;
 $classhash[$class]=array($filename,$fpout,$count);
}
// Initial xml lines
$header = array('<?xml version="1.0" encoding="UTF-8"?>',
  '<!DOCTYPE LEX SYSTEM "lex.dtd" []>',
  '<LEX>');
foreach($classhash as $class=>$val) {
 list($filename,$fpout,$count)=$val;
 foreach($header as $x) {
  fwrite($fpout,"$x\n");
 }
}
$n=0;
 while (!feof($fpin)) {
  $x = fgets($fpin);
  $x = trim($x);
  if ($x == ''){continue;}
  if (preg_match('|^<r><rule[^>]* class="(.*?)"|',$x,$matches)) {
   $y = $x;
  }else {
   echo "skipping: $x\n";
   continue;
  }
  $n++;
  $class=$matches[1];
  $val = $classhash[$class];
  if (!$val) {
   echo "UNKNOWN class: $x\n";
   exit(0);
  }
  list($filename,$fpout,$count)=$val;
  fwrite($fpout,"$y\n");
  $count++;
  $val = array($filename,$fpout,$count);
  $classhash[$class]=$val;
 }
fclose($fpin);
echo "$n records in $filein\n";
// close root of xml documents
$ntot=0;
foreach($classhash as $class=>$val) {
 list($filename,$fpout,$count)=$val;
 fwrite($fpout,"</LEX>\n");
 fclose($fpout);
 echo "$count records in file $filename\n";
 $ntot+=$count;
}
echo "$ntot total output records\n";
exit;
?>
