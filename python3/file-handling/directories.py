import os, shutil

print("\n The current directory is : ****", os.getcwd(), "****")
pwd = os.getcwd()
print('\nPlease change directory to some other directory & list its contents')
os.chdir("C:\\Users\\erotbht\\Documents\\Study\\Python\\TestFolder")
list1 = os.listdir(os.getcwd())
print("\nNow the current directory is : ****", os.getcwd(), "****\n")
for i in list1:
    print(i, end=" ")

print("\n\nLets go back to our previous directory")
os.chdir(pwd)
print("\nLets create a new directory named testdir and cd into it and then create a new file in it")

if ("testdir" in os.listdir()):
    print("Directory already exists !!")
else:
    os.mkdir("testdir")
    print("Directory created")

with open("testdir\\testfile", "w") as newFH:
    print()
list2 = os.listdir("testdir")
print("Listing the contents of the testdir")
for i in list2:
    print(i)  # # print("Now lets delete the directory testdir with its contents")
# # shutil.rmtree("testdir")
