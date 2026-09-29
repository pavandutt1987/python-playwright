s= "pavandutt"
duplicatechar = {}
for char in s:
    duplicatechar[char] = duplicatechar.get(char,0)+1

for char , count in duplicatechar.items():
    if count > 1:
        print(f"{char} : {count}")

# Using Set
s= "pavandutt"

for char in set(s):
    count = s.count(char)

    if count>1:
        print(f"{char}:{count}")

# Using collections 
from collections import Counter
count = Counter(s)
for char,count in count.items():
    if count>1:
        print(f"{char}:{count}")