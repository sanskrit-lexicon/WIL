Counterpart of PWG/pwgissues/issue174/08_markup_fix.py
(see https://github.com/sanskrit-lexicon/PWG/issues/175
 and https://github.com/sanskrit-lexicon/PWK/issues/113).

Files in this folder:
  08_markup_fix.py        -- fixer + audit script for wil.txt
  test_markup_fix.py      -- synthetic tests (20/20 pass)
  wil_fixed.txt           -- repaired copy of wil.txt (1 whitespace trim)
  markup_fix_changes.txt  -- updateByLine log of every auto-fix
  markup_audit.txt        -- audit findings requiring human review
  ISSUE_COMMENT.md        -- GitHub issue body (also saved as comment_markup_fix.md)
  comment_markup_fix.md   -- same as ISSUE_COMMENT.md (older naming convention)
  readme.txt              -- this file

Usage:
  python 08_markup_fix.py            # uses csl-orig/v02/wil/wil.txt by default
  python 08_markup_fix.py IN OUT     # custom paths
  python test_markup_fix.py          # run synthetic tests
