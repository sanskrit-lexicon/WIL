import re
import sys

def convert_ab_to_cdsl(text):
    # Split into entries
    entries = re.split(r'(<L>.*?<LEND>)', text, flags=re.DOTALL)
    
    output = []
    for entry in entries:
        if not entry.strip():
            continue
            
        if not entry.startswith("<L>"):
            output.append(entry)
            continue
            
        # Process entry
        lines = entry.split('\n')
        new_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("<L>"):
                new_lines.append(line)
                continue
                
            if line.startswith("<LEND>"):
                new_lines.append("") # Blank line before <LEND>
                new_lines.append(line)
                continue
                
            # Remove tags
            line = re.sub(r'<lex>(.*?)</lex>', r'\1', line)
            line = re.sub(r'<ab>E.</ab>', r'.E.', line)
            line = re.sub(r'<ab>(.*?)</ab>', r'\1', line)
            line = re.sub(r'<div[^>]*>', ' ', line)
            line = re.sub(r'</div>', ' ', line)
            
            # Replace bullet
            line = line.replace('∙', '.')
            
            # Normalize whitespace
            line = re.sub(r'\s+', ' ', line).strip()
            
            if not line:
                continue
                
            # Handle senses moving to new line
            if " .²1" in line:
                parts = line.split(" .²1")
                new_lines.append(parts[0].strip())
                new_lines.append(".²1 " + parts[1].strip())
                continue
                
            if line.startswith(".²") or line.startswith(".E."):
                new_lines.append(line)
            else:
                # Join with previous line if it's a continuation
                if new_lines and not new_lines[-1].startswith("<L>") and not new_lines[-1] == "":
                    new_lines[-1] = new_lines[-1] + " " + line
                else:
                    new_lines.append(line)
                    
        # Join lines for this entry
        output.append("\n".join(new_lines))
        
    # Join entries. CDSL has no blank lines between entries.
    # Wait, the split might leave whitespace between entries.
    # Let's clean up the output.
    final_output = []
    for item in output:
        item = item.strip()
        if item:
            final_output.append(item)
            
    return "\n".join(final_output) + "\n"

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
