import re
import sys

ABS = ["neg.", "aff.", "&c.", "cl.", "pl.", "sing.", "du.", "nom."]
LEXS = ["m.", "n.", "f.", "mfn.", "ind.", "r."]

def convert_cdsl_to_ab(text):
    entries = re.split(r'(<L>.*?<LEND>)', text, flags=re.DOTALL)
    
    output = []
    for entry in entries:
        if not entry.strip():
            continue
            
        if not entry.startswith("<L>"):
            output.append(entry)
            continue
            
        lines = entry.split('\n')
        new_lines = []
        
        # Remove blank line before <LEND> in CDSL
        if len(lines) >= 2 and lines[-2].strip() == "":
            lines.pop(-2)
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("<L>"):
                new_lines.append(line)
                continue
                
            if line.startswith("<LEND>"):
                new_lines.append(line)
                continue
                
            # Replace bullets
            line = line.replace('.²', '∙²')
            
            # Restore <ab>E.</ab>
            if line.startswith(".E."):
                line = line.replace(".E.", "\t <ab>E.</ab>\t")
                
            # Restore <lex> tags on the headword line or start of line
            # This is heuristic
            for lex in LEXS:
                # If lex is at the end of the part before definition or start
                if f" {lex}" in line:
                    line = line.replace(f" {lex}", f" <lex>{lex}</lex>")
                    
            # Restore <ab> tags
            for ab in ABS:
                if f" {ab}" in line:
                    # Avoid double wrapping if already wrapped or part of something else
                    line = line.replace(f" {ab}", f" <ab>{ab}</ab>")
                    
            # Handle senses
            if line.startswith("∙²"):
                # Merge first sense back to headword line if it's the previous line
                if new_lines and new_lines[-1].startswith("{#") and "∙²" not in new_lines[-1]:
                    new_lines[-1] = new_lines[-1] + "\t" + line
                else:
                    new_lines.append("\t\t " + line)
            else:
                if line.startswith("{#"):
                    new_lines.append(line)
                else:
                    # For other lines, we might need to indent or just leave them
                    # AB has some indentation for continuation lines, but it's hard to guess.
                    new_lines.append(line)
                    
        output.append("\n".join(new_lines))
        
    # Join entries with a blank line between entries (AB format)
    final_output = []
    for item in output:
        item = item.strip()
        if item:
            final_output.append(item)
            
    return "\n\n".join(final_output) + "\n"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cdsl2ab.py input_file output_file")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    converted = convert_cdsl_to_ab(content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"Converted {input_file} to {output_file}")
