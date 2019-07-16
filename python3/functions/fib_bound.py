def fibonacci(n):
    (first, last) = (0, 1)
    while last < n:
        first, last = last, last + first

    next = first + last
    if n == last:
        return (first, next)
    else:
        return (first, last)


# main body
if (__name__ == "__main__"):
    x = int(input("Please enter any number: "))
    (small, large) = fibonacci(x)
    print("The previous fibonacci number before {} is {}".format(x, small))
    print("The next fibonacci number after {} would be {}".format(x, large))
else:
    print()
