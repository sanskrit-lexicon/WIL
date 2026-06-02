# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WIL** is the development and correction repository for **Horace Hayman Wilson's *A Dictionary, Sanscrit and English*, 2nd edition (Calcutta, 1832)**, a Sanskrit→English dictionary, within the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL).

- **Canonical source text**: [`csl-orig/v02/wil/wil.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/wil/wil.txt) (44,577 entries) — corrections are applied to that file, not stored here.
- This repository holds **development artifacts**: Wilson↔Monier-Williams root correspondence, verb identification (Wilson / Yates / Śabda-Sāgara), botanical-name markup, and per-issue working files.
- Wilson (1832) is the **earliest** CDSL dictionary and an ancestor of later works, so much of the analysis here is comparative against MW and contemporaries.

## Architecture

| Path | Purpose |
|---|---|
| `wilmwroots/` | Wilson↔MW root correspondence: `step1/`, `step2/`, `step2a/`, `wil_mw.txt`, reason-code docs |
| `verbs01/` | Wilson verbs → MW roots: `wil_verb_filter_map*`, Devanāgarī renderings |
| `verbs01-yat/` | Yates verbs → MW (`yat_verb_filter_map`) |
| `verbs01-shs/` | Śabda-Sāgara verbs → MW (`shs_verb_filter_map`) |
| `maprep/` | Ahlborn-Scharf (2011) MW↔Wilson headword comparison (`corr6-roots.txt` etc.) |
| `wiltab2011/`, `wiltabwork/` | Wilson headword-table working files |
| `bottags/` | Botanical-name (`<bot>`) tagging work |
| `alphawork/` | Headword alphabetization |
| `issues/` | Per-issue working directories |
| `DATA_DICTIONARY.md` | Markup tag reference (see **Data format** below) |
| `CITATION.cff` | Citation metadata |

## Key commands

Corrections follow the CDSL `updateByLine.py` pattern, applied against the csl-orig source:

```sh
python updateByLine.py <input> <changefile> <output>
```

Change-file format (paired lines; `;`-prefixed comments):
```
1234 old <original line>
1234 new <replacement line>
```
Supports `new` (replace), `ins` (insert after), `del` (delete). All files UTF-8 (**no BOM** — a leading BOM breaks `hw.py` parsing).

## Data format

Wilson entries use standard CDSL Sanskrit-lexicography markup. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for the full tag reference.

| Tag | Role | Example |
|---|---|---|
| `<H>{#hw#}` | Headword-group marker (opens a set of homographic `<L>` entries) | `<H>{#a#}` |
| `<L>NNNN<pc>PPP` | Entry begin, with print page-column ref | `<L>2<pc>001` |
| `<k1>`, `<k2>` | Primary / secondary headword (SLP1) | `<k1>a<k2>a` |
| `<LEND>` | Entry end | |
| `{#…#}` | Sanskrit text (SLP1) | `{#an#}` |
| `{%…%}` | English gloss / italic display text | `{%akāra%}` |
| `¦` | Headword / definition separator (broken bar) | |
| `<lex>…</lex>` | Lexical category | `<lex>ind.</lex>` |
| `.²N` | Numbered sense within an entry | `.²1`, `.²2` |
| `<div n="p">…</div>` | Paragraph / grammatical note | |
| `<ls>…</ls>` | Literary source citation | `<ls>L.</ls>` |

Annotated example — the second entry of `wil.txt` (headword *a*, indeclinable):
```
<H>{#a#}                       # headword group "a"
<L>2<pc>001<k1>a<k2>a          # entry 2; print page 001; headword "a"
{#a#}¦                         # SLP1 headword + separator bar
<lex>ind.</lex>                # lexical category: indeclinable
.²1 No, not.                   # sense 1
.²2 A privative, prohibitive, and diminutive particle.   # sense 2
<div n="p">As a negative prefix to words beginning with a vowel, {#a#} is changed to {#an#}, as {#a#} and {#anta#} form {#ananta#}.</div>
<LEND>                         # entry end
```

## Dependencies

- Python 3 (correction and comparison scripts).
- No build step in this repo; XML and web display are generated centrally from `csl-orig` via `csl-pywork`.

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.
