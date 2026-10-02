s="abbacab"
i=0
while i < len(s)-1:
    if s[i] == s[i+1]:
        s = s[:i]+s[i+2:]
        print(s)
        i=0
    else:
        i+=1
