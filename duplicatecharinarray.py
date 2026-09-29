chars = ['d','a','c','b','a','d']

from collections import Counter

count = Counter(chars)

for char,count in count.items():
    if count>1:
        print(f"{char}:{count}")

# 2 nd logic
result = {}
for char in chars:
    result[char] = result.get(char,0)+1

for char,count in result.items():
    if count>1:
        print(f"{char}:{count}")

# 3RD LOGIC

result1 = {}
for char in chars:
    if char in result1:
        result1[char]+=1
    else:
        result1[char] =1
for char,count in result1.items():
    if count>1:
        print(f"{char}:{count}")