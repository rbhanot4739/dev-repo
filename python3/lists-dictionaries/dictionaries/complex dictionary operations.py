dict1 = {"Chandigarh": {"Haryana", "Punjab"}, "Shimla": "HP"}
dict2 = {"Srinagar": "J&K", "Chandigarh": {"Haryana", "Punjab", "Chd"}}
print("\n Dict1 is ", dict1)
print("\n Dict2 is ", dict2)
dict1.update(dict2)  # Merging two dictionaries
print("\n Dict1 after update is ", dict1)

print("\nCreating a list of dictionary key & values using list comprehension")
capitals = [n for n in dict1.keys()]
print("\n Keys ", capitals)

states = [n for n in dict1.values()]
print("\n Values ", states)

cars = {"Honda": "City", "Toyota": "Corolla", "Fiat": "Linea", "Hyunadai": "Verna"}

print("\n cars dictionary", cars)
print("\n Creating a list from dictionary")
list_cars = list(cars.items())
print("\n", list_cars)

real_name = ['Bruce Wayne', 'Clark Kent', 'Steve Rogers', 'Tony Stark']
hero_name = ['Batman', 'Superman', 'Captain America', 'Iron Man']

superheroes = list(zip(real_name, hero_name))
print("\n Creating a dictionary from two seperate lists", superheroes)

super_heroes = dict(superheroes)
print("\n Created dictionary is ", super_heroes)
