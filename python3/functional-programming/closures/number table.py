def table1(rows):
    def table2(cols):
        i = 1
        while i < rows + 1:
            k = i
            for j in range(k, k * (cols + 1), k):
                print("{:5d}".format(j), end="")
            print()
            i += 1

    return table2


t5 = table1(10)
t2 = table1(4)
t5(11)
t2(20)
