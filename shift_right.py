arr = [1,2,3,4,5,6,7,8,9,10]
k=9
# mod = k % len(arr)  # Use modulo to handle cases where k is larger than the array length
# for i in range(mod):  # Use modulo to handle cases where k is larger than the array length
#     last = arr.pop()
#     arr.insert(0,last)
# print (arr)
n = len(arr)
if k>n:
    k= k%n  # Use modulo to handle cases where k is larger than the array length
arr = arr[-k:] + arr[:-k]  # Use slicing to rotate the array
print(arr)
# left shift
arr = arr[k:] + arr[:k]
print (arr)