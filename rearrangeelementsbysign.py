nums = [3,1,-2,-5,2,-4]
result = []
# [3,-2,1,-5,2,-4]

i=0
j=0
while i < len(nums):
    if nums[i] > 0:
        result.append(nums[i])
    else:
        if result[i-1] and result[i-2] > 0:
             result.insert(i-1,nums[i])
        else:
           result.append(nums[i])
    i+=1

print(result)


nums = [3,1,-2,-5,2,-4]
result = []
# [3,-2,1,-5,2,-4]

for num in nums:
    if num >0:
        result.append(num)
    else:
        if result and result[-1] >0:
            result.insert(len(result)-1,num)
        else:
            result.append(num)

print(result)

