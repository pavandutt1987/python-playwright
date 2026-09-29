def combination1(n,k):
    result=[]
    exp_result= []
    for i in range(1,n):
        for j in range(i+1,n):
            exp_result = [i,j]
            result.append(exp_result)
            exp_result =""
    print(result)


combination1(4,3)

