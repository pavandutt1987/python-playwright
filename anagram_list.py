arr = ["eat", "tea", "tan", "ate", "nat", "bat"]
result=[]
seen =[]
# LOGIC: Loop through the array and check if the word has been seen before. If not, sort the word and compare it with the sorted version of the other words in the array. If they match, add them to a group and mark them as seen. Finally, append the group to the result list.
# for i in range(len(arr)):
#   if arr[i] not in seen:
#     word = sorted(arr[i])
#     group=[]
#     for j in range(i,len(arr)):
#         word2 = sorted(arr[j])
#         if word == word2:
#            seen.append(arr[j])
#            group.append(arr[j])
#     result.append(group)

# print(result)

# LOGIC2 : Use a dictionary to group anagrams together. Loop through the array, sort each word, and use the sorted word as a key in the dictionary. Append the original word to the list of values for that key. Finally, return the values of the dictionary as a list of lists.
group ={}
result2=[]

for word in arr:
   group_key = '' .join(sorted(word))
   if word not in group :
         if group_key not in group:
            group[group_key] = []
         group[group_key].append(word)
result2 = list(group.values())
print(result2)