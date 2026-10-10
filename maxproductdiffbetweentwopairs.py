nums = [5,6,2,7,4]
output = 34
result = []

for i in range(len(nums)):
    for j in range(i+1,len(nums)):
        if (nums[i]*nums[j]) not in result:
            result.append(nums[i]*nums[j])

max_number = max(result)
print(result)

print(max_number)
for num in result:
    if max_number - num == 34:
        print(max_number,num)


#2 logic
nums = sorted(nums)

diff = nums[-1]*nums[-2] - nums[0]*nums[1]
print(diff)

