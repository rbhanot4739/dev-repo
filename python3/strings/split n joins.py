str1 = "This is a sample string seperated by space"
print(str1)

list1 = str1.split(" ")
print("Split fxn returns a list", list1)

i = "sample"

if i in list1:
    print(i)

# Join operation

str2 = "-".join(list1)

print()

print(str2)

str3 = "#"

tup1 = ('Hello', 'how', 'are', 'you')

print(tup1)

print(str3.join(tup1))

str4 = "Hello"

print("|".join(str4))

str5 = "Hello How are you! What's up!"
list2 = str5.split(" ", 1)
print(list2)

str6 = list2[-1]

print(str6.split("!"))
