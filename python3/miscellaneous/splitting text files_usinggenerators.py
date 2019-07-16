# This is a script that splits a text file with large number of lines into smaller files using Generators.

# @profile
# @profile()
from itertools import islice


def main():
    # file_name = input("Enter the full path of file you want to split into smaller inputFiles: ")
    file_name = "/apps/nttech/rbhanot/Downloads/newtest.txt"
    with open(file_name) as input_file:
        num_lines_orig = sum(1 for _ in input_file)
        input_file.seek(0)
        # parts = int(input("Enter the number of parts you want to split in: "))
        parts = 3
        output_files = ((file_name + str(i)) for i in range(1, parts + 1))
        chunk_size = num_lines_orig // parts
        lines_written = 0
        for file in output_files:
            with open(file, "w") as OF:
                # islice for slicing the iterators
                OF.writelines(islice(input_file, chunk_size))

                lines_written += chunk_size
                # copy the remaining lines to the end of the last file
                if num_lines_orig - lines_written < chunk_size:
                    OF.writelines(input_file)
                    break


if __name__ == "__main__":
    main()
