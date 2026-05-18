import re
import sys

def wrap_len(s):
    # Strip XML/HTML tags for standard wrap length calculation
    clean = re.sub(r'<[^>]+>', '', s)
    return len(clean)

def visible_len(s):
    # Strip XML/HTML tags
    clean = re.sub(r'<[^>]+>', '', s)
    # Strip braces, hashes, percent signs
    clean = clean.replace("{", "").replace("}", "").replace("#", "").replace("%", "")
    return len(clean)

def combined_wrap(text, max_std=82, max_vis=82):
    # Splits by space and wraps keeping visible length <= 82 and wrap_len <= 82
    words = text.split(" ")
    lines = []
    current_line = []
    current_std_len = 0
    current_vis_len = 0
    
    for word in words:
        if not word:
            continue
        word_std = wrap_len(word)
        word_vis = visible_len(word)
        
        added_std = current_std_len + 1 + word_std if current_line else word_std
        added_vis = current_vis_len + 1 + word_vis if current_line else word_vis
        
        if added_std > max_std or added_vis > max_vis:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_std_len = word_std
            current_vis_len = word_vis
        else:
            current_line.append(word)
            current_std_len = added_std
            current_vis_len = added_vis
            
    if current_line:
        lines.append(" ".join(current_line))
    return lines
def process_lex_tags(line):
    # Process grammatical tags <lex>
    def replace_lex(match):
        content = match.group(1)
        if content in ('ind.', 'ind'):
            after_text = line[match.end():].strip()
            if not after_text:
                return 'ind.'
            else:
                return '{%ind.%}'
        elif content in ('adj.', 'adv.', 'pron.', 'subst.', 'Adj.', 'Pron.', 'Subst.'):
            # Check if it is already wrapped in {%...%}
            is_already_wrapped = False
            start_idx = match.start()
            end_idx = match.end()
            if start_idx >= 2 and line[start_idx-2:start_idx] == '{%':
                if end_idx + 2 <= len(line) and line[end_idx:end_idx+2] == '%}':
                    is_already_wrapped = True
            if is_already_wrapped:
                return content
            return f'{{%{content}%}}'
        else:
            return content
            
    return re.compile(r'<lex>(.*?)</lex>').sub(replace_lex, line)

def preprocess_line(line):
    # Process <lex> tags
    line = process_lex_tags(line)
    # Convert <ab>E.</ab> to .E.
    line = line.replace('<ab>E.</ab>', '.E.')
    # Strip other <ab> tags
    line = re.sub(r'<ab>(.*?)</ab>', r'\1', line)
    # Strip <ls> tags
    line = re.sub(r'<ls>(.*?)</ls>', r'\1', line)
    # Replace -{# with {#-
    line = line.replace('-{#', '{#-')
    # Replace ∙ with .
    line = line.replace('∙', '.')
    # Replace \t with space
    line = line.replace('\t', ' ')
    # Collapse multiple spaces
    line = re.sub(r' +', ' ', line)
    return line.strip()

