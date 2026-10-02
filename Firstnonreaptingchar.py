s="aabbcddee"
#Your logic is fine if the interviewer specifically says: "duplicates are adjacent". Otherwise, use the frequency-map approach.
i=0
while i < len(s)-1:
    if s[i] != s[i+1]:
        print("First Non reapting char ", s[i])
        break
    else:
       i+=2

#2 login using count
for ch in s:
    if s.count(ch)==1:
        print("First Non reapting char is logic2 ",ch)

#3 use dic 
freq={}

for ch in s:
    freq[ch] = freq.get(ch,0)+1
print(freq)

for ch , count in freq.items():
    if count ==1:
        print("non repating char is logic3 ",ch)



