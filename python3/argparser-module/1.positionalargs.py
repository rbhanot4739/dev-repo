if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("arg1", help="First argument")
    parser.add_argument("arg2", help="Second arguement")
    parser.add_argument("opr", help="Operation to be performed")

    args = parser.parse_args()
    if args.opr == 'add':
        res = int(args.arg1) + int(args.arg2)

    print("Result of {2} operation on arguments {0},{1} = {3}".format(args.arg1, args.arg2, args.opr, res))
