def fib(n):
    # Using for loop
    # for i in range(N):
    # third=first+second
    # print(third)
    # first=second
    # second=third

    # Using while loop
    i = 1
    first, second = 0, 1
    print(first, second, end=" ")
    while i < n:
        third = first + second
        print(third, end=" ")
        first = second
        second = third
        i += 1


if __name__ == '__main__':
    n = int(input("Enter the last digit till which you want Fibonacci series : \n"))
    fib(n)
