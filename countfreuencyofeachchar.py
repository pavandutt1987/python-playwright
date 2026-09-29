s="python playwright python selenium playwright python"
result = {}

for char in s:
    result[char] = result.get(char,0)+1

print(result)