s1 = "listen"
s2 = "silent"

if sorted(s1) == sorted(s2):
    print ("anagram")
else:
    print("Not Anagram")





if len(s1) != len(s2):
    print("Not anagram")
else:
    counter = {}
for char in s1:
    counter[char] = counter.get(char,0)+1
for char in s2:
    if char not in counter:
        print("Not Anagram")
        break
    counter[char]-=1

    if counter[char]<0:
        print("Not Anagrama")
        break
else:
    print("anagram")
