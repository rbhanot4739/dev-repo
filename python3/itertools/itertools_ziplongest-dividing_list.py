from itertools import zip_longest


def list_divider(input, n):
    iters = [iter(input)] * n
    return zip(*iters)


def better_list_divider(input, n):
    iters = [iter(input)] * n
    return zip_longest(*iters)


for i in list_divider(range(20), 3):
    print(i)

for i in better_list_divider(range(20), 3):
    print(i)
