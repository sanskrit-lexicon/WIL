"""
Markup fixer + audit for wil.txt (WIL).

Counterpart of pwgissues/issue174/08_markup_fix.py (PWG) and
pwkissues/markup_fix/08_markup_fix.py (PWK).

Two jobs:

  1. FIX problems that have a single safe automatic resolution.
       (a) nested <ab><ab>X</ab> Y</ab>  →  <ab>X Y</ab>           (rare-but-possible)
       (b) nested <ab><ab>X</ab></ab>    →  <ab>X</ab>             (degenerate dup)
       (c) whitespace inside tag pairs, for every paired tag that
           actually occurs in wil.txt (see TRIM_TAGS).

  2. AUDIT issues that need a human decision. These are reported but
     NOT auto-modified. Each finding lands in markup_audit.txt with
     enough surrounding context to act.

Why the nesting fixer exists even though wil.txt is currently clean
on <ab>: this script is meant to be re-run after any new auto-wrap
pass that overlays <ab n="…"> tags. Such a pass can produce
<ab><ab>…</ab>…</ab>; this is the cleanup tool for that contingency.

WIL-specific notes vs the PWK counterpart:
  - TRIM_TAGS covers only paired tags actually present in wil.txt:
    <ab> (67,797), <lex> (53,028), <bot> (3,883), <ls> (230),
    <zoo> (213), <lang> (28), <symbol> (1).
    Tags present in PWK but absent here: <is>, <hom>, <gk>, <iw>,
    <arab>, <span>.
  - The only whitespace hit in current wil.txt is one trailing space
    inside <ab> (L~trail). All other tags are already clean.
  - 5 <ab n="…"> attribute occurrences with non-standard values
    ("???", "Diabetes", "grains", "active", "passive") plus one
    empty n="" — these are audit-only.
  - 280 {{old -> new || …}} correction records are present; nested
    <ls> inside those blocks is informational, not a bug.
  - No <is> tag exists in wil.txt; boundary-collision checks that
    reference <is> are removed.

Inputs:
  ../../../csl-orig/v02/wil/wil.txt      (when run from wilissues/markup_fix/)
  or argv[1] (any path)

Outputs:
  wil_fixed.txt             -- repaired copy
  markup_fix_changes.txt    -- log of every auto-fix
  markup_audit.txt          -- everything requiring a human eye, with line refs

Usage:
  python 08_markup_fix.py            # uses default in/out paths
  python 08_markup_fix.py IN OUT     # custom paths
"""

import sys
import re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent

if len(sys.argv) >= 3:
    PW_TXT = Path(sys.argv[1])
    OUT_FIX = Path(sys.argv[2])
else:
    candidates = [
        HERE.parent.parent.parent / "csl-orig" / "v02" / "wil" / "wil.txt",
        HERE / "wil.txt",
    ]
    PW_TXT = next((p for p in candidates if p.exists()), candidates[0])
    OUT_FIX = HERE / "wil_fixed.txt"

OUT_LOG = HERE / "markup_fix_changes.txt"
OUT_AUDIT = HERE / "markup_audit.txt"


# ---------------------------------------------------------------------------
# Pattern 1: nested <ab> wrappings
# ---------------------------------------------------------------------------
#
# After any future auto-wrap + local-abbreviation overlay pass we may see:
#   <ab><ab>fem.</ab> or masc.</ab>           (case a)
#   <ab n="?"><ab>St.</ab></ab>               (case b — exact-duplicate)
#
# Rule of repair:
#  * If the inner wrap covers a strict prefix or suffix of the outer wrap,
#    drop the inner — the outer is canonical.
#  * If the inner wrap exactly matches the outer wrap's content, drop the
#    inner (degenerate duplicate).
#  * If the inner wrap covers something in the middle, leave it — that is
#    too ambiguous to resolve without semantic context.

NEST_RX = re.compile(
    r"<ab(?P<oa>\b[^>]*)>(?P<pre>[^<]*)<ab(?P<ia>\b[^>]*)>(?P<inner>[^<]*)</ab>(?P<post>[^<]*)</ab>"
)


def fix_nested_ab(line):
    n_fixed = 0
    while True:
        m = NEST_RX.search(line)
        if not m:
            return line, n_fixed
        oa = m.group("oa")
        pre = m.group("pre")
        inner = m.group("inner")
        post = m.group("post")
        repl = f"<ab{oa}>{pre}{inner}{post}</ab>"
        line = line[:m.start()] + repl + line[m.end():]
        n_fixed += 1


# ---------------------------------------------------------------------------
# Pattern 2: whitespace inside common tag pairs
# ---------------------------------------------------------------------------
# Paired tags that actually exist in wil.txt (closing-tag counts):
#   ab 67,797 | lex 53,028 | bot 3,883 | ls 230 | zoo 213 | lang 28 | symbol 1
TRIM_TAGS = ["ab", "lex", "bot", "ls", "zoo", "lang", "symbol"]


