import json

jsonObj = '{"Rohit": {"City": "Noida", "Age": 29}, "Mohit": {"City": "Mumbai", "Age": 25}}'
dict1 = json.loads(jsonObj)
print(dict1)
for key in dict1:
    print(key, dict1[key])

jsonArr1 = '["Red", "Yellow", "Blue"]'
list1 = json.loads(jsonArr1)
print(list1)
