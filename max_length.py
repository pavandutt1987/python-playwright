s = "abcdabacad"
left =0
seen = {}
max_length = 0
max_string = " "

for right in range(len(s)):
    if s[right] in seen and seen[s[right]] >= left:
        left = seen[s[right]] + 1
    seen[s[right]] = right
    if right - left + 1 > max_length:
        max_length = right - left + 1
        max_string = s[left:right + 1]

print(f"Maximum length: {max_length}")
print(f"Maximum substring: {max_string}")