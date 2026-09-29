num  = 123
def numberrev(num):
    sign = -1 if num < 0 else 1
    num = abs(num)
    rev = 0
    while num>0:
        num1 =num %10
        print(num1)
        rev =(rev * 10)+num1
        print(rev)
        num = num//10
        print(num)
    return sign * rev
    # s = str(num)
    # rev = ""
    # for ch in s:
    #     rev = ch+rev
    # return rev

print(int(numberrev(1534236469)))