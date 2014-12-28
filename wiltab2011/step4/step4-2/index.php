<?php
 $files=array(
  "wiltab_mw-4-2-likely.html",
  "wiltab_mw-4-2-root.html",
  "wiltab_mw-4-2-sure.html",
  "wiltab_mw-4-2-todo-error.html",
  "wiltab_mw-4-2-todo-grammar.html",
  "wiltab_mw-4-2-todo.html",
  "wiltab_mw-4-2-todo-issue.html",
  "wiltab_mw-4-2-todo-todo.html",
  "wiltab_mw-4-2-todo-variant.html");
 $dir = "http://www.sanskrit-lexicon.uni-koeln.de/scans/WILScan/mysql/wiltab/keys/step4/step4-2";
 foreach($files as $file) {
  $href="$dir/$file";
  echo "<a href='$href'>$file</a><br/>";
 }
?>
