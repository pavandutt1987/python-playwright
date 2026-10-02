s= "programming"

seen = []
duplicates = []

for ch in s:
    if ch not in seen:
        seen.append(ch)
    else:
        duplicates.append(ch)

print(duplicates)
print("".join(seen))
    