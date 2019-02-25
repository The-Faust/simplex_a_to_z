from numpy import array
from simplex_modular_implementation.simplex_functions import two_phases_simplex

solvable_matrix_1 = array([
    [2.0, 3.0, 1.0, 0.0, 40.0],
    [4.0, 2.0, 0.0, 1.0, 48.0],
    [20.0, 25.0, 0.0, 0.0, 0.0]
])

summits_list_1 = two_phases_simplex(solvable_matrix_1)
for summit in summits_list_1:
    print(summit)
print()

solvable_matrix_2 = array([
    [-1.0, -2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [-2.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    [-1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0],
    [-1.0, 4.0, 0.0, 0.0, 0.0, 1.0, 0.0, 13.0],
    [4.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 23.0],
    [3.0, -6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
])

summit_list_2 = two_phases_simplex(solvable_matrix_2, opt_max=False)
for summit in summit_list_2:
    print(summit)
print()

solvable_matrix_3 = array([
    [1, 1, 1, 0, 10],
    [-5, -4, 0, 1, -20],
    [2, 3, 0, 0, 0]
])

summits_list_3 = two_phases_simplex(solvable_matrix_3, prints=False)
for summit in summits_list_3:
    print(summit)
print()


"to counter cycling haven't found solution yet :/"
solvable_matrix_4 = array([
    [1.0/2, -11.0/2, -5/2, 9, 1, 0, 0, 0],
    [1.0/2, -3.0/2, -1/2, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1],
    [-10, 57, 9, 24, 0, 0, 0, 0]
])

summits_list_4 = two_phases_simplex(solvable_matrix_4, opt_max=False)
for summit in summits_list_4:
    print(summit)
print()