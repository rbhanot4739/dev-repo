list1 = [1, 2, 3, 4, 5]
print("\nShallow Copy illustration ---> list2 = list1 \n")

list2 = list1
print("List1 is :", list1)
print("List2 is :", list2)

print("\nNow we are going to do 'del list1[1]' and will see how it affects both the lists \n")
del list1[1]
print("List1 is :", list1)
print("List2 is :", list2)

print("\nLets try Deep Copy now ---> list4 = list3[:]\n")
list3 = [n * n for n in list1]
list4 = list3[:]
print("List3 is :", list3)
print("List4 is :", list4)

print("\nNow lets try to do 'del list3[1]' again and see how it affects both the lists\n")
del list3[1]
print("List3 is :", list3)
print("List4 is :", list4)
