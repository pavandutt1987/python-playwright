num = [1, 2, 2, 3, 1, 4]

# numset = set(num)

# num = sorted(numset)
# print(num)

seen = set()
result =[]

for item in num:
    if item not in seen:
        seen.add(item)
        result.append(item)
print(result)