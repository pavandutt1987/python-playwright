arr = [0, 3, 0, 1, 5]

# for i in range(len(arr)):
#     for j in range(len(arr)-1-i):
#         if arr[j] < arr[j+1]:
#             if arr[j] ==0:
#                 arr[j],arr[j+1] = arr[j+1],arr[j]
# print(arr)

# for num in arr:
#     if num ==0:
#         arr.remove(0)
#         arr.append(0)
# print(arr)


zero = [n for n in arr if n==0]
print(zero)
non_zero = [n for n in arr if n!=0]
print(non_zero)
arr = non_zero+zero
print(arr)

arr = [1,5,0,0,0,3,2,4,6]
j=0
for i in range(len(arr)):
    if arr[i]!=0:
        arr[i],arr[j] = arr[j],arr[i]

        j+=1
print(arr)