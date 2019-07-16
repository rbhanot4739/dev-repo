# Decorate the function(s) you want to profile with the Profile decorator and
# run from command line as `kernprof -l -v cpu_profiling.py` this will display output on terminal
# to send the output to a file and then analyse it later run `kernprof -l cpu_profiling.py` and then analyse
# with this command `python -m line_profiler cpu_profiling.py.lprof`

@profile
def main():
    gen_squares = (x * x for x in range(100000))
    for _ in gen_squares:
        pass

    sq = [x * x for x in range(100000)]
    for _ in sq:
        pass


if __name__ == '__main__':
    main()
