import re
import os

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines() if line.strip()]

    lextags_with_paren = ['mfn\\.', 'mn\\.', 'mf\\.', 'nf\\.', 'adv\\.', 'subst\\.', 'adj\\.', 'sub\\.', 'pron\\.',
               'm\\.', 'f\\.', 'n\\.', 'ind\\.']
    tag_pattern = re.compile(r'((?:' + '|'.join(lextags_with_paren) + r'))\s*(\({#.*?#}\))')

    lextags_standalone = ['mfn\\.', 'mn\\.', 'mf\\.', 'nf\\.', 'adv\\.', 'subst\\.', 'adj\\.', 'sub\\.', 'pron\\.',
               'm\\.', 'f\\.', 'n\\.', 'ind\\.', 'r\\.', 'fn\\.', 'Subst\\.', 'subst\\.']
    standalone_pattern = re.compile(r'(?:^|(?<=\s)|(?<=¦))(' + '|'.join(lextags_standalone) + r')(?=\s|$)')

    output_lines = []
    for line in lines:
        if '¦' in line:
            parts = line.split('¦', 1)
            before = parts[0]
            after = parts[1]
            if after.strip():
                output_lines.append(before + '¦')
                output_lines.append(after)
            else:
                output_lines.append(line)
        else:
            output_lines.append(line)

    temp_lines = []
    for line in output_lines:
        r_sub = re.sub(r'(?:^|(?<= ))r\.\s*', '<lex>r.</lex> ', line)
        idx = r_sub.find('<lex>r.</lex> ')
        if idx > 0:
            part_before = r_sub[:idx].rstrip()
            part_after = r_sub[idx:]
            if part_before:
                temp_lines.append(part_before)
            temp_lines.append(part_after)
        else:
            temp_lines.append(r_sub)

    ab_tags = ['passive v.', 'plur.', 'viz.', 'prep.', 'plu.', '&c.', 'neut.', 'mas.', 'privat.', 'nom. v.', 'penult.', 'sing.', 'du.', 'pl.', 'part.', 'fem.', 'pre.', 'desider.', 'antepen.', 'pers.', 'caus.', 'pen.', 'acc.', 'desid.', 'superl.', 'dim.', 'gen.', 'causal v.', 'priv.', 'frequent.', 'past.', 'Sing.', 'aff.', 'der.', 'fig.', 'deriv.', 'patron.', 'E.', 'affs.', 'irr.', 'liter.', 'N. W.', 'reg.', 'desid. v.', 'lit.', 'nominal v.', 'met.', 'ff.', 'dat.', 'abl.', 'augm.', 'N. E.', 'intensitive v.', 'accu.', 'dimin.', 'a.', 'aug.', 'q. v.', 'S. W.', 'redup.', 'S. E.', 'ut sup.', 'form.', 'do.', 'possess.', 'var.', 'redup. v.', 'poss.', 'posses.', 'ante-pen.', 'S. W. ', 'cent.', 'masc.', 'comp.', 'neg.', 'pass.', 'pref.', 'cl.', 'Mss.', 'MSS', 'fut.', 'metaph.', 'oz.', 'lbs.', 'affir.', 'intens.', 'inten.', 'reiter. v.', 'abst.', 'freq. v.', 'pass. v.', 'cls.', 'pos.', 'Ex.', 'vulg.', 'i. e.', 'intens. v.', 'frequent. v.', 'reit. v.', 'super.', 'nom.', 'infin.', 'A. D.']
    ab_tags.sort(key=len, reverse=True)
    ab_pattern = re.compile(r'(^|\s)(' + '|'.join(re.escape(tag) for tag in ab_tags) + r')(?=\s|$|[,;\.])')

    input_dir = os.path.dirname(input_path)
    
    with open(os.path.join(input_dir, 'bot_tags.txt'), 'r', encoding='utf-8') as bf:
        bot_tags = [line.split('\t')[0].strip() for line in bf if line.strip()]
    bot_tags.sort(key=len, reverse=True)
    bot_pattern = re.compile(r'(^|[\s(])(' + '|'.join(re.escape(tag) for tag in bot_tags) + r')(?=[\s,;.)]|$)')

    with open(os.path.join(input_dir, 'zoo_tags.txt'), 'r', encoding='utf-8') as zf:
        zoo_tags = [line.split('\t')[0].strip() for line in zf if line.strip()]
    zoo_tags.sort(key=len, reverse=True)
    zoo_pattern = re.compile(r'(^|[\s(])(' + '|'.join(re.escape(tag) for tag in zoo_tags) + r')(?=[\s,;.)]|$)')

    processed = []
    for line in temp_lines:
        result = tag_pattern.sub(r'<lex>\1</lex> \2\n', line)
        result = standalone_pattern.sub(r'<lex>\1</lex>\n', result)
        result = result.replace('.E.', ' <ab>E.</ab>\n')

        # Apply <ab> tags using the single compiled regex
        result = ab_pattern.sub(r'\1<ab>\2</ab>', result)
        
        # Apply <bot> and <zoo> tags
        result = bot_pattern.sub(r'\1<bot>\2</bot>', result)
        result = zoo_pattern.sub(r'\1<zoo>\2</zoo>', result)
        
        # Fix any double-wrapped tags
        result = result.replace('<ab><ab>', '<ab>').replace('</ab></ab>', '</ab>')
        result = result.replace('<bot><bot>', '<bot>').replace('</bot></bot>', '</bot>')
        result = result.replace('<zoo><zoo>', '<zoo>').replace('</zoo></zoo>', '</zoo>')

        r_with_content = re.search(r'<lex>r\.</lex>.*?(\({#.*?#}\))', result)
        if r_with_content:
            end_pos = r_with_content.end(1)
            before_paren_end = result[:end_pos]
            after_paren_end = result[end_pos:]
            result = before_paren_end + '\n' + after_paren_end

        # Put <lex> tags that appear mid-line onto their own line
        result = re.sub(r'(?<=[^ \n])\s+(<lex>)', r'\n \1', result)

        processed.append(result)

    flat_lines = []
    for line in processed:
        flat_lines.extend([l for l in line.split('\n')])

    flat_lines = [line for line in flat_lines if line.strip()]

    final_lines = []

    def starts_new_block(line):
        return (line.startswith('<L>') or
                line.startswith('<LEND>') or
                line.startswith(' <lex>') or
                line.startswith(' <ab>') or
                line.startswith('<lex>') or
                (line.startswith('{#') and '¦' in line) or
                line.startswith('.²'))

    def should_not_merge(line, prev_line):
        return (prev_line.rstrip().endswith('¦') or
                prev_line.rstrip().endswith(')') or
                prev_line.rstrip().endswith('</lex>') or
                prev_line.rstrip().endswith('</ab>'))

    for i, line in enumerate(flat_lines):
        if i > 0 and not starts_new_block(line) and not should_not_merge(line, final_lines[-1]):
            final_lines[-1] = final_lines[-1] + ' ' + line
        else:
            final_lines.append(line)

    final_text = '\n'.join(final_lines)

    # 1. Remove leading spaces
    final_text = re.sub(r'(?m)^[ ]+', '', final_text)
    
    # 2. Ensure .² is preceded by exactly one space, but not at the start of a line
    final_text = final_text.replace('.²', ' .²').replace('  .²', ' .²')
    final_text = re.sub(r'(?m)^ \.²', '.²', final_text)

    # 3. Merge <lex> and ({#...#}) from next line, then add newline
    final_text = re.sub(r'</lex>\s*\n\s*(\({#.*?#}\))\s*', r'</lex> \1\n', final_text)

    # 4. Swap punctuation out of closing tags
    final_text = re.sub(r'([,.])%\}', r'%}\1', final_text)
    final_text = re.sub(r'([,.])#\}', r'#}\1', final_text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_text + '\n')

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'temp_wil_0.txt')
    output_file = os.path.join(script_dir, 'temp_wil_1.txt')
    process_file(input_file, output_file)
