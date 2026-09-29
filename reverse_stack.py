s = "hello"

stack =[]

for ch in s:
    stack.append(ch)
print(stack)

reverse = []

while stack:
    reverse.append(stack.pop())
reverse_string = " ".join(reverse)

print(reverse_string)