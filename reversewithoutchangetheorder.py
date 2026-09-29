s="Python Playwright automation"

words = s.split(" ")
reverse = " "

for word in words:
    reverse += word[::-1] + " "
print(reverse)