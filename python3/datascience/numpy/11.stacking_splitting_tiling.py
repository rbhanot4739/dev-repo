import numpy as np

# Stacking and Splitting array
a1 = np.arange(4).reshape(2, 2)
a2 = np.arange(4).reshape(2, 2)

print(np.hstack((a1, a2)))
print(np.vstack((a1, a2)))

print('\n\n\n')
a3 = np.arange(36).reshape(6, 6)
print('\n', np.hsplit(a3, 2))
print('\n', np.vsplit(a3, 2))

# Tiling arrays

a = np.arange(1, 5).reshape(2, 2)

print('\n\n', np.tile(a, (3, 2)))
