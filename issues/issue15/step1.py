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

    processed = []
    for line in temp_lines:
        result = tag_pattern.sub(r'<lex>\1</lex> \2\n', line)
        result = standalone_pattern.sub(r'<lex>\1</lex>\n', result)
        result = result.replace('.E.', ' <ab>E.</ab>')

        r_with_content = re.search(r'<lex>r\.</lex>.*?(\({#.*?#}\))', result)
        if r_with_content:
            end_pos = r_with_content.end(1)
            before_paren_end = result[:end_pos]
            after_paren_end = result[end_pos:]
            result = before_paren_end + '\n' + after_paren_end

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

    def should_not_merge_with_prev(line, prev_line):
        return (prev_line.strip().endswith(')') or
                prev_line.strip().endswith('</lex>') or
                prev_line.strip().endswith('</ab>'))

    for i, line in enumerate(flat_lines):
        if i > 0 and not starts_new_block(line) and not should_not_merge_with_prev(line, flat_lines[i-1]):
            final_lines[-1] = final_lines[-1] + ' ' + line
        else:
            final_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(final_lines) + '\n')

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'temp_wil_0.txt')
    output_file = os.path.join(script_dir, 'temp_wil_1.txt')
    process_file(input_file, output_file)
