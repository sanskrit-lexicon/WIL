wil_AB_1.1.txt obtained from <https://github.com/sanskrit-lexicon/csl-corrections/issues/10#issuecomment-4466084543> on 17 May 2026

temp_wil_0.txt copied from csl-orig/v02/wil/wil.txt as on commit 837b40b16424eff6b7def975385b37e7b606cca5 on 17 May 2026.

# Process adopted

0. `cd sanskrit-lexicon/csl-orig` and  `git show 837b40b16424eff6b7def975385b37e7b606cca5:v02/wil/wil.txt > temp_wil_0.txt` - This generates the starting version of CDSL data.
1. `python3 step1.py` - This generates `temp_wil_1.txt` from `temp_wil_0.txt`. i.e. it generates a version from CDSL data programmatically.
2. `python3 step2.py` - This generates `temp_wil_2.txt` from `wil_AB_1.1.txt` i.e. it generates a version from AB data programmatically.
3. `cp temp_wil_2.txt temp_wil_3.txt`. A few manual changes were made in `temp_wil_3.txt`.
4. `diff temp_wil_0.txt temp_wil_2.txt > log2.diff` - this file stores the differences between the CDSL data and AB data. It was cursorily checked. AB data was consistently found to be providing better data and markup.
5. `diff temp_wil_2.txt temp_wil_3.txt > log3.diff` - This file stores the manual changes made in `temp_wil_3.txt` file.

# Structural Differences between AB Format and CDSL Format

This document outlines the major structural differences between the AB format and the CDSL format as observed in the examples provided.

## 1. Tags and Markup

- **AB Format:** Uses XML-like tags for semantic markup:
  - `<lex>...</lex>` for grammatical categories (e.g., `<lex>ind.</lex>`, `<lex>m.</lex>`).
  - `<ab>...</ab>` for abbreviations (e.g., `<ab>neg.</ab>`, `<ab>E.</ab>`).
  - `<div>` or `<div n="p">` for paragraph divisions.
- **CDSL Format:** Removes these tags entirely, leaving only the text content (with some specific text markers).

## 2. Special Markers and Bullet Points

- **AB Format:** Uses the bullet character `∙` followed by superscript numbers (e.g., `∙²1`, `∙²2`) to denote senses.
- **CDSL Format:** Replaces the bullet `∙` with a standard dot `.` (e.g., `.²1`, `.²2`).
- **AB Format:** Uses `<ab>E.</ab>` to mark etymology.
- **CDSL Format:** Replaces it with the text marker `.E.`.

## 3. Layout and Indentation

- **AB Format:** Uses tabs for indentation of senses and etymology blocks.
- **CDSL Format:** Removes leading tabs and left-aligns the text.
- **AB Format:** Often places the first sense (`∙²1`) on the same line as the headword and grammatical info if they fit.
- **CDSL Format:** Moves the first sense to a new line.

## 4. Entry Separation and Terminator (`<LEND>`)

- **AB Format:**
  - There is **no blank line** before `<LEND>`.
  - There is a **blank line** between entries (after `<LEND>` and before the next `<L>`).
- **CDSL Format:**
  - There is a **blank line** before `<LEND>`.
  - There is **no blank line** between entries (the next `<L>` follows immediately after `<LEND>`).

## 5. Line Wrapping

- **CDSL Format** appears to be hard-wrapped at around 75-80 characters, which may break lines in the middle of sentences.
- **AB Format** preserves more structured line breaks based on list items or semantic blocks.
