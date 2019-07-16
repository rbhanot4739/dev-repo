import pstats, sys
import subprocess as sb

inFile = sys.argv[1]
outFile = inFile.split('.')[0] + '.prof'

# This will save the stats to a file specified by outfile

p1 = sb.run(['py', '-m', 'cProfile', '-o', outFile, inFile], stdout=sb.PIPE)

# Using the below query will display the output on screen

# p1 = sb.run(['py', '-m', 'cProfile', '-s', 'cumtime', file])

stats = pstats.Stats(outFile)
stats.strip_dirs().sort_stats('cumtime').print_stats(.6)  # This will display the 60% results
