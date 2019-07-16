import sys

print("Name of the script is :  ", str(str(sys.argv[0]).split(":")[-1]).split("/")[-1])

print("Other arguements of the script are: \n", "\n".join(sys.argv[:]), sep="")
