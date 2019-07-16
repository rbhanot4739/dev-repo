import pickle
import shelve

states = ['UP', 'PUNJAB', "Gujrat"]
cities = ('Mumbai', 'Delhi', 'Pune')
players = {'India': "Kohli", 'NZ': 'Williamson'}

with open('data.pick', 'wb') as OF:
    pickle.dump(states, OF)
    pickle.dump(cities, OF)
    pickle.dump(players, OF)

with open('data.pick', 'rb') as IF:
    st = pickle.load(IF)
    ct = pickle.load(IF)
    pl = pickle.load(IF)

print(st)
print(ct)
print(pl)

shelf = shelve.open('shelfdata')
shelf['states'] = states
shelf['cities'] = cities
shelf['pl'] = players

shelf.close()

shelf = shelve.open('shelfdata')
for key in shelf:
    print(key)
