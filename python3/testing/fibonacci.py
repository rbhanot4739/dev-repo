def fib(n):
    fibs = []
    i = 1
    first, second = 0, 1
    # fibs.extend([first,second])

    # Using for loop
    for i in range(n):
        third = first + second
        fibs.append(third)
        first = second
        second = third

    # Using while loop

    # while i < n:
    #     third = first+second
    #     first=second
    #     second=third
    #     i+=1
    #     fibs.append(third)
    if fibs:
        return fibs
    else:
        return None


if __name__ == '__main__':
    n = int(input("Enter the last digit till which you want Fibonacci series : \n"))
    val = fib(n)
    print(val)
