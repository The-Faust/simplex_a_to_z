
from numpy import array
from simplex_modular_implementation.simplex_functions import two_phases_simplex

# exercice 1 a)
print("exercize 1 \n ______________________________________________ \n   a) \n")
solvable_matrix_1a = array([
    [1, 0, 1, 0, 0, 6],
    [1.0/4, 1, 0, 1, 0, 6],
    [3, 2, 0, 0, 1, 22],
    [5, 4, 0, 0, 0, 0]
])

summit_list_1a = two_phases_simplex(solvable_matrix_1a)
for summit in summit_list_1a:
    print(summit)
print("_____________________________________________ \n   b)  \n")

solvable_matrix_1b = array([
    [1, 0, 1, 0, 0, 6],
    [1.0/4, 1, 0, 1, 0, 6],
    [3, 2, 0, 0, 1, 22],
    [6, 4, 0, 0, 0, 0]
])

summit_list_1b = two_phases_simplex(solvable_matrix_1b)
for summit in summit_list_1a:
    print(summit)
print("_____________________________________________ \n")