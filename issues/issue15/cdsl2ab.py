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


import os

LEXS = ["m.", "n.", "f.", "mfn.", "ind.", "r.", "mn."]
BOTS = []
ZOOS = []

if os.path.exists("wil_AB_1.1.txt"):
    print("Loading tags from wil_AB_1.1.txt...")
    with open("wil_AB_1.1.txt", "r", encoding="utf-8") as f:
        ab_text = f.read()
        
    def extract_tags(text, tag_name):
        pattern = f"<{tag_name}>(.*?)</{tag_name}>"
        return set(re.findall(pattern, text))
        
    extracted_lex = extract_tags(ab_text, "lex")
    if extracted_lex:
        LEXS = list(extracted_lex)
        # Filter out messy ones
        LEXS = [l for l in LEXS if len(l) < 10]
        
    extracted_bot = extract_tags(ab_text, "bot")
    if extracted_bot:
        BOTS = list(extracted_bot)
        # Sort by length descending to match longer phrases first
        BOTS.sort(key=len, reverse=True)
        
    extracted_zoo = extract_tags(ab_text, "zoo")
    if extracted_zoo:
        ZOOS = list(extracted_zoo)
        # Sort by length descending
        ZOOS.sort(key=len, reverse=True)
        
    print(f"Loaded {len(LEXS)} lex categories, {len(BOTS)} botanical names, and {len(ZOOS)} zoological names.")
else:
    print("wil_AB_1.1.txt not found. Using default LEXS.")


def convert_cdsl_to_ab(text):
    entries = re.split(r'(<L>.*?<LEND>)', text, flags=re.DOTALL)
    
    bot_regex = None
    if BOTS:
        bot_pattern = r"(<[^>]+>.*?</[^>]+>)|\b(" + "|".join(re.escape(b) for b in BOTS) + r")\b"
        bot_regex = re.compile(bot_pattern)
        
    zoo_regex = None
    if ZOOS:
        zoo_pattern = r"(<[^>]+>.*?</[^>]+>)|\b(" + "|".join(re.escape(z) for z in ZOOS) + r")\b"
        zoo_regex = re.compile(zoo_pattern)
        
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
            
            # Move punctuation outside of % and # tags
            line = re.sub(r"([.,:;])%}", r"%}\1", line)
            line = re.sub(r"([.,:;])#}", r"#}\1", line)
            
            # Restore tabs after ¦
            if line.startswith("{#"):
                line = line.replace("¦ ", "¦\t ")
                
            # Restore <ab>E.</ab>
            if line.startswith(".E."):
                line = line.replace(".E.", "\t <ab>E.</ab>\t")
                
            # Convert {%ind%}. to <lex>ind.</lex>
            line = line.replace('{%ind%}.', '<lex>ind.</lex>')
            line = line.replace('{%ind%}', '<lex>ind.</lex>')
            
            # Convert <bio> to <zoo>
            line = line.replace('<bio>', '<zoo>').replace('</bio>', '</zoo>')
            
            for lex in LEXS:
                # Use regex to handle space or tab before lex
                line = re.sub(r"([ \t])" + re.escape(lex), r"\1<lex>" + lex + "</lex>", line)
                    
            # Restore <ab> tags
            for ab in ABS:
                # Use regex to handle space or tab before ab
                line = re.sub(r"([ \t])" + re.escape(ab), r"\1<ab>" + ab + "</ab>", line)
                    
            # Restore <bot> tags
            if bot_regex:
                line = bot_regex.sub(lambda m: m.group(1) if m.group(1) else f"<bot>{m.group(2)}</bot>", line)
                
            # Restore <zoo> tags
            if zoo_regex:
                line = zoo_regex.sub(lambda m: m.group(1) if m.group(1) else f"<zoo>{m.group(2)}</zoo>", line)
                
            # Split on embedded lex (often following a period)
            line = line.replace(". <lex>", ".\n\t <lex>")
                
            # Add tab before definition
            line = re.sub(r"\) ([A-Z\u00C0-\u017F]|{%)", r")\t \1", line)
            line = re.sub(r"</lex> ([A-Z\u00C0-\u017F]|{%)", r"</lex>\t \1", line)
            
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
