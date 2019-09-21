from time import time


def left_rotate_array(a, factor):
    """
    input array = [1, 2, 3, 4, 5, 6]
    factor = 2
    output array = [3, 4, 5, 6, 1, 2]
    """

    for _ in range(factor):
        temp = a[0]
        for i in range(len(a) - 1):
            a[i] = a[i + 1]
        a[len(a) - 1] = temp

    return a
    # print(f"Array rotated left by {factor} elements {a}")


def right_rotate_array(a, factor):
    length = len(a)
    for _ in range(factor):
        temp = a[length - 1]
        for i in range(length):
            a[length - 1 - i] = a[length - 2 - i]
        a[0] = temp
    print(f"Array rotated right by {factor} elements {a}")


def rotate_array(a, factor):
    n = len(a)
    gcd = get_gcd(n, factor)
    for i in range(0, gcd):
        temp = a[i]
        j = i

        while True:
            k = j + factor
            if k >= n:
                k -= n
            if k == i:
                break
            a[j] = a[k]
            j = k
        a[j] = temp

    return a


def get_gcd(a, b):
    for i in range(9, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


arr = list(range(1, 10000000))
# print('Original array ===>', arr)
t = time()
rotate_array(arr, 4)
print(f"{time() - t:.3f} seconds")
t = time()
left_rotate_array(arr, 4)
print(f"{time() - t:.3f} seconds")
# right_rotate_array(list(range(1, 7)), 2)
