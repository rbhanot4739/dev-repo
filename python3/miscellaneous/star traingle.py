n = 50
k = int(input("Enter the number of rows for pyramid : "))
for i in range(1, k):
    print(' ' * (k - i), '* ' * (i))
