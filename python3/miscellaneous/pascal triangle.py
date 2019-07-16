pas = []
n = 9
for i in range(n):
    if i == 0:
        pas.append([1])
    elif i == 1:
        pas.append([1, 1])
    else:
        temp = []
        for j in range(0, i - 1):  # 2
            tmp = pas[i - 1][j] + pas[i - 1][j + 1]
            temp.append(
                tmp)  #  temp = [pas[i - 1][j] + pas[i - 1][j + 1] for j in range(0, i - 1)] - Using List comprehensions
        temp.insert(0, 1)
        temp.append(1)
        pas.append(temp)

for i in pas:
    n = 50 - (len(i))
    # print(n)
    k = " ".join(map(str, i))
    print(' ' * n, end="")
    print("{:{w}}".format(k, w=n))
