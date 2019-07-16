names = ['Bruce Wayne', 'Clark Kent', 'Logan', 'Steve Rogers', 'Tony Stark']
hero = ['Batman', 'Superman', 'Wolverine', 'Captain America', 'Iron Man']

## Illustraion of zip fxn as well.
z = list(zip(hero, names))
print(z)

dict1 = {n: h for n, h in zip(names, hero)}
print(dict1)
