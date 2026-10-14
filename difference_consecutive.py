a = [10,15,25,40,60]

res = [a[i+1] - a[i ] for i in range(len(a)-1)]
print(res)

result = [j - i for i,j in zip(a[:-1],a[1:])]
print(result)