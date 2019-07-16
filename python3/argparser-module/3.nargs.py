if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--opr", help="Operation to be performed", choices=['sum', 'max', 'min'])
    parser.add_argument("--nums", help="List of numbers", nargs='*', type=int)  # Nargs = '+' one ore more args,
    # Nargs = '*' 0 or more args

    args = parser.parse_args()

    if args.opr == 'sum':
        res = sum(args.nums)
    elif args.opr == 'min':
        res = min(args.nums)
    elif args.opr == 'max':
        res = max(args.nums)

    print('The numbers passed to program are {}'.format(args.nums))
    print("{} of args is {}".format(args.opr, res))
