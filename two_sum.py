
print("What does the Visualize button do?")
# def two_sum(arr,sum):
#   result1=[]
#   group =[]
#   indicies=[]
#   for num in  arr:
#     number = sum - num
#     if number in arr:
#       if num and number not in group:
#         group.append(num)
#         group.append(number)
#   result1.append(group)
#   print(result1)
#   for i in range(len(arr)):
#         if arr[i] in list(group):
#             indicies.append(i)
#         print("Indices of the two numbers that add up to the target:",indicies)


def two_sum(arr, target):
    seen = []
    indices = []
    for i in range(len(arr)):
        for j in range (i+1,len(arr)):
            if arr[i] + arr[j] == target:
                seen.append((arr[i], arr[j]))
                indices.append((i, j))
    print("Pairs of numbers that add up to the target:", seen)
    print("indices of numbers that add up to the target:", indices)
    

two_sum([2, 7,1, 11, 8, 15], 9)

      
  