arr=[1,2,3,4]

result =[]
prd = 1
for i in range(len(arr)):
  prd = 1
  for j in range(len(arr)):
    if i == j:
      continue
    else:
      prd *=arr[j]
  print(prd)
  result.append(prd)
print(result)


# 2 logic