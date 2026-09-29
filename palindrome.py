s= "madam"
reverse = ""

for char in s:
    reverse = char+reverse

print(reverse)

if s == reverse:
    print("palindrome")
else:
    print("Not")