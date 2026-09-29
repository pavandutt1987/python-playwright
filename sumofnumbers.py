num = 123456
sum = 0
while num !=0:
    no = num%10
    sum+=no
    num = num//10
print(sum)


num = 12345
total = 0
for digit in str(num):
    total += int(digit)

print(total)