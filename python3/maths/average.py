n = 5
print("please enter 5 numbers")
count = 0
total = 0
while count < n:
    num = float(input(""))
    total += num
    count += 1
print("Sum is : ", total)
print("Average is :", total / n)
