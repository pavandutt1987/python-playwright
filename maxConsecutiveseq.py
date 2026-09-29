s= "1234512589"
start =0

current_length =1
result = {}

for i in range(1,len(s)):
    if int(s[i]) == int(s[i-1])+1:
        current_length +=1
    else:
        if current_length > 1:
            substring = s[start:i]
            result[substring] = current_length

        current_length =1
        start = i
if current_length > 1:
    substring = s[start:start + current_length]
    result[substring] = current_length

max_length = max(result.values()) if result else 0
max_substring = max(result, key=result.get) 
print(f"Maximum length: {max_length}")
print(f"Maximum substring: {max_substring}")


arr=[1,5,6,9,8,7,11,23]

print(*arr)