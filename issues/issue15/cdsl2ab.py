import re
import sys

ABS = [
    "aff.", "&c.", "cl.", "neg.", "fem.", "irr.", "deriv.", "affs.", 
    "causal v.", "cls.", "poss.", "part.", "plu.", "priv.", "desid. v.", 
    "q. v.", "pass. v.", "past.", "du.", "i. e.", "viz.", "aug.", "pen.", 
    "desid.", "do.", "sing.", "fig.", "masc.", "nom.", "plur.", "lit.", 
    "pl.", "mas.", "possess.", "vulg.", "intens.", "antepen.", "affir.", 
    "intens. v.", "N. W.", "dimin.", "frequent. v.", "dim.", "gen.", 
    "nominal v.", "patron.", "pass.", "pref.", "passive v.", "form.", 
    "pre.", "liter.", "lbs.", "desider.", "cent.", "redup.", "abl.", 
    "reit. v.", "freq. v.", "frequent.", "acc.", "metaph.", "S. W.", 
    "a.", "augm.", "superl.", "nom. v.", "super.", "reg.", "Sing.", 
    "Ex.", "ante-pen.", "met.", "penult.", "S. E.", "N. E.", "posses.", 
    "oz.", "pos.", "A. D.", "var.", "dat.", "MSS", "ut sup.", "infin.", 
    "comp.", "pers.", "privat.", "der.", "abst.", "ff.", "prep.", 
    "fut.", "caus.", "reiter. v.", "intensitive v.", "inten.", "S. W. ", 
    "Mss.", "neut.", "accu.", "redup. v."
]


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
        
        # Join continuation lines
        joined_lines = []
        for line in lines:
            if not line.strip():
                continue
            
            is_new_block = False
            if line.startswith(("<L>", "<LEND>", ".²", "∙²", ".E.", "[Page")):
                is_new_block = True
            elif line.startswith("{#") and "¦" in line:
                is_new_block = True
                
            if is_new_block:
                joined_lines.append(line)
            else:
                # This is a continuation line
                if joined_lines:
                    joined_lines[-1] = joined_lines[-1].strip() + " " + line.strip()
                else:
                    joined_lines.append(line)
                    
        new_lines = []
        for line in joined_lines:
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
            
            # Move period outside of % tag
            line = line.replace('.%}', '%}.')
            
            # Restore tabs after ¦
            if line.startswith("{#"):
                line = line.replace("¦ ", "¦\t ")
                
            # Restore <ab>E.</ab>
            if line.startswith(".E."):
                line = line.replace(".E.", "\t <ab>E.</ab>\t")
                
            for lex in LEXS:
                # Use regex to handle space or tab before lex
                line = re.sub(r"([ \t])" + re.escape(lex), r"\1<lex>" + lex + "</lex>", line)
                    
            # Restore <ab> tags
            for ab in ABS:
                # Use regex to handle space or tab before ab
                line = re.sub(r"([ \t])" + re.escape(ab), r"\1<ab>" + ab + "</ab>", line)
                    
            # Split on embedded lex (often following a period)
            line = line.replace(". <lex>", ".\n\t <lex>")
                
            # Add tab before definition
            line = re.sub(r"\) ([A-Z])", r")\t \1", line)
            
            # Add tab before senses if preceded by space
            line = line.replace(" ∙²", "\t ∙²")
            
            # Handle senses
            if line.startswith("∙²"):
                # Merge first sense back to headword line if it's the previous line
                if new_lines and new_lines[-1].startswith("{#") and "∙²" not in new_lines[-1]:
                    new_lines[-1] = new_lines[-1] + "\t " + line
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
