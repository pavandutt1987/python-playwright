arr = [10, 25, 4, 90, 12]

for i in range (len(arr)):
    for j in range(len(arr)-i-1):
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1],arr[j]
print(arr)

print("Large",arr[-1])

large = sec_lat =0
for num in arr:
    if num > large:
        sec_lat = large
        large =num
    if large > num >sec_lat:
        sec_lat = num
print(sec_lat)
