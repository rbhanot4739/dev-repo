import numpy as np

a = np.loadtxt('test.txt', delimiter=',')
print(a, '\n')

b = np.load('array_data.npy')
print(b)

with np.load('arrays_data.npz') as data:
    for arr in data:
        print('\n', data[arr])
