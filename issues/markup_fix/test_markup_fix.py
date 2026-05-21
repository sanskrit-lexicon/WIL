"""Synthetic tests for 08_markup_fix.py (WIL)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path

# Import from sibling
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
mod = import_module("08_markup_fix")
fix_nested_ab = mod.fix_nested_ab
fix_trim_whitespace = mod.fix_trim_whitespace

PASS = 0
FAIL = 0


def check(desc, got, want):
    global PASS, FAIL
    if got == want:
        print(f"  PASS  {desc}")
        PASS += 1
    else:
        print(f"  FAIL  {desc}")
        print(f"        got:  {got!r}")
        print(f"        want: {want!r}")
        FAIL += 1


print("=== nested <ab> fixes ===")

# (a) prefix: inner wraps a prefix → flatten into outer
line, n = fix_nested_ab("<ab>  <ab>fem.</ab> or masc.</ab>")
check("prefix-inner flattened", line, "<ab>  fem. or masc.</ab>")
check("prefix-inner count", n, 1)

# (b) suffix: inner wraps a suffix → flatten
line, n = fix_nested_ab("<ab>nom. sing. <ab>us.</ab></ab>")
check("suffix-inner flattened", line, "<ab>nom. sing. us.</ab>")
check("suffix-inner count", n, 1)

# (c) exact dup: inner == outer's entire content
line, n = fix_nested_ab("<ab><ab>fem.</ab></ab>")
check("exact-dup flattened", line, "<ab>fem.</ab>")
check("exact-dup count", n, 1)

# (d) middle: inner in the middle is also flattened (pre+inner+post concatenated)
line, n = fix_nested_ab("<ab>nom. <ab>sing.</ab> us.</ab>")
check("middle flattened (line)", line, "<ab>nom. sing. us.</ab>")
check("middle flattened (count)", n, 1)

# (e) no nesting → no-op
line, n = fix_nested_ab("<ab>fem.</ab>")
check("no-op nested", line, "<ab>fem.</ab>")
check("no-op count", n, 0)

print("\n=== whitespace trims ===")

# <ab> trailing space
line, n = fix_trim_whitespace("<ab>fem. </ab>")
check("<ab> trailing trim", line, "<ab>fem.</ab>")
check("<ab> trailing trim count", n, 1)

# <lex> leading space
line, n = fix_trim_whitespace("<lex> m.</lex>")
check("<lex> leading trim", line, "<lex>m.</lex>")
check("<lex> leading trim count", n, 1)

# <bot> trailing space
line, n = fix_trim_whitespace("<bot>Ficus indica </bot>")
check("<bot> trailing trim", line, "<bot>Ficus indica</bot>")
check("<bot> trailing trim count", n, 1)

# already clean → no-op
line, n = fix_trim_whitespace("<ab>fem.</ab>")
check("already-clean no-op", line, "<ab>fem.</ab>")
check("already-clean count", n, 0)

# <zoo> clean
line, n = fix_trim_whitespace("<zoo>Clupea cultrata</zoo>")
check("<zoo> clean no-op", line, "<zoo>Clupea cultrata</zoo>")
check("<zoo> clean count", n, 0)

print(f"\n{'='*40}")
print(f"Results: {PASS}/{PASS+FAIL} passed", ("✓" if FAIL == 0 else "✗"))
if FAIL:
    sys.exit(1)
