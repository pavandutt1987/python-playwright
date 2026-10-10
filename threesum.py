nums = [-1,2,1,-4]
target = 1
closest_sum = nums[0]+nums[1]+nums[2]
for i in range(len(nums)):
  for j in range(i+1,len(nums)):
    for k in range(j+1,len(nums)):
     total =  nums[i]+nums[j]+nums[k]
    
    if abs(target-closest_sum) > abs(target-total):
            closest_sum = total
print(closest_sum)