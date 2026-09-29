# def find_pairs(arr , sum):
#     for i in range (len(arr)):
#         for j in range(i+1, len(arr)):
#             if arr[i] +arr[j] ==10:
#                print (arr[i] , arr[j])
# find_pairs([1, 5, 3, 7, 9, 2], 10)

arr = [1, 5, 3, 7, 9, 2] 
sum = 10
seen = set()
for num in arr:
    diff = sum -num
    if diff in seen:
        print(f'{diff} + {num} = {sum}')
    seen.add(num)
