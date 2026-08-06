# Audit A (vision) vs B (Tesseract) — WIL 1819 front matter

_Date: 06-08-2026 · Engine A: Claude vision OCR (Fable 5, `claude-fable-5`, subagent fan-out) · Engine B: archive.org hOCR searchtext (Tesseract) for the same leaves · pipeline: per-leaf token comparison_

Metrics normalized (lowercase, markdown stripped, `[?]`/`[illegible]` dropped). B is the
Internet Archive's own Tesseract OCR of the identical scans — an independent second channel.
Reference means for this run: Recall@A 0.81 · Jaccard 0.64 · len ratio 1.00 (53 pages).
Length ratios ~1.0 throughout = no coverage gaps in either direction.

| NN | leaf | Recall@A | Jaccard | len(B)/len(A) | Flag |
|---|---|---:|---:|---:|---|
| 01 | 6 | 0.84 | 0.69 | 1.02 | ok |
| 02 | 8 | 0.69 | 0.47 | 1.08 | ok |
| 03 | 9 | 0.96 | 0.90 | 1.02 | ok |
| 04 | 10 | 0.91 | 0.79 | 1.12 | ok |
| 05 | 11 | 0.93 | 0.81 | 1.01 | ok |
| 06 | 12 | 0.93 | 0.82 | 1.01 | ok |
| 07 | 13 | 0.96 | 0.90 | 1.00 | ok |
| 08 | 14 | 0.91 | 0.78 | 1.03 | ok |
| 09 | 15 | 0.74 | 0.49 | 1.06 | ok |
| 10 | 16 | 0.85 | 0.65 | 1.02 | ok |
| 11 | 17 | 0.85 | 0.67 | 1.00 | ok |
| 12 | 18 | 0.84 | 0.64 | 0.98 | ok |
| 13 | 19 | 0.69 | 0.43 | 0.98 | ok |
| 14 | 20 | 0.64 | 0.39 | 1.05 | ok |
| 15 | 21 | 0.88 | 0.73 | 1.02 | ok |
| 16 | 22 | 0.91 | 0.81 | 1.02 | ok |
| 17 | 23 | 0.86 | 0.68 | 1.01 | ok |
| 18 | 24 | 0.81 | 0.59 | 1.01 | ok |
| 19 | 25 | 0.84 | 0.68 | 1.00 | ok |
| 20 | 26 | 0.59 | 0.36 | 1.00 | ok |
| 21 | 27 | 0.38 | 0.18 | 1.10 | REVIEW: low recall |
| 22 | 28 | 0.61 | 0.37 | 1.07 | ok |
| 23 | 29 | 0.79 | 0.61 | 1.03 | ok |
| 24 | 30 | 0.91 | 0.81 | 0.99 | ok |
| 25 | 31 | 0.88 | 0.75 | 1.00 | ok |
| 26 | 32 | 0.83 | 0.65 | 0.99 | ok |
| 27 | 33 | 0.86 | 0.70 | 0.99 | ok |
| 28 | 34 | 0.76 | 0.58 | 1.01 | ok |
| 29 | 35 | 0.67 | 0.43 | 1.00 | ok |
| 30 | 36 | 0.58 | 0.33 | 1.02 | ok |
| 31 | 37 | 0.80 | 0.58 | 1.03 | ok |
| 32 | 38 | 0.90 | 0.75 | 1.01 | ok |
| 33 | 39 | 0.89 | 0.77 | 1.00 | ok |
| 34 | 40 | 0.78 | 0.59 | 0.99 | ok |
| 35 | 41 | 0.92 | 0.81 | 0.99 | ok |
| 36 | 42 | 0.78 | 0.57 | 1.00 | ok |
| 37 | 43 | 0.96 | 0.90 | 1.00 | ok |
| 38 | 44 | 0.89 | 0.76 | 1.00 | ok |
| 39 | 45 | 0.87 | 0.75 | 1.00 | ok |
| 40 | 46 | 0.88 | 0.70 | 1.01 | ok |
| 41 | 47 | 0.88 | 0.73 | 1.00 | ok |
| 42 | 48 | 0.88 | 0.72 | 1.01 | ok |
| 43 | 49 | 0.91 | 0.73 | 1.01 | ok |
| 44 | 50 | 0.92 | 0.60 | 0.94 | ok |
| 45 | 51 | 0.84 | 0.66 | 1.01 | ok |
| 46 | 52 | 0.70 | 0.46 | 1.03 | ok |
| 47 | 53 | 0.88 | 0.73 | 1.02 | ok |
| 48 | 54 | 0.69 | 0.54 | 0.86 | ok |
| 49 | 55 | 0.83 | 0.63 | 1.01 | ok |
| 50 | 56 | 0.94 | 0.85 | 1.01 | ok |
| 51 | 57 | 0.73 | 0.47 | 1.09 | ok |
| 52 | 58 | 0.50 | 0.30 | 0.98 | REVIEW: low recall |
| 53 | 59 | 0.40 | 0.30 | 0.66 | REVIEW: low recall |

pages compared: 53

## Flags (3, all resolved as Engine-B false positives)

### pref21 (leaf 27, p. xviii) — low recall 0.38
- Signal: B garbles this page; A prose long.
- Check: native-resolution band re-read (06-08-2026) — A matches the print verbatim; the page has the worst ink show-through of the run plus two Devanagari ślokas, which Tesseract shreds.
- Resolution: **false positive (B garbage)**.

### pref52 (leaf 58, p. xlix) — low recall 0.50
- Signal: abbreviation list (diacritic-heavy italic titles, dot leaders).
- Resolution: **false positive** — documented Engine-B weakness class (abbrev keys); len ratio 0.98 shows full coverage.

### pref53 (leaf 59, p. l) — low recall 0.40, len 0.66
- Signal: transliteration table (Devanagari + roman pairs).
- Resolution: **false positive** — B cannot read the Devanagari column; A's table verified glyph-by-glyph at native zoom (see page file notes).

## Second-copy collation (06-08-2026)

The `[?]` flags on Devanagari passages were tested against a **second independent copy** of the
1819 first edition: [archive.org: sanskritenglishdictionaryhoracehaymanwilson1819_456_T](https://archive.org/details/sanskritenglishdictionaryhoracehaymanwilson1819_456_T)
(leaf ≈ primary-copy leaf + 1; e.g. preface p. vi = primary leaf 15 = second-copy leaf 16).

| Locus | Second-copy verdict |
|---|---|
| p. vi navaratna śloka (pref09, 7 × `[?]`) | Same setting, same ink-fused conjuncts — the defect is in the **letterpress**, not the scan. Flags stand as edition-level; the verse is the well-known navaratna stanza (धन्वन्तरिः क्षपणकामरसिंहशङ्कुवेतालभट्टघटकर्परकालिदासाः…), cited here as editorial reference only, not as a reading of the print. |
| p. xlvii preface end (pref50, 1 × `[illegible]`) | **Resolved**: the second copy shows *nothing printed* below the final paragraph — the faint marks in the primary scan are ink set-off from a facing page. The preface ends without signature or dateline; pref50 carries an editorial note. |
| Remaining Devanagari `[?]` (pref13/14/17/20/21/28–30/36/43–45) | Not re-collated page-by-page; the p. vi result (same printing, same fused type) predicts the same verdict. A future pass may spot-check individual loci via the same leaf+1 mapping. |

_Dr. Mārcis Gasūns_
