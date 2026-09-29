arr = [1, 2, 3, 5,7]


missing = []
for num in range(1,max(arr)+1):
    if num not in arr:
        missing.append(num)
print(missing)

missing1 = []
for i in range(len(arr)-1):
    for num in range(arr[i]+1,arr[i+1]):
        if num < arr[i+1]:
            missing1.append(num)
            num+=1
print(missing1)