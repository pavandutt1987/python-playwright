list1 = [1,2,2,3,4,5]
list2 = [2,2,4,5,5,6]
seen = []
for num in list1:
  if num in list2 and num not in seen:
    seen.append(num)
print(seen)


import copy

a=[2,3,4]
b= copy.copy(a)
#b= copy.deepcopy(a)
print(b)
b.append(5)
b[1].append(6)
print(b)
print(a)
