import random

print("*****Sorting list of integers*****\n")
# Creating a random list of integers
l1 = [random.randint(2, 30) for i in range(10)]
print("\tUnsorted values in list -> ", l1)
print("\tSorted values in list ->", sorted(l1))

print("\n*****Sorting a list of tuples*****")
# tup1=[(chr(random.randint(97,122)),random.randint(2,15)) for i in range(5)]

tup1 = [('d', 10), ('o', 4), ('u', 21), ('b', 6), ('m', 76), ('y', 1)]

print("\nUnsorted List of Tuples ->", tup1)

print("\tSorted list of tuples based on 1st element ->", sorted(tup1, key=lambda i: i[0]))
print("\tSorted list of tuples based on 2nd element ->", sorted(tup1, key=lambda i: i[1]))

print("\n*****Sorting a dictioanry*****\n")

d1 = {'Punjab': 87376742, 'U.P': 162365645, 'Kerala': 1356482, 'Rajasthan': 71637653, 'Manipur': 653278}

print("Unsorted dictionary", d1.items())

print("\tDictionary sorted on the basis of key ->", sorted(d1.items(), key=lambda i: i[0]))
print("\tSDictionary sorted on the basis of value ->", sorted(d1.items(), key=lambda i: i[1]))

# Sorting a list of dictionaries based on dictionary key rank
a = [{'rank': 3, 'name': 'test3'}, {'rank': 1, 'name': 'test1'}, {'rank': 2, 'name': 'test2'}]
print(sorted(a, key=lambda dct: dct['rank']))

# Sorting a list of strings by last character of string
l = ['Delhi', 'Bombay', 'Calcutta', 'Madras', 'Banglore']
print(sorted(l, key=lambda s: s[-1]))
