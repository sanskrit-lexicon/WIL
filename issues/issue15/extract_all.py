import re
import collections

with open("wil_AB_1.1.txt", "r", encoding="utf-8") as f:
    text = f.read()

def extract_tags(text, tag_name):
    pattern = f"<{tag_name}>(.*?)</{tag_name}>"
    matches = re.findall(pattern, text)
    return collections.Counter(matches)

lex_counts = extract_tags(text, "lex")
with open("lex_tags.txt", "w", encoding="utf-8") as f:
    for item, count in lex_counts.most_common():
        f.write(f"{item}\t{count}\n")

bot_counts = extract_tags(text, "bot")
with open("bot_tags.txt", "w", encoding="utf-8") as f:
    for item, count in bot_counts.most_common():
        f.write(f"{item}\t{count}\n")

zoo_counts = extract_tags(text, "zoo")
with open("zoo_tags.txt", "w", encoding="utf-8") as f:
    for item, count in zoo_counts.most_common():
        f.write(f"{item}\t{count}\n")

print("Done writing to files.")
