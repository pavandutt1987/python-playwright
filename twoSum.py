l1 = [2, 4, 3]
l2 = [5, 6, 4,5]

i=0
result=[]
carry = 0
while i < len(l1) or i< len(l2) or carry:
  val1 = l1[i] if i <len(l1) else 0
  val2 = l2[i] if  i< len(l2) else 0

  total = val1+val2+carry

  digit = total%10
  carry = total //10

  result.append(digit)
  i+=1
print(result)
