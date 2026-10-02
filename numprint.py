if __name__ == '__main__':
    n = int(input())
    result = []
    if n >0:
        for i in range(1,n+1):
            result.append(i)
    print(*result,sep ="")
            