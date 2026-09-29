arr = [1, 2, 2, 3, 3, 3]
seen = {}
for num in arr:
    seen[num] = seen.get(num,0)+1
print(seen)