s = "I love coding"

arr = s.split(" ")
result = ""

print(arr[::-1])
for i in range(len(arr)-1,-1,-1):
   result +=(arr[i])+" "
print(result)