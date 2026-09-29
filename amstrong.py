s= "153"
sun = 0
for i in range(len(s)):
     num = int(s[i])
     sun += num**3

print(sun)

if (int(s) == sun):
     print("Armstrong number")
