arr = [0, 3, 0, 1, 5,0 ,0 ,2]

# for i in range(len(arr)):
#     for j in range(len(arr)-1-i):
#         if arr[j] > arr[j+1]:
#             if arr[j+1] ==0:
#                 arr[j],arr[j+1] = arr[j+1],arr[j]
# print(arr)

# for i in range(len(arr)):
#     if arr[i] ==0:
#         arr.pop(i)
#         arr.insert(0,0)
# print(arr)


for i in range(len(arr)):
    if arr[i] == 0:
        arr.pop(i)
        arr.insert(0,0)
print(arr)