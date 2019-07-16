NAME = input("Please enter the name of the file you want to create : ")

fh = open(NAME, "a")
fh.write("This is the 1st line\n")
fh.write("This is the last line\n")
fh.close()

fh = open(NAME, "r+")
print(fh.read())
fh.write("This is a new insert\n")
print(fh.read())
fh.close()
