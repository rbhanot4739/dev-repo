def counting(path):
    tabs = 0
    spaces = 0
    lines = 0
    fh = open(path, "r")
    for i in fh:
        tabs += i.count("\t")
        spaces += i.count(" ")
        lines += 1
    fh.close()
    print(spaces, "----", tabs, "----", lines)


if __name__ == "__main__":
    path = input("Please enter the file path :")
    counting(path)
