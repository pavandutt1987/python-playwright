head = [1,2,3,4,5]
for i in range(0,len(head)-1,2):
  head[i],head[i+1] = head[i+1],head[i]
  print(head)
print(head)
