s = "Big black bug bit a big black dog on his big black nose"
#s= s.replace("."," ").tolower()

words = s.split(" ")
duplicates ={}

for word in words:
    duplicates[word]= duplicates.get(word,0)+1

for word , count in duplicates.items():
    if count>1:
        print(f"{word} : {count}")
    