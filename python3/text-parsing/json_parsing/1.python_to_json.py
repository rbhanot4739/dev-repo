import json

dict1 = {'Rohit': {'City': 'Noida', 'Age': 29}, 'Mohit': {'City': 'Mumbai', 'Age': 25}}
jsonObj = json.dumps(dict1)
print(jsonObj)

list1 = [1, 2, 3, 4]
jsonArr1 = json.dumps(list1)
print(jsonArr1)

tup1 = ('Yellow', 'Black', 'Blue')
jsonTup1 = json.dumps(tup1)
print(jsonTup1)
