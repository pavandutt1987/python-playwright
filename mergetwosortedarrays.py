
# Two-pointer merge works when both arrays are sorted
# in the same order.

# Ascending + Ascending -> works
# Descending + Descending -> works with adjusted comparison
# Ascending + Descending -> first normalize one array


arr1 = [1,3,5,7]
arr2=[4, 6, 8, 10]
#arr2 = [10,8,6,4] --> We need to sort this array in ascending order first before merging
result = []

result = arr1+arr2
print(result)

for i in range(len(result)):
    for j in range (len(result)-1-i):
        if result[j] > result[j+1]:
            result[j],result[j+1] = result[j+1],result[j]
print(result)



result1=[]
i=0
j=0

while i< len(arr1) and j<len(arr2):
    if arr1[i] < arr2[j]:
        result1.append(arr1[i])
        i+=1
    else:
        result1.append(arr2[j])
        j+=1

result1.extend(arr2[j:])
print(result1)
