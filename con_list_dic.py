keys = ["name", "age", "city"]
values = ["John", 30, "Hyderabad"]
#zip(keys, values) pairs corresponding items, and dict() converts those pairs into a dictionary.
result = dict(zip(keys,values))
print (result)