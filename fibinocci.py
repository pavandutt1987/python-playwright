num =10
a=0
b = 1


result = "" 

for i in range(num):
    result += str(a) + " "
    c = a + b
    a = b
    b = c   

print(result)