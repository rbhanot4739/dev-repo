import csv, glob

path = r'C:\Users\erotbht\Documents\Study\Python\data_files\2014*.csv'
outputCsvFile = open(r'2014Elections.csv', 'w', newline='')
csvWriter = csv.writer(outputCsvFile)

for fname in glob.glob(path):
    inputCsvFile = open(fname, "rt")
    csvReader = csv.reader(inputCsvFile, delimiter=',')
    for row in csvReader:
        if csvReader.line_num != 1:
            csvWriter.writerow(row)
    inputCsvFile.close()
outputCsvFile.close()