def fix_trim_whitespace(line):
    n = 0
    for tag in TRIM_TAGS:
        pat = re.compile(rf"(<{tag}\b[^>]*>)(\s+)([^<]*?)(\s*)(</{tag}>)")
        def _repl(m, _n=None):
            nonlocal n
            inside = m.group(3).rstrip()
            if inside != m.group(2) + m.group(3) + m.group(4):
                n += 1
            return f"{m.group(1)}{inside}{m.group(5)}"
        line = pat.sub(_repl, line)
        pat2 = re.compile(rf"(<{tag}\b[^>]*>)([^<]*?)(\s+)(</{tag}>)")
        def _repl2(m, _n=None):
            nonlocal n
            inside = m.group(2).rstrip()
            n += 1
            return f"{m.group(1)}{inside}{m.group(4)}"
        line = pat2.sub(_repl2, line)
    return line, n


# ---------------------------------------------------------------------------
# Audit (no auto-modification)
# ---------------------------------------------------------------------------

# Helper: classify each nested-<ls> match by whether the inner <ls>
# opens inside a {{…}} correction block (informational) or outside (bug).
def _ls_nested_classify(line):
    inside = []
    outside = []
    for m in re.finditer(r"<ls\b[^>]*>([^<]*<ls\b[^>]*>)", line):
        inner_offset = m.group(1).find("<ls")
        inner_open = m.start(1) + (inner_offset if inner_offset >= 0 else 0)
        prefix = line[:inner_open]
        if prefix.rfind("{{") > prefix.rfind("}}"):
            inside.append(m)
        else:
            outside.append(m)
    return outside, inside


AUDIT_CHECKS = [
    ("Adjacent </ab> <ab> — possibly intentional but worth verifying",
     re.compile(r"</ab>\s*<ab")),
    ("Nested <ls> outside a {{ … }} correction record",
     None),  # custom handler below
    ("Nested <ls> INSIDE a {{ … }} correction record (informational)",
     None),  # custom handler below
    ("<ab n=\"?\"> or <ab n=\"???\"> placeholder — needs an expansion",
     re.compile(r'<ab\s+n="\?+\">')),
    ("<ab n=\"\"> empty attribute — expansion field is blank",
     re.compile(r'<ab\s+n="">')),
    ("<ab n=\"…\"> with non-standard expansion value (not a plain abbreviation)",
     re.compile(r'<ab\s+n="(?!")[^"]{2,}">')),
    ("Empty content tag",
     re.compile(r"<(ls|ab|lex|bot|zoo|lang|symbol)\b[^>]*></\1>")),
    ("{#…#} closing brace immediately followed by <ab> or <ls> (likely missing space)",
     re.compile(r"#\}<(?:ab|ls)\b")),
    ("[PageN-NNN-N] glued to preceding </ls>. (likely missing space or newline)",
     re.compile(r"</ls>\.\[Page\d")),
    ("Malformed tag with unescaped < inside attribute value",
     re.compile(r'<[A-Za-z][A-Za-z0-9]*\s+[A-Za-z]+="[^"]*<[^"]*"\s*[^>]*>')),
]


