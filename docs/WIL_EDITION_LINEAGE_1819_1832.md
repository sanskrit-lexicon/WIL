# Wilson edition lineage — 1819 vs 1832 (PWG / MW / MW72)

_Created: 02-08-2026 · Last updated: 02-08-2026_

**Canonical home for the two Wilson print editions and how they feed the European
dictionary line.** CDSL digitises only the **1832** text; this note records the
**1819** base, the edition-split rule, OCR status, and what is (and is not) next.

## Two print editions

| Edition | Full title (short) | Place | Role in the European line |
|---|---|---|---|
| **WIL 1819** | H. H. Wilson, *A Dictionary, Sanscrit and English*, **1st ed.** | Calcutta | **Basis of PWG** (Böhtlingk–Roth). Not digitised at Cologne. |
| **WIL 1832** | same, **2nd ed.** | Calcutta (Education Press) | **Basis of MW72** English stock (over which PWG matter was added). **This** is what CDSL / this repo digitise as `wil`. |

House rule of thumb:

- **PWG relies on WIL 1819.**
- **MW (via MW72) relies on WIL 1832** for the English-gloss base; MW1899 then brings English meanings forward from MW72 and continues to rework PWG.

```text
WIL 1819  ──basis──►  PWG (1855–75)  ──condensed/reworked──►  MW 1899 (structure, cites, German philology)
WIL 1832  ──basis──►  MW72 (1872)    ──English meanings carried forward──►  MW 1899
                         ▲
                         └── PWG matter added on top of the WIL 1832 English base
```

## MW citation markers — do not collapse `L.` and `W.`

Two distinct MW `<ls>` markers sit next to this lineage; they are **not** interchangeable.

| Marker | MW's own expansion | How it relates to Wilson editions |
|---|---|---|
| **`W.`** | Wilson — words/meanings on Wilson's authority (MW 1899 preface: "All the words and meanings marked W. … rest on his authority") | Editorial cross-ref to Wilson; CDSL's Wilson text is **1832**. Count ~8,286 in MW. |
| **`L.`** | **Lexicographers** — word/meaning met only in **native lexicons**, not in a published literary work (MW 1899 preface, directions for use) | **Not** a Wilson siglum. Transmission note (MG, 02-08-2026): the European capture of the dictionary-tradition stream that MW compresses under `L.` is to be **traced into WIL 1819**, which PWG took as its print base (PWG then names individual koshas; MW collapses those named kosha-only cites into the single `L.` hedge). |

So: **surface tag** `L.` = native lexicons (MW's definition, load-bearing); **historical path** for that European stream = **WIL 1819 → PWG → MW `L.`**. Do not re-expand `L.` as "Wilson".

Cross-refs in house docs: [MWS DICT_PROFILE — citation markers](https://github.com/sanskrit-lexicon/MWS/blob/master/DICT_PROFILE.md#citation-markers--not-all-are-literary-works), [Lineage section](https://github.com/sanskrit-lexicon/MWS/blob/master/DICT_PROFILE.md#lineage-wil--koshas-mw--pwg).

## Digitisation / OCR status (Cologne)

| Edition | Full body OCR / CDSL text | Front matter (preface) |
|---|---|---|
| **WIL 1832** | **Yes** — `csl-orig/v02/wil/wil.txt` (~44,577 entries); Cologne WIL scan + this repo | Cologne / csl-doc has wilpref material for the **1832** line |
| **WIL 1819** | **No** full OCR at Cologne; not in CDSL body text | **None yet** — actionable now (see below) |

Local residue of 1819 already in this repo: sample page
[`WIL_1819_page59_iast.pdf`](https://github.com/sanskrit-lexicon/WIL/blob/main/WIL_1819_page59_iast.pdf)
(one page, not a substitute for front matter or body).

## Scope discipline (02-08-2026)

| Work | Status |
|---|---|
| Full WIL **1819** body digitisation | **Not needed now** — large task; do not open unless a human re-scopes |
| WIL **1819 preface** (front matter OCR + EN, optional RU) | **Doable now** — same `/cologne-preface-ocr` shape as other dict prefaces; park under `prefaces/` when scans are in hand |
| Treat CDSL `wil` as 1832 | Standing — never label the digitised body as 1819 |

## Implications for comparative / forensic work

1. **Edition-sensitive joins.** A headword/gloss agreement with "Wilson" is not edition-free: PWG-side ancestry expects **1819**; MW/MW72 English stock expects **1832**. Mixing them without naming the edition confounds "copied Wilson" tests.
2. **`L.` tracing.** To follow the European dictionary-tradition stream behind an MW `L.` hedge, use **WIL 1819** (and PWG's named kosha cites) as the European intermediate — not the 1832 CDSL text alone, and not by rewriting the tag expansion.
3. **`W.` tracing.** Use WIL **1832** (CDSL `wil`) for material MW marks `W.`.
4. **MW72** has **zero** `<ls>` tags ([FINDINGS §511](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md#511-mw72-carries-zero-ls-source-citations--every-cross-dictionary-citation-test-that-names-it-shrinks-to-mw)) — English-base comparison to WIL 1832 is content-level, not citation-tag-level.

## Registry / hub pointers

- Sanskrit-data finding: [FINDINGS §515](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md) (edition split + OCR gap).
- Prefaces skill: `/cologne-preface-ocr` (Fable 5 / vision OCR).
- Related repos: [PWG](https://github.com/sanskrit-lexicon/PWG), [MW72](https://github.com/sanskrit-lexicon/MW72), [MWS](https://github.com/sanskrit-lexicon/MWS).

_Dr. Mārcis Gasūns_
