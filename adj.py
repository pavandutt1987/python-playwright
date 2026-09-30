s = "abbacab"

i=0

stack = []

for char in s:
    if stack and stack[-1] == char:
        stack.pop()
    else:
        stack.append(char)
result = "".join(stack)
print(result)


# while i < len(s) -1:
#     if s[i] == s[i+1]:
#         s= s[:i]+s[i+2:]
#         print(s)
#         i=0
#     else:
#         i +=1

# Wrong apporach
# for i in range(len(s)):
#     print(len(s))
#     if s[i] ==s[i+1]:
#         s = s[:i]+s[i+2:]
#         print(s)
#         i=0
            