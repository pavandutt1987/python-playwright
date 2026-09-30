# s = "pa*van*dutt*"
# stack=[]

# for ch in s:
#     if ch=='*':
#         stack.pop()
#     else:
#         stack.append(ch)
# print("".join(stack))

s="pavandutt"
stack1 =[]
for ch in s:
    if stack1 and ch == stack1[-1]:
        stack1.pop()
    else:
        stack1.append(ch)
print("".join(stack1))