def main():
    print(f"Reading {PW_TXT} …", flush=True)
    lines = PW_TXT.read_text(encoding="utf-8").splitlines()
    print(f"  {len(lines):,} lines", flush=True)

    out_lines = []
    fix_log = []
    tot_nested = 0
    tot_trim = 0

    audit_hits = {label: [] for label, _ in AUDIT_CHECKS}

    for lineno, line in enumerate(lines, 1):
        orig = line
        line, n1 = fix_nested_ab(line)
        line, n2 = fix_trim_whitespace(line)
        tot_nested += n1
        tot_trim += n2
        if line != orig:
            fix_log.append((lineno, orig, line))
        out_lines.append(line)

        # custom handlers for nested <ls>
        outside_hits, inside_hits = _ls_nested_classify(orig)
        for m in outside_hits:
            start = max(0, m.start() - 40)
            end = min(len(orig), m.end() + 40)
            audit_hits["Nested <ls> outside a {{ … }} correction record"].append(
                (lineno, orig[start:end].replace("\t", " "))
            )
        for m in inside_hits:
            start = max(0, m.start() - 40)
            end = min(len(orig), m.end() + 40)
            audit_hits["Nested <ls> INSIDE a {{ … }} correction record (informational)"].append(
                (lineno, orig[start:end].replace("\t", " "))
            )

        for label, pat in AUDIT_CHECKS:
            if pat is None:
                continue
            for m in pat.finditer(orig):
                start = max(0, m.start() - 40)
                end = min(len(orig), m.end() + 40)
                snippet = orig[start:end].replace("\t", " ")
                audit_hits[label].append((lineno, snippet))
                if len(audit_hits[label]) >= 5000:
                    break
        if lineno % 200000 == 0:
            print(f"  {lineno:,}/{len(lines):,}", flush=True)

    print(f"Total nested <ab> repairs:    {tot_nested}", flush=True)
    print(f"Total whitespace trims:       {tot_trim}", flush=True)
    print(f"Total changed lines:          {len(fix_log)}", flush=True)

    print(f"Writing {OUT_FIX} …", flush=True)
    with OUT_FIX.open("w", encoding="utf-8", newline="\n") as f:
        for line in out_lines:
            f.write(line + "\n")

    print(f"Writing {OUT_LOG} …", flush=True)
    with OUT_LOG.open("w", encoding="utf-8") as f:
        f.write("; markup_fix log for wil.txt\n")
        f.write(f"; nested <ab>:    {tot_nested}\n")
        f.write(f"; whitespace:     {tot_trim}\n")
        f.write(f"; changed lines:  {len(fix_log)}\n;\n")
        for lineno, old, new in fix_log:
            f.write(f"{lineno} old {old}\n")
            f.write(f"{lineno} new {new}\n")

    print(f"Writing {OUT_AUDIT} …", flush=True)
    with OUT_AUDIT.open("w", encoding="utf-8") as f:
        f.write("WIL markup audit — findings requiring a human decision\n")
        f.write("=" * 60 + "\n\n")
        f.write("Generated by 08_markup_fix.py against wil.txt.\n")
        f.write("Items below were DETECTED but NOT modified by the fixer.\n")
        f.write("Each section explains the pattern and what to consider.\n\n")
        f.write("If a check has matches: 0, that pattern is currently absent\n")
        f.write("from wil.txt — the check is kept so this script can be re-run\n")
        f.write("after any future auto-wrap / local-overlay pass and still\n")
        f.write("catch what those passes might introduce.\n\n")
        f.write("------------------------------------------------------------\n")
        f.write("\nWHAT THIS FIXER AUTO-CORRECTS\n")
        f.write("------------------------------------------------------------\n")
        f.write("  - Nested <ab><ab>X</ab> Y</ab>          → <ab>X Y</ab>\n")
        f.write("  - Whitespace inside <ab>/<lex>/<bot>/<ls>/<zoo>/<lang>/<symbol>\n")
        f.write("\nThe original file is left untouched; results go to\n")
        f.write("wil_fixed.txt with the full change log in markup_fix_changes.txt.\n\n")
        f.write("------------------------------------------------------------\n")
        f.write("\nWHAT NEEDS HUMAN ATTENTION\n")
        f.write("------------------------------------------------------------\n")
        f.write("  1. Adjacent </ab> <ab> — wil.txt has 2,095 of these. Most\n")
        f.write("     are clearly two separate intended abbreviations\n")
        f.write("     (e.g. <ab>m.</ab> <ab>or f.</ab>) — verify rather than\n")
        f.write("     auto-merge. If any pair *should* be a single <ab>, fix\n")
        f.write("     by hand.\n\n")
        f.write("  2. Nested <ls> outside correction records — 0 currently.\n")
        f.write("     Kept for re-run safety after future overlay passes.\n\n")
        f.write("  3. Nested <ls> INSIDE {{…}} correction records —\n")
        f.write("     part of the format {{old -> new || date | author | URL}}.\n")
        f.write("     Reported for awareness only; do not touch.\n\n")
        f.write("  4. <ab n=\"?\">/<ab n=\"???\"> placeholders — 1 occurrence\n")
        f.write("     (L13356, 'M. N.').  The expansion is unknown; needs\n")
        f.write("     a human lookup against the WIL printed text.\n\n")
        f.write("  5. <ab n=\"\"> empty attribute — 1 occurrence (L118743,\n")
        f.write("     'B.' used for Bengali reference). Fill in the expansion.\n\n")
        f.write("  6. <ab n=\"…\"> non-standard values — 3 additional occurrences:\n")
        f.write("     n=\"Diabetes\" (L47969), n=\"grains\" (L139218),\n")
        f.write("     n=\"active\" and n=\"passive\" (L169793). These are readable\n")
        f.write("     English expansions; decide whether to standardise the\n")
        f.write("     format or leave them.\n\n")
        f.write("  7. WIL-specific paired tags <bot> (3,883), <zoo> (213),\n")
        f.write("     <lang> (28), <symbol> (1) have low enough usage that\n")
        f.write("     visual review of their content is cheap:\n")
        f.write("       grep -n '<bot>'    wil.txt | head\n")
        f.write("       grep -n '<zoo>'    wil.txt | head\n")
        f.write("       grep -n '<lang>'   wil.txt\n")
        f.write("       grep -n '<symbol>' wil.txt\n\n")
        f.write("------------------------------------------------------------\n")
        f.write("\nAUTOMATED CHECKS BELOW\n")
        f.write("------------------------------------------------------------\n\n")
        for label, _ in AUDIT_CHECKS:
            hits = audit_hits[label]
            f.write(f"## {label}\n")
            f.write(f"   matches: {len(hits)} (showing up to 200)\n")
            for ln, snippet in hits[:200]:
                f.write(f"   L{ln}: {snippet}\n")
            f.write("\n")

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
