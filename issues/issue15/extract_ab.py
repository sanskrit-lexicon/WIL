import re
from collections import Counter

with open('wil_AB_1.1.txt', 'r', encoding='utf-8') as f:
    content = f.read()

ab_tags = re.findall(r'<ab>(.*?)</ab>', content)
counts = Counter(ab_tags)

# Print top 100 most common or all of them if not too many
# Let's print all unique ones sorted by frequency
for ab, count in counts.most_common():
    print(f"{ab}\t{count}")
