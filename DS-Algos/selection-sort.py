def selection_sort(a):
    n = len(a)

    for i in range(n):
        min = a[i]
        for j in range(i + 1, n):
            if a[j] < min:
                a[i] = a[j]
                a[j] = min
                min = a[i]
    return a


print(selection_sort([7, 16, 2, 4, 9, 13, 1, 15]))