def convert_ab_to_cdsl(text):
    # Replace the preamble with the gold standard preamble
    first_l_idx = text.find("<L>")
    if first_l_idx != -1:
        gold_preamble = (
            "1%***This_File_is_E:\\SANSKRIT\\WILSON\\WILSON.ALL,_Last_update_28.06.06\n\n"
            "A Dictionary, Sanscrit and English. HH Wilson 2nd edition, Calcutta 1832\n\n"
            "[Page1]\n"
            "<H>{#a#}\n\n"
        )
        body = text[first_l_idx:]
    else:
        gold_preamble = ""
        body = text

    # Preprocess page markers at the end of entries (e.g., `<LEND> [Page2]`)
    body = re.sub(r'<LEND>\s+\[Page(\d+)\]', r'[Page\1]\n\n<LEND>', body)
    
    # Split into entries
    entries = re.split(r'(<L>.*?<LEND>)', body, flags=re.DOTALL)
    
    output = []
    for entry in entries:
        if not entry.strip():
            continue
            
        if not entry.startswith("<L>"):
            # Text outside L tags (e.g. trailing lines of the file, or unexpected comments)
            output.append(entry.strip())
            continue
            
        raw_lines = entry.split('\n')
        
        # 1. Clean and split inline sense headers like `.²1`
        cleaned_lines = []
        for line in raw_lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Repeatedly split inline sense starts (preceded by whitespace)
            current_line = line
            while True:
                match = re.search(r'\s+[∙.]²([1-9])\s+', current_line)
                if match:
                    idx = match.start()
                    part1 = current_line[:idx].strip()
                    part2 = current_line[match.end():].strip()
                    sense_num = match.group(1)
                    if part1:
                        cleaned_lines.append(part1)
                    current_line = f".²{sense_num} " + part2
                else:
                    cleaned_lines.append(current_line)
                    break
        
        # 2. Group into paragraphs
        paragraphs = []
        current_para = None
        
        for line in cleaned_lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            starts_new = False
            para_type = 'body'
            
            if line_stripped.startswith("<L>"):
                starts_new = True
                para_type = 'L'
            elif line_stripped.startswith("<LEND>"):
                starts_new = True
                para_type = 'LEND'
            elif line_stripped.startswith("[Page"):
                starts_new = True
                para_type = 'page'
            elif line_stripped.startswith(".²") or line_stripped.startswith("∙²"):
                starts_new = True
                para_type = 'dot2'
            elif line_stripped.startswith(".E.") or line_stripped.startswith("<ab>E.</ab>"):
                starts_new = True
                para_type = 'etym'
            elif line_stripped.startswith("<div"):
                # Extract text after <div...> and check if it starts with [Ww]ith
                text_part = re.sub(r'<div[^>]*>', '', line_stripped).strip()
                clean_text = text_part.replace("{%", "").replace("%}", "").strip()
                if clean_text.lower().startswith("with"):
                    starts_new = True
                    para_type = 'div'
                else:
                    # Treat as a continuation line of the current paragraph
                    starts_new = False
            elif line_stripped.startswith("{#") and "¦" in line_stripped:
                starts_new = True
                para_type = 'headword'
            elif current_para is None:
                starts_new = True
                para_type = 'body'
                
            if starts_new:
                if current_para is not None:
                    paragraphs.append(current_para)
                current_para = {'type': para_type, 'lines': [line_stripped]}
            else:
                if para_type == 'body' and line_stripped.startswith("<div"):
                    # Strip the div tag and treat as plain text continuation
                    text_part = re.sub(r'<div[^>]*>', '', line_stripped).strip()
                    current_para['lines'].append(text_part)
                else:
                    current_para['lines'].append(line_stripped)
                
        if current_para is not None:
            paragraphs.append(current_para)
            
        # 3. Format and wrap paragraphs
        entry_lines = []
        for para in paragraphs:
            if para['type'] == 'L':
                entry_lines.extend(para['lines'])
            elif para['type'] == 'LEND':
                entry_lines.append("") # Blank line before <LEND>
                entry_lines.extend(para['lines'])
            elif para['type'] == 'page':
                entry_lines.extend(para['lines'])
            elif para['type'] == 'div':
                entry_lines.extend(preprocess_line(l) for l in para['lines'])
            else:
                para_lines = []
                joined_text = " ".join(preprocess_line(l) for l in para['lines'])
                joined_text = re.sub(r' +', ' ', joined_text)
                
                parts = re.split(r'(\[Page\d+\])', joined_text)
                for idx, part in enumerate(parts):
                    if not part:
                        continue
                    if part.startswith('[Page'):
                        para_lines.append(part)
                    else:
                        wrapped = combined_wrap(part)
                        if idx > 0 and wrapped:
                            wrapped[0] = " " + wrapped[0]
                        if idx + 1 < len(parts) and wrapped:
                            wrapped[-1] = wrapped[-1] + " "
                        para_lines.extend(wrapped)
                entry_lines.extend(para_lines)
                
        output.append("\n".join(entry_lines))
        
    final_output = []
    for item in output:
        item = item.strip()
        if item:
            final_output.append(item)
            
    return gold_preamble + "\n".join(final_output) + "\n"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ab2cdsl.py input_file output_file")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    converted = convert_ab_to_cdsl(content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"Converted {input_file} to {output_file}")
