import csv

infile = open(r'2014Elections.csv', "rt")
outfile = open(r'out.csv', 'w', newline='')
reader = csv.reader(infile, delimiter=',')
writer = csv.writer(outfile)

# Fetching the headers form input csv file
for row in reader:
    writer.writerow([row[0], row[3], row[5], 'Voter Difference'])
    break

for row in reader:
    state = row[0]
    male_voters = int(row[3])
    female_voters = int(row[5])
    voter_diff = male_voters - female_voters
    writer.writerow([state, male_voters, female_voters, voter_diff])

infile.close()
outfile.close()
