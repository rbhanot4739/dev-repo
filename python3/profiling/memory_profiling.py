# Decorate the function(s) you want to profile with the Profile decorator and
# run from commandline as 'python <script_name>'

from memory_profiler import profile, memory_usage
from sys import getsizeof


@profile(precision=3)
def main():
    squares = (x * x for x in range(1000000))
    print('Size of Generator expression with 1000000 values => {} bytes'.format(getsizeof(squares)))

    print("Total Memory occupied by program after creating the big Generator => {} MB".format(memory_usage()[0]))
    print('*' * 50)
    print("Total Memory occupied by program before creating the big list => {} MB".format(memory_usage()[0]))

    square_list = [x * x for x in range(1000000)]
    print('Size of List comprehension with 1000000 values => {} MB'.format(getsizeof(square_list) / 1024 / 1024))
    print("Total Memory occupied by program after creating the big list => {} MB".format(memory_usage()[0]))


if __name__ == "__main__":
    print("Total Memory occupied by program before creating the big Generator => {} MB ".format(memory_usage()[0]))
    main()
