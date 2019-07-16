import numpy as np

fh = open('1.csv')
for line in fh:
    break

a = np.loadtxt(fh, delimiter=',', dtype='i4')
print(a)
fh.close()

fh = open('2.csv')
for line in fh:
    break

a = np.loadtxt(fh, delimiter=',',
               dtype=[('Name', 'S15'), ('Age', 'i4'), ('Salary', 'i4'), ('Weight', 'f'), ('City', 'S10')])

print('\n', a)
fh.close()
