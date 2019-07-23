# https://realpython.com/python-itertools/

# Problem Statement
# You have three $20 dollar bills, five $10 dollar bills, two $5 dollar bills, and five $1 dollar bills.
# How many ways can you make change for a $100 dollar bill?

import itertools as it

bills = list(it.chain.from_iterable([[20]*3, [10]*5, [5]*2, [1]*5]))

total_combinations = (it.combinations(bills, i) for i in range(5, len(bills)))
comb_100s = []
count = 0
for combination in total_combinations:
    for val in combination:
        count += 1
        if sum(val) == 100:
            comb_100s.append(val)

print(set(comb_100s), count)

# Here’s a variation on the same problem:
# How many ways are there to make change for a $100 bill using any number of $50, $20, $10, $5, and $1 dollar bills?

bills = [1, 5, 10, 20]

total_combinations = (it.combinations_with_replacement(bills, i) for i in range(3, 51))
comb_100s = []

for combination in total_combinations:
    for val in combination:
        if sum(val) == 100:
            comb_100s.append(val)

print(len(comb_100s))
