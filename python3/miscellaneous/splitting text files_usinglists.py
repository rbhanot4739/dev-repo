# This is a script that splits a text file with large number of lines into a small files.

# from memory_profiler import profile as profile

# @profile
# @profile()
def main():
    # file_name = input("Enter the full path of file you want to split into smaller inputFiles: ")
    file_name = "/apps/nttech/rbhanot/Downloads/newtest.txt"
    input_file = open(file_name).readlines()
    num_lines_orig = len(input_file)
    # parts = int(input("Enter the number of parts you want to split in: "))
    parts = 3
    output_files = [(file_name + str(i)) for i in range(1, parts + 1)]
    st = 0
    chunk_size = num_lines_orig // parts
    ed = chunk_size
    for i in range(parts - 1):
        with open(output_files[i], "w") as OF:
            OF.writelines(input_file[st:ed])
        st = ed
        ed = st + chunk_size

    with open(output_files[-1], "w") as OF:
        OF.writelines(input_file[st:])


if __name__ == "__main__":
    main()
