capitals = {"India": "New Delhi", "USA": "Washington", "Germany": "Berlin", "France": "Paris"}
print()
print("Printing the dictionary", capitals)
print("Printing the dictionary items by dict.items() ---->", capitals.items())
print("Printing the dictionary keys by dict.keys() ---->", capitals.keys())
print("Printing the dictionary values by dict.values() ---->", capitals.values())

print()
print("Removing elements from dictionary with del dict[key] --- USA in this case")
del capitals["USA"]
print(capitals)

print("Adding elements to dictionary with dict[key] = value --- capitals['Spain'] ='Madrid' in this case")
capitals["Spain"] = "Madrid"
print(capitals)

print("Length of dictionary is len(dict)  ", len(capitals))
