s="coding"

vowels = "aeiouAEIOU"
index = []

for i in range(len(s)):
    if s[i] in vowels:
        index.append(i)
    
print(index)

left = 0
right = len(index)-1
s = list(s)
while left < right:
    s[index[left]], s[index[right]]= s[index[right]],s[index[left]]
    left+=1
    right-=1
s="".join(s)
print(s)
        