nums = [0,0,1,1,1,2,2,3,3,4]

seen = set(nums)
print(seen)

seen1 = set()
for num in nums:
    if num not in seen1:
        seen1.add(num)
print(seen1)

result = {}
for num in nums:
    result[num] = result.get(num,0)+1

for num,count in result.items():
    print(f"{num}: {count}")