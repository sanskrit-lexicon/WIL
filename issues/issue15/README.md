wil_AB_1.1.txt obtained from https://github.com/sanskrit-lexicon/csl-corrections/issues/10#issuecomment-4466084543 on 17 May 2026

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
