import os, re
import subprocess as sb

match_pat = input("Enter the text you want to search for: ")
# top = input("Enter the full path where you want to search:  ")
top = "/apps/nttech/rbhanot/Documents"
pat = re.compile(match_pat)


def grepper(top, pat):
    for path, dirlist, name in os.walk(top):
        fpath = (os.path.join(path, n) for n in name)
        try:
            for file in fpath:
                if 'text' in sb.check_output("file " + file,
                                             shell=True).decode().strip('\n'):
                    with open(file, "r") as f:
                        line_num = 0
                        for line in f:
                            line_num += 1
                            if re.search(pat, line):
                                yield (
                                    "{1:>2d} : {0}".format(file, line_num))
        except Exception as e:
            print(e)


gp = grepper(top, pat)
for l in gp:
    print(l)
