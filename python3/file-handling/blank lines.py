import re

# with open("C:\\ECD Utilization Script - Copy\\test.txt") as fh, open("C:\\ECD Utilization Script - Copy\\newtest","w") as f:
#     output_lines = []
#     for line in fh:
#         if not re.search("^$",line):
#             f.write(line.split()[-1].split(",")[0]+'\n')
#
#
#
fh = open("C:\\ECD Utilization Script - Copy\\BIND_ACCOUNTS", "r")
n = 0
for i, line in enumerate(fh):
    if re.search("^$", line):
        n = n + 1
        print(n, "Blank lines---", i, "  ----", line)
fh.close()
