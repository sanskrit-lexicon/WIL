### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `wil.txt`.

I ran the same two-job recipe over `csl-orig/v02/wil/wil.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `wilissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — would value a look at the 5 `<ab n="…">` attribute oddities and the 760 within-line adjacent `</ab> <ab>` cases.

## Markup fixer + audit for `wil.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>fem.</ab> or masc.</ab>` | `<ab>fem. or masc.</ab>` |
| `<ab n=X><ab>St.</ab></ab>` | `<ab n=X>St.</ab>` |
| `<ab>foo<ab>bar</ab>baz</ab>` | `<ab>foobarbaz</ab>` |
| `<ab>S. W. </ab>` | `<ab>S. W.</ab>` |
| `<lex> m. </lex>` | `<lex>m.</lex>` |

Whitespace trimming applies to all 7 paired tags that actually occur in `wil.txt`: `<ab>`, `<lex>`, `<bot>`, `<ls>`, `<zoo>`, `<lang>`, `<symbol>`. The original file is never modified — output goes to `wil_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format).

### Closing-tag inventory in current `wil.txt`

| Tag | Count |
|---|---:|
| `</ab>` | 67,797 |
| `</lex>` | 53,028 |
| `</bot>` | 3,883 |
| `</ls>` | 230 |
| `</zoo>` | 213 |
| `</lang>` | 28 |
| `</symbol>` | 1 |

No self-closing tags. Every open/close count matches at the file level (tag-balanced). `wil.txt` uses 7 paired tag types. Tags present in PWK but absent here: `<is>`, `<hom>`, `<gk>`, `<iw>`, `<arab>`, `<span>`.

### What it found in current `wil.txt`

- **0** nested `<ab>` — clean. The nesting fixer is retained for re-runs after any future auto-wrap overlay pass.
- **1** whitespace trim — applied: L294494, trailing space inside `<ab>S. W. </ab>` → `<ab>S. W.</ab>`. `wil_fixed.txt` differs from source by exactly this one line.
- **5** `<ab n="…">` attribute occurrences with non-standard values (all within `wil.txt`'s 6 total n= attributes):
  - L13356 — `<ab n="???">M. N.</ab>` — genuine expansion-unknown placeholder.
  - L47969 — `<ab n="Diabetes">D.</ab>` — readable English expansion; decide whether to keep or encode as an abbreviation entry.
  - L118743 — `<ab n="">B.</ab>` — empty expansion field; likely a Bengali reference needing a value.
  - L139218 — `<ab n="grains">grs.</ab>` — readable English expansion.
  - L169793 — `<ab n="active">a.</ab>` and `<ab n="passive">p.</ab>` — grammatical voice labels.
- **0** nested `<ls>` — clean, outside and inside correction records alike. (280 `{{old → new || …}}` correction records are present; nested `<ls>` inside them is the format, not a bug — kept as an informational audit row for re-runs.)
- **0** boundary collisions — `wil.txt` is clean on `{#…#}<ab>/<ls>`, `</ls>.[Page…]`, and malformed-attribute patterns.
- **760** within-line adjacent `</ab> <ab>` — listed in `markup_audit.txt` for verification (2,095 total when matching across line boundaries too). Spot checks show mostly intentional pairs such as `<ab>m.</ab> <ab>or f.</ab>`; verify rather than auto-merge.

### Broader cleanup checklist (in `markup_audit.txt`)

1. **Adjacent `</ab> <ab>`** (760 within-line, 2,095 total) — verify each pair is intentional; fix by hand any that should be a single `<ab>`.
2. **`<ab n="">` empty expansion** (1 occurrence, L118743) — fill in the expansion for `B.`.
3. **`<ab n="???">` placeholder** (1 occurrence, L13356) — look up `M. N.` in the printed WIL text and supply the expansion.
4. **`<ab n="…">` non-standard values** (3 further occurrences) — decide whether to standardise `"Diabetes"`, `"grains"`, `"active"`, `"passive"` or leave them as human-readable tooltips.
5. **Low-frequency paired tags** — `<bot>` (3,883), `<zoo>` (213), `<lang>` (28), `<symbol>` (1) are cheap to review visually; `markup_audit.txt` notes grep commands for each.
6. **Nested `<ab>` / nested `<ls>` guards** — both currently 0; kept in the fixer so any future overlay pass can be re-audited automatically.

### Usage

```
cd wilissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/wil/wil.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `wil_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

`wil.txt` is tag-balanced across all 7 paired tag types. One auto-fix was applied (L294494 trailing space in `<ab>`). There are no boundary collisions and no nested tags of any kind. The non-trivial findings are 6 `<ab n="…">` attribute oddities (1 empty, 1 placeholder, 4 non-standard values) and 760 within-line adjacent `</ab> <ab>` pairs for human verification.

### Severity

`minor`
