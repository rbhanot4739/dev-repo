# print("This is a program to display a table till 9")
i = 1
N = 10
print(50 * "-")
while i < N + 1:
    for j in range(i, i * (N + 1), i):
        print("{:4d}".format(j), end=" ")
    print()
    i += 1
print(50 * "-")
