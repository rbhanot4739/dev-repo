import numpy as np

a = np.arange(101, 116).reshape(3, 5)
b = np.random.randint(50, 70, size=(4, 5), dtype=int)

# np.savetxt saves an array in text file

np.savetxt('test.txt', a, fmt="%.1f", delimiter=',')
np.savetxt('test.txt', a, fmt="%d", delimiter=',', header='This is the header', footer='This is the footer')

# np.save saves an array in a binary file
# np.savez can save multiple arrays at once into a binary file

np.save('array_data', a)
np.savez('arrays_data', a, b)
