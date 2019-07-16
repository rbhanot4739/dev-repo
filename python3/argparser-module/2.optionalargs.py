if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help="Verbose output", action='store_true')
    parser.add_argument('--num1', help="First number")
    parser.add_argument('--num2', help="Second number")
    parser.add_argument('--opr', help="Operation to be performed")
    args = parser.parse_args()

    if args.num1 and args.num2:
        if args.opr == 'add':
            res = int(args.num1) + int(args.num2)
            print("Result of {2} operation on arguments {0},{1} = {3}".format(args.num1, args.num2, args.opr, res))
