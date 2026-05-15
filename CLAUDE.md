# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WIL** is the corrections and research repository for the Cologne digitization of Wilson's *Sanskrit-English Dictionary* (1819). The canonical source lives in `csl-orig/v02/wil/wil.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `verbs01/` | Root identification: maps WIL verb entries to MW root spellings, identifies prefixed verbs |
| `verbs01-shs/` | Cross-reference with SHS (Shabda-Sagara) verb roots |
| `verbs01-yat/` | Cross-reference with YAT (Yates) verb roots |
| `alphawork/` | Alphabetical ordering analysis and corrections |
| `bottags/` | Analysis of `<bot>` (botanical) tags in WIL entries |
| `maprep/` | Manuscript/apparatus report analysis |

### Historical data

The repo includes `WIL_1819_page59_iast.pdf` and the `wiltab2011/` materials — correlation work between Wilson headwords and MW headwords done in 2011 by Peter Scharf and Matthias Ahlborn.

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/WIL/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh wil ../../WILScan/2020
sh xmlchk_xampp.sh wil
```

## Dependencies

- **Python 3**
- **wil.txt** — in `$BASE/cologne/csl-orig/v02/wil/wil.txt`
