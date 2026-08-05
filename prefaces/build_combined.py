"""Build the consolidated single-file edition of the WIL 1819 front matter.

Reads wil1819prefNN.md page files (YAML frontmatter + body) in order and writes
wil1819pref_all.en.md (source language is English, so the source edition IS the
English edition). Reuses the data-driven pattern of Wil-YAT/prefaces/build_combined.py.
"""
import sys, os, re, glob
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = 'wil1819pref'

LANGS = {
  'src': ('.md', f'{CODE}_all.en.md', 'WIL 1819 (first edition) front matter — complete (English, source)', 'Page', 'Source (scan)'),
}

def split(text):  # drop opening YAML block + first H1; return (meta, body)
    meta = {}; L = text.splitlines(); i = 0
    if L and L[0].strip() == '---':
        i = 1
        while i < len(L) and L[i].strip() != '---':
            m = re.match(r'\s*([A-Za-z_]+):\s*(.*)$', L[i])
            if m: meta[m.group(1)] = m.group(2).strip()
            i += 1
        i += 1
    while i < len(L) and not L[i].strip(): i += 1
    if i < len(L) and L[i].lstrip().startswith('# '): i += 1
    while i < len(L) and not L[i].strip(): i += 1
    return meta, '\n'.join(L[i:]).rstrip()

def slug(s):
    s = re.sub(r'[^\w\s-]', '', s.lower(), flags=re.UNICODE)
    return re.sub(r'\s+', '-', s.strip())

pages = sorted(glob.glob(os.path.join(HERE, f'{CODE}[0-9][0-9].md')))
for lang, (suf, outname, title, pw, srcw) in LANGS.items():
    out = [f'# {title}\n',
           '**Edition = 1819 first ed.** — H. H. Wilson, *A Dictionary, Sanscrit and English*, '
           'Calcutta: Philip Pereira, Hindoostanee Press, 1819. This is NOT the 1832 second edition '
           '(the CDSL `wil` text); see [README.md](README.md).\n',
           f'Per-page files: `{CODE}NN{suf}`. Index: [README.md](README.md).\n', '## Contents\n']
    body = []
    for de in pages:
        nn = re.search(r'(\d\d)\.md$', de).group(1)
        src = de[:-3] + suf if suf != '.md' else de
        if not os.path.exists(src): continue
        meta, txt = split(open(src, encoding='utf-8').read())
        pp = meta.get('printed_page', '')
        h = f'{pw} {nn} — {meta.get("source_page","")}' + (f' (p. {pp})' if pp else '')
        out.append(f'- [{h}](#{slug(h)})')
        txt = re.sub(r'(?m)^(#{1,5})(\s)', r'#\1\2', txt)
        body.append(f'\n---\n\n## {h}\n\n<sub>{srcw}: [{meta.get("source_scan","")}]({meta.get("source_url","")})</sub>\n\n{txt}\n')
    open(os.path.join(HERE, outname), 'w', encoding='utf-8').write('\n'.join(out + body).rstrip() + '\n')
    print('wrote', outname, f'({len(body)} pages)')
