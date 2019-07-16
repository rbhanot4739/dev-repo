if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--Ifile', help='Input File', type=argparse.FileType('r'))
    parser.add_argument('-o', '--Ofile', help='Output File', type=argparse.FileType('w'))
    args = parser.parse_args()

    for line in args.Ifile:
        cube = int(line.rstrip()) ** 3
        args.Ofile.write(str(cube))
        args.Ofile.write('\n')
